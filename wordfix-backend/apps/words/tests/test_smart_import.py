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

        assert len(result) == 2
        assert result[0]["word"] == "inevitable"
        assert result[1]["word"] == "reluctant"

    def test_analyze_text_filters_existing(self, user, sample_words):
        """Existing words should be filtered out."""
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

        # "apple" already exists in sample_words, so only "inevitable" should be returned
        words_returned = [w["word"] for w in result]
        assert "apple" not in words_returned
        assert "inevitable" in words_returned

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

        assert isinstance(result, list)
        assert len(result) > 0
        # All returned words should be strings
        for item in result:
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
