"""
Tests for Smart Import feature.
"""

import pytest
from unittest.mock import MagicMock, patch
from rest_framework import status

from apps.words.application.use_cases import AnalyzeTextUseCase, ImportWordsUseCase
from apps.words.infrastructure.models import Word


# =============================================================================
# USE CASE TESTS
# =============================================================================


@pytest.mark.django_db
class TestAnalyzeTextUseCase:

    def test_analyze_text_success(self, user, sample_words):
        """AI mock → words are extracted."""
        mock_ai = MagicMock()
        mock_ai.generate_json.return_value = [
            {
                "word": "inevitable",
                "translation": "muqarrar",
                "part_of_speech": "adjective",
                "context_sentence": "It was inevitable that...",
                "difficulty": "hard",
                "reason": "B2+ level word",
            },
            {
                "word": "reluctant",
                "translation": "istaksiz",
                "part_of_speech": "adjective",
                "context_sentence": "She was reluctant to...",
                "difficulty": "medium",
                "reason": "B1+ level word",
            },
        ]

        mock_user_repo = MagicMock()
        mock_user_repo.get_user_language_info.return_value = {
            "native_language": "uz",
            "proficiency_level": "A2",
        }

        from apps.words.infrastructure.repositories import DjangoWordRepository
        word_repo = DjangoWordRepository()

        use_case = AnalyzeTextUseCase(
            word_repo=word_repo,
            ai_provider=mock_ai,
            user_repo=mock_user_repo,
            prompt_template="test {text} {proficiency_level} {native_language} {known_words} {max_words}",
            language_map={"uz": "Uzbek"},
        )

        result = use_case.execute(
            user_id=user.id,
            text="The outcome was inevitable. She was reluctant to admit it.",
        )

        assert isinstance(result, dict)
        assert "suggestions" in result
        assert "parse_mode" in result
        assert len(result["suggestions"]) >= 2
        words = [s["word"] for s in result["suggestions"]]
        assert "inevitable" in words
        assert "reluctant" in words

    def test_analyze_text_filters_existing(self, user, sample_words):
        """Existing words should be marked as in_user_library."""
        mock_ai = MagicMock()
        # Return words that include one in the user's word bank
        mock_ai.generate_json.return_value = [
            {"word": "apple", "translation": "olma", "part_of_speech": "noun",
             "context_sentence": "I ate an apple.", "difficulty": "easy", "reason": "basic"},
            {"word": "inevitable", "translation": "muqarrar", "part_of_speech": "adjective",
             "context_sentence": "It was inevitable.", "difficulty": "hard", "reason": "advanced"},
        ]

        mock_user_repo = MagicMock()
        mock_user_repo.get_user_language_info.return_value = {
            "native_language": "uz", "proficiency_level": "A2",
        }

        from apps.words.infrastructure.repositories import DjangoWordRepository
        word_repo = DjangoWordRepository()

        use_case = AnalyzeTextUseCase(
            word_repo=word_repo,
            ai_provider=mock_ai,
            user_repo=mock_user_repo,
            prompt_template="test {text} {proficiency_level} {native_language} {known_words} {max_words}",
            language_map={"uz": "Uzbek"},
        )

        result = use_case.execute(user_id=user.id, text="I ate an apple. It was inevitable.")

        suggestions = result["suggestions"]
        # "apple" exists in sample_words: it should be included but flagged
        apple_items = [s for s in suggestions if s["word"].lower() == "apple"]
        inevitable_items = [s for s in suggestions if s["word"].lower() == "inevitable"]
        # If apple is present, it should be marked in_user_library
        if apple_items:
            assert apple_items[0]["in_user_library"] is True
        # inevitable should not be in library
        assert len(inevitable_items) >= 1

    def test_analyze_text_fallback_no_ai(self, user):
        """AI fail → simple extraction fallback."""
        mock_user_repo = MagicMock()
        mock_user_repo.get_user_language_info.return_value = {
            "native_language": "uz", "proficiency_level": "A2",
        }

        from apps.words.infrastructure.repositories import DjangoWordRepository
        word_repo = DjangoWordRepository()

        # No AI provider
        use_case = AnalyzeTextUseCase(
            word_repo=word_repo,
            ai_provider=None,
            user_repo=mock_user_repo,
            prompt_template="test {text} {proficiency_level} {native_language} {known_words} {max_words}",
            language_map={"uz": "Uzbek"},
        )

        result = use_case.execute(
            user_id=user.id,
            text="The inevitable consequence of procrastination is failure.",
        )

        assert isinstance(result, dict)
        assert "suggestions" in result
        assert "parse_mode" in result
        suggestions = result["suggestions"]
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        # All returned items should have "word" key
        for item in suggestions:
            assert "word" in item

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


# =============================================================================
# STRUCTURED TEXT PARSING TESTS
# =============================================================================


class TestParseStructuredText:
    """Tests for parse_structured_text function."""

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
