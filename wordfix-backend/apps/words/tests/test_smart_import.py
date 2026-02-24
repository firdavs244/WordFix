"""
Tests for Smart Import feature — AI-First Architecture (Sprint 12.4).
"""

import json
import pytest
from unittest.mock import MagicMock, patch
from rest_framework import status

from apps.words.application.use_cases import AnalyzeTextUseCase, ImportWordsUseCase
from apps.words.infrastructure.models import Word


# =============================================================================
# MOCK HELPERS
# =============================================================================


class MockAIProvider:
    """AI provider mock — har doim to'g'ri natija qaytaradi."""

    def __init__(self, response=None):
        self._response = response

    def is_available(self):
        return True

    def get_provider_name(self):
        return "mock"

    def generate_json(self, prompt, **kwargs):
        if self._response is not None:
            return self._response
        return []

    def generate_text(self, prompt, **kwargs):
        if self._response is not None:
            return json.dumps(self._response)
        return "[]"


class MockWordRepo:
    """Word repository mock."""

    def __init__(self, existing_words=None):
        self._existing = existing_words or []

    def get_all_by_user(self, user_id, page=1, page_size=10000):
        # Return mock word objects with original_word attr
        words = []
        for w in self._existing:
            obj = MagicMock()
            obj.original_word = w
            words.append(obj)
        return words, len(words)

    def get_user_word_list(self, user_id):
        return self._existing

    def get_words(self, user_id, **kwargs):
        return []

    def exists(self, word, user_id):
        return word.lower() in [w.lower() for w in self._existing]


# =============================================================================
# AI-FIRST USE CASE TESTS
# =============================================================================


class TestSmartImportAI:

    def test_dictionary_format_keeps_user_translation(self):
        """
        Foydalanuvchi lug'atdan copy qilsa:
        grip: ushlab olish
        AI foydalanuvchi tarjimasini saqlab qolishi kerak.
        """
        ai_response_extract = [
            {
                "word": "grip",
                "translation": "ushlab olish",
                "translation_source": "user",
                "pronunciation": "/ɡrɪp/",
                "definition": "to hold something firmly",
                "example": "She gripped the handle tightly.",
                "part_of_speech": "verb",
                "cefr": "B1"
            }
        ]

        ai_response_validate = [
            {
                "word": "grip",
                "is_valid_english": True,
                "translation_correct": True,
                "correct_translation": "ushlab olish",
                "cefr": "B1"
            }
        ]

        call_count = 0

        def mock_generate_json(prompt, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return ai_response_extract
            return ai_response_validate

        provider = MockAIProvider()
        provider.generate_json = mock_generate_json

        use_case = AnalyzeTextUseCase(
            word_repo=MockWordRepo(),
            ai_provider=provider
        )

        result = use_case.execute("00000000-0000-0000-0000-000000000001", "grip: ushlab olish")

        assert result["total_found"] == 1
        assert result["suggestions"][0]["word"] == "grip"
        assert result["suggestions"][0]["translation"] == "ushlab olish"
        assert result["parse_mode"] == "ai"

    def test_wrong_translation_gets_corrected(self):
        """
        grip: koptok — XATO tarjima
        AI buni aniqlashi va to'g'rilashi kerak.
        """
        ai_response_extract = [
            {
                "word": "grip",
                "translation": "koptok",
                "translation_source": "corrected",
                "original_user_translation": "koptok",
                "pronunciation": "/ɡrɪp/",
                "definition": "to hold firmly",
                "example": "Grip the rope with both hands.",
                "part_of_speech": "verb",
                "cefr": "B1"
            }
        ]

        ai_response_validate = [
            {
                "word": "grip",
                "is_valid_english": True,
                "translation_correct": False,
                "correct_translation": "mahkam ushlamoq",
                "cefr": "B1"
            }
        ]

        call_count = 0

        def mock_generate_json(prompt, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return ai_response_extract
            return ai_response_validate

        provider = MockAIProvider()
        provider.generate_json = mock_generate_json

        use_case = AnalyzeTextUseCase(
            word_repo=MockWordRepo(),
            ai_provider=provider
        )

        result = use_case.execute("00000000-0000-0000-0000-000000000001", "grip: koptok")

        assert result["total_found"] == 1
        assert result["suggestions"][0]["translation"] == "mahkam ushlamoq"

    def test_pdf_noise_text(self):
        """PDF dan ko'chirilgan noise li matn."""
        ai_response_extract = [
            {"word": "female", "translation": "urg'ochi", "cefr": "A1",
             "pronunciation": "/ˈfiː.meɪl/", "definition": "a woman or girl",
             "example": "The female lion hunts.", "part_of_speech": "noun"},
            {"word": "adult", "translation": "voyaga yetgan", "cefr": "A2",
             "pronunciation": "/ˈæd.ʌlt/", "definition": "a fully grown person",
             "example": "Only adults can drive.", "part_of_speech": "noun"},
            {"word": "powerful", "translation": "kuchli", "cefr": "A2",
             "pronunciation": "/ˈpaʊ.ə.fəl/", "definition": "having great strength",
             "example": "The engine is very powerful.", "part_of_speech": "adjective"},
        ]

        ai_response_validate = [
            {"word": "female", "is_valid_english": True, "translation_correct": True,
             "correct_translation": "urg'ochi", "cefr": "A1"},
            {"word": "adult", "is_valid_english": True, "translation_correct": True,
             "correct_translation": "voyaga yetgan", "cefr": "A2"},
            {"word": "powerful", "is_valid_english": True, "translation_correct": True,
             "correct_translation": "kuchli", "cefr": "A2"},
        ]

        call_count = 0

        def mock_generate_json(prompt, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return ai_response_extract
            return ai_response_validate

        provider = MockAIProvider()
        provider.generate_json = mock_generate_json

        use_case = AnalyzeTextUseCase(
            word_repo=MockWordRepo(),
            ai_provider=provider
        )

        text = """NotebookLM
Unit 9: The Anatomy of a Kangaroo
1. Female
Urg'ochi
2. Adult
Voyaga yetgan
www.example.com $5.00
Powerful
Kuchli"""

        result = use_case.execute("00000000-0000-0000-0000-000000000001", text)

        assert result["total_found"] == 3
        assert result["ai_used"] is True
        words = [s["word"] for s in result["suggestions"]]
        assert "female" in words
        assert "adult" in words
        assert "powerful" in words

    def test_empty_text(self):
        use_case = AnalyzeTextUseCase(
            word_repo=MockWordRepo(),
            ai_provider=MockAIProvider()
        )
        with pytest.raises(Exception):
            use_case.execute("00000000-0000-0000-0000-000000000001", "")

    def test_very_short_text(self):
        use_case = AnalyzeTextUseCase(
            word_repo=MockWordRepo(),
            ai_provider=MockAIProvider()
        )
        result = use_case.execute("00000000-0000-0000-0000-000000000001", "ab ")
        assert result["total_found"] == 0

    def test_ai_failure_uses_fallback(self):
        """AI fail bo'lsa — fallback ishlaydi."""

        class FailingAIProvider:
            def is_available(self):
                return True

            def get_provider_name(self):
                return "failing"

            def generate_json(self, prompt, **kwargs):
                raise ConnectionError("API down")

            def generate_text(self, prompt, **kwargs):
                raise ConnectionError("API down")

        use_case = AnalyzeTextUseCase(
            word_repo=MockWordRepo(),
            ai_provider=FailingAIProvider()
        )

        result = use_case.execute(
            "00000000-0000-0000-0000-000000000001",
            "1. Apple\nOlma\n2. Book\nKitob"
        )

        assert result["parse_mode"] == "fallback"

    def test_ai_unavailable_uses_fallback(self):
        """AI provider unavailable."""

        class UnavailableAI:
            def is_available(self):
                return False

        use_case = AnalyzeTextUseCase(
            word_repo=MockWordRepo(),
            ai_provider=UnavailableAI()
        )

        result = use_case.execute(
            "00000000-0000-0000-0000-000000000001",
            "Hello\nSalom"
        )
        assert result["parse_mode"] == "fallback"

    def test_existing_words_marked(self):
        """Mavjud so'zlar in_user_library=True bo'lishi kerak."""

        ai_response = [
            {"word": "apple", "translation": "olma", "cefr": "A1"},
            {"word": "book", "translation": "kitob", "cefr": "A1"},
        ]

        call_count = 0

        def mock_gen(prompt, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return ai_response
            return [
                {"word": "apple", "is_valid_english": True, "translation_correct": True,
                 "correct_translation": "olma", "cefr": "A1"},
                {"word": "book", "is_valid_english": True, "translation_correct": True,
                 "correct_translation": "kitob", "cefr": "A1"},
            ]

        provider = MockAIProvider()
        provider.generate_json = mock_gen

        use_case = AnalyzeTextUseCase(
            word_repo=MockWordRepo(existing_words=["apple"]),
            ai_provider=provider
        )

        result = use_case.execute("00000000-0000-0000-0000-000000000001", "apple, book")

        assert result["already_in_library"] == 1
        apple = next(s for s in result["suggestions"] if s["word"] == "apple")
        book = next(s for s in result["suggestions"] if s["word"] == "book")
        assert apple["in_user_library"] is True
        assert book["in_user_library"] is False

    def test_various_formats(self):
        """Turli xil formatlar — AI barchani tushunishi kerak."""

        formats = [
            "grip: ushlab olish",
            "grip - ushlab olish",
            "grip — ushlab olish",
            "grip = ushlab olish",
            "grip (ushlab olish)",
            "1. grip - ushlab olish",
            "grip\nushlab olish",
        ]

        for fmt in formats:
            ai_response = [{"word": "grip", "translation": "ushlab olish", "cefr": "B1"}]

            call_count = 0

            def mock_gen(prompt, **kwargs):
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    return ai_response
                return [{"word": "grip", "is_valid_english": True,
                         "translation_correct": True,
                         "correct_translation": "ushlab olish", "cefr": "B1"}]

            provider = MockAIProvider()
            provider.generate_json = mock_gen

            use_case = AnalyzeTextUseCase(
                word_repo=MockWordRepo(),
                ai_provider=provider
            )

            result = use_case.execute("00000000-0000-0000-0000-000000000001", fmt)
            assert result["total_found"] >= 1, f"Format failed: {fmt}"

    def test_extract_json_from_markdown(self):
        """AI markdown bilan javob bersa ham ishlashi kerak."""
        use_case = AnalyzeTextUseCase(word_repo=MockWordRepo())

        text = '```json\n[{"word": "hello", "translation": "salom"}]\n```'
        result = use_case._extract_json_from_text(text)
        assert len(result) == 1
        assert result[0]["word"] == "hello"

    def test_extract_json_from_plain(self):
        use_case = AnalyzeTextUseCase(word_repo=MockWordRepo())

        text = 'Here are the words:\n[{"word": "hello", "translation": "salom"}]'
        result = use_case._extract_json_from_text(text)
        assert len(result) == 1

    def test_ai_no_provider(self):
        """AI provider None — fallback ishlaydi."""
        use_case = AnalyzeTextUseCase(
            word_repo=MockWordRepo(),
            ai_provider=None
        )

        result = use_case.execute(
            "00000000-0000-0000-0000-000000000001",
            "Hello\nSalom\nBook\nKitob"
        )
        assert result["parse_mode"] == "fallback"
        assert result["ai_used"] is False

    def test_result_structure(self):
        """Result da barcha kerakli fieldlar bo'lishi kerak."""
        ai_response = [{"word": "test", "translation": "test", "cefr": "A1"}]

        call_count = 0

        def mock_gen(prompt, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return ai_response
            return [{"word": "test", "is_valid_english": True,
                     "translation_correct": True,
                     "correct_translation": "test", "cefr": "A1"}]

        provider = MockAIProvider()
        provider.generate_json = mock_gen

        use_case = AnalyzeTextUseCase(
            word_repo=MockWordRepo(),
            ai_provider=provider
        )

        result = use_case.execute("00000000-0000-0000-0000-000000000001", "test word")

        assert "suggestions" in result
        assert "parse_mode" in result
        assert "total_found" in result
        assert "already_in_library" in result
        assert "new_words" in result
        assert "text_difficulty" in result
        assert "ai_used" in result

    def test_minimal_clean_urls_removed(self):
        """URL va emaillar olib tashlanishi kerak."""
        use_case = AnalyzeTextUseCase(word_repo=MockWordRepo())

        cleaned = use_case._minimal_clean(
            "Hello https://example.com world test@email.com www.site.com end"
        )
        assert "https://" not in cleaned
        assert "test@email.com" not in cleaned
        assert "www.site.com" not in cleaned
        assert "Hello" in cleaned
        assert "world" in cleaned

    def test_calc_difficulty(self):
        """Difficulty hisoblash."""
        use_case = AnalyzeTextUseCase(word_repo=MockWordRepo())

        suggestions = [
            {"difficulty": "A1"},
            {"difficulty": "A1"},
            {"difficulty": "A2"},
        ]
        result = use_case._calc_difficulty(suggestions)
        assert result in ("A1", "A2")

    def test_empty_result_structure(self):
        """Bo'sh natija to'g'ri strukturada bo'lishi kerak."""
        use_case = AnalyzeTextUseCase(word_repo=MockWordRepo())

        result = use_case._empty_result()
        assert result["total_found"] == 0
        assert result["suggestions"] == []
        assert result["ai_used"] is False

    def test_backward_compat_kwargs(self):
        """Eski kwargs (user_repo, prompt_template, language_map) qabul qilinishi kerak."""
        mock_user_repo = MagicMock()
        use_case = AnalyzeTextUseCase(
            word_repo=MockWordRepo(),
            ai_provider=MockAIProvider(),
            user_repo=mock_user_repo,
            prompt_template="test {text}",
            language_map={"uz": "Uzbek"},
        )
        assert use_case.user_repo is mock_user_repo
        assert use_case.prompt_template == "test {text}"
        assert use_case.language_map == {"uz": "Uzbek"}

    def test_validation_skips_non_english(self):
        """Validation bosqichida ingliz bo'lmagan so'zlar o'chirilishi kerak."""
        ai_response_extract = [
            {"word": "apple", "translation": "olma", "cefr": "A1"},
            {"word": "kitob", "translation": "book", "cefr": "A1"},
        ]

        ai_response_validate = [
            {"word": "apple", "is_valid_english": True, "translation_correct": True,
             "correct_translation": "olma", "cefr": "A1"},
            {"word": "kitob", "is_valid_english": False, "translation_correct": False,
             "correct_translation": "", "cefr": "A1"},
        ]

        call_count = 0

        def mock_gen(prompt, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return ai_response_extract
            return ai_response_validate

        provider = MockAIProvider()
        provider.generate_json = mock_gen

        use_case = AnalyzeTextUseCase(
            word_repo=MockWordRepo(),
            ai_provider=provider
        )

        result = use_case.execute("00000000-0000-0000-0000-000000000001", "apple kitob")
        assert result["total_found"] == 1
        assert result["suggestions"][0]["word"] == "apple"


# =============================================================================
# IMPORT ADD TESTS
# =============================================================================


@pytest.mark.django_db
class TestImportWordsUseCase:

    def test_import_add_words(self, user):
        """Selected words are added to word bank."""
        from apps.words.infrastructure.repositories import DjangoWordRepository
        word_repo = DjangoWordRepository()

        use_case = ImportWordsUseCase(word_repo=word_repo, enrich_task=None, enrichment_enabled=False)

        result = use_case.execute(
            user_id=user.id,
            selected_words=[
                {"original_word": "inevitable", "translation": "muqarrar", "difficulty_level": "hard"},
                {"original_word": "reluctant", "translation": "istaksiz", "difficulty_level": "medium"},
            ],
        )

        assert result["added"] == 2
        assert result["skipped"] == 0
        assert Word.objects.filter(user=user, original_word="inevitable").exists()
        assert Word.objects.filter(user=user, original_word="reluctant").exists()

    def test_import_skips_duplicates(self, user, sample_word):
        """Duplicate words are skipped."""
        from apps.words.infrastructure.repositories import DjangoWordRepository
        word_repo = DjangoWordRepository()

        use_case = ImportWordsUseCase(word_repo=word_repo, enrich_task=None, enrichment_enabled=False)

        result = use_case.execute(
            user_id=user.id,
            selected_words=[
                {"original_word": "hello", "translation": "salom"},  # already exists
                {"original_word": "newword", "translation": "yangi"},
            ],
        )

        assert result["added"] == 1
        assert result["skipped"] == 1


# =============================================================================
# VIEW TESTS
# =============================================================================


@pytest.mark.django_db
class TestImportViews:

    def test_analyze_endpoint_unauth(self, api_client):
        """Unauthenticated → 401."""
        resp = api_client.post("/api/v1/words/import/analyze/", {"text": "hello"}, format="json")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_add_endpoint_unauth(self, api_client):
        """Unauthenticated → 401."""
        resp = api_client.post("/api/v1/words/import/add/", {"words": [{"original_word": "test"}]}, format="json")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_add_words_endpoint(self, authenticated_client):
        """POST import/add → 201 with added count."""
        resp = authenticated_client.post(
            "/api/v1/words/import/add/",
            {"words": [
                {"original_word": "imported_word", "translation": "tarjima", "difficulty_level": "medium"},
            ]},
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data["data"]["added"] == 1

    def test_analyze_text_empty(self, authenticated_client):
        """Empty text → 400."""
        response = authenticated_client.post(
            "/api/v1/words/import/analyze/",
            {"text": ""},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_analyze_text_too_long(self, authenticated_client):
        """Text > 5000 chars → 400."""
        response = authenticated_client.post(
            "/api/v1/words/import/analyze/",
            {"text": "a" * 5001},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# =============================================================================
# STRUCTURED TEXT PARSING TESTS (Backward compat)
# =============================================================================


class TestParseStructuredText:
    """Tests for parse_structured_text function (backward compat)."""

    def test_parse_multi_unit_text(self):
        """Test parsing text with multiple Unit sections."""
        from apps.words.application.use_cases.smart_import import parse_structured_text

        text = """Unit 6: Our Favorite Hobbies
1. Clap – qarsak chalmoq
2. Nervous – xavotirlangan
3. Score – ball, ochko

Unit 7: Sport time
4. Catch – tutib olmoq
5. Choose – tanlamoq
6. Smile – jilmaymoq

Unit 8: At school
7. Base – asos
8. Bat – ko'rshapalak
9. Kick – tepmoq"""

        result = parse_structured_text(text)
        assert len(result) == 9
        assert result[0]["word"] == "Clap"
        assert result[0]["translation"] == "qarsak chalmoq"
        assert result[8]["word"] == "Kick"

    def test_parse_with_parentheses(self):
        """Test parsing words with parenthetical forms."""
        from apps.words.application.use_cases.smart_import import parse_structured_text

        text = """1. Choose (chose) – tanlamoq
2. Write (wrote) – yozmoq
3. Run (ran) – yugurmoq"""

        result = parse_structured_text(text)
        assert len(result) == 3
        assert result[0]["word"] == "Choose"
        assert result[0].get("notes") == "chose"

    def test_ignore_unit_headers(self):
        """Test that unit/section headers are skipped."""
        from apps.words.application.use_cases.smart_import import parse_structured_text

        text = """Unit 6: Our Favorite Hobbies
1. Clap – qarsak chalmoq
Unit 7: Sport
2. Run – yugurmoq"""

        result = parse_structured_text(text)
        assert len(result) == 2
        words = [r["word"] for r in result]
        assert "Unit 6" not in " ".join(words)

    def test_parse_phrasal_verbs(self):
        """Test parsing phrasal verbs."""
        from apps.words.application.use_cases.smart_import import parse_structured_text

        text = """1. Shout at – baqirmoq
2. Step up – ko'tarilmoq
3. Write down – yozib olmoq"""

        result = parse_structured_text(text)
        assert len(result) == 3
        assert result[0]["word"] == "Shout at"
        assert result[2]["word"] == "Write down"
