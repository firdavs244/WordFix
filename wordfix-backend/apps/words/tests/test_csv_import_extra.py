"""
Additional CSV import tests for coverage — edge cases in views and use cases.
"""

import io
from unittest.mock import patch, MagicMock

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.infrastructure.models import CustomUser, UserProgress
from apps.words.application.use_cases.smart_import import (
    CSVImportUseCase,
    ValidateCSVUseCase,
)
from apps.words.infrastructure.models import Word


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    u = CustomUser.objects.create_user(
        email="csvextra@example.com",
        username="csvextra",
        password="testpass123",
    )
    UserProgress.objects.create(user=u)
    return u


@pytest.fixture
def auth_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return api_client


def _make_csv(content: str) -> SimpleUploadedFile:
    return SimpleUploadedFile(
        name="test.csv",
        content=content.encode("utf-8"),
        content_type="text/csv",
    )


class TestValidateCSVEdgeCases:
    """Edge cases for CSV validation."""

    def test_validate_no_headers(self):
        uc = ValidateCSVUseCase()
        result = uc.execute("")
        assert result["errors"] == ["No headers found in CSV file."]
        assert result["valid_rows"] == 0

    def test_validate_missing_word_column(self):
        uc = ValidateCSVUseCase()
        result = uc.execute("translation,difficulty\nolma,easy\n")
        assert "must have a 'word' column" in result["errors"][0]
        assert result["valid_rows"] == 0

    def test_validate_over_max_rows(self):
        uc = ValidateCSVUseCase()
        lines = ["word,translation"]
        for i in range(501):
            lines.append(f"word{i},trans{i}")
        result = uc.execute("\n".join(lines))
        assert any("more than 500" in e for e in result["errors"])

    def test_validate_long_word(self):
        uc = ValidateCSVUseCase()
        long = "a" * 101
        result = uc.execute(f"word\napple\n{long}\nbanana\n")
        assert result["valid_rows"] == 2
        assert any("too long" in e for e in result["errors"])

    def test_validate_preview_max_10(self):
        uc = ValidateCSVUseCase()
        lines = ["word"]
        for i in range(20):
            lines.append(f"word{i}")
        result = uc.execute("\n".join(lines))
        assert len(result["preview"]) == 10
        assert result["valid_rows"] == 20


class TestCSVImportEdgeCases:
    """Edge cases for CSV import use case."""

    def test_import_no_headers(self, user, db):
        from apps.words.infrastructure.repositories import DjangoWordRepository

        repo = DjangoWordRepository()
        uc = CSVImportUseCase(word_repo=repo, enrich_task=None, enrichment_enabled=False)
        result = uc.execute(user_id=user.id, file_content="")
        assert result["imported"] == 0
        assert "No headers" in result["errors"][0]

    def test_import_invalid_difficulty_defaults_to_medium(self, user, db):
        from apps.words.infrastructure.repositories import DjangoWordRepository

        repo = DjangoWordRepository()
        uc = CSVImportUseCase(word_repo=repo, enrich_task=None, enrichment_enabled=False)
        result = uc.execute(
            user_id=user.id,
            file_content="word,translation,difficulty\napple,olma,EXPERT\n",
        )
        assert result["imported"] == 1
        word = Word.objects.get(user=user, original_word="apple")
        assert word.difficulty_level == "medium"

    def test_import_enrichment_failure_continues(self, user, db):
        from apps.words.infrastructure.repositories import DjangoWordRepository

        def failing_enrich(word_id, user_id):
            raise RuntimeError("Celery down")

        repo = DjangoWordRepository()
        uc = CSVImportUseCase(word_repo=repo, enrich_task=failing_enrich, enrichment_enabled=True)
        result = uc.execute(
            user_id=user.id,
            file_content="word,translation\nhello,salom\n",
        )
        assert result["imported"] == 1  # still imported despite enrichment failure

    def test_import_word_too_long_skipped_invalid(self, user, db):
        from apps.words.infrastructure.repositories import DjangoWordRepository

        repo = DjangoWordRepository()
        uc = CSVImportUseCase(word_repo=repo, enrich_task=None, enrichment_enabled=False)
        long_word = "x" * 101
        result = uc.execute(
            user_id=user.id,
            file_content=f"word,translation\n{long_word},trans\napple,olma\n",
        )
        assert result["imported"] == 1
        assert result["skipped_invalid"] == 1

    def test_import_with_notes(self, user, db):
        from apps.words.infrastructure.repositories import DjangoWordRepository

        repo = DjangoWordRepository()
        uc = CSVImportUseCase(word_repo=repo, enrich_task=None, enrichment_enabled=False)
        result = uc.execute(
            user_id=user.id,
            file_content="word,translation,notes\napple,olma,A fruit I like\n",
        )
        assert result["imported"] == 1


class TestCSVViewEdgeCases:
    """CSV view integration edge cases."""

    def test_csv_import_with_errors_returns_400(self, auth_client, user):
        """CSV with >500 rows returns 400."""
        lines = ["word,translation"]
        for i in range(501):
            lines.append(f"word{i},trans{i}")
        csv_file = _make_csv("\n".join(lines))
        response = auth_client.post(
            "/api/v1/words/import/csv/",
            {"file": csv_file},
            format="multipart",
        )
        assert response.status_code == 400

    def test_csv_validate_non_csv_extension_400(self, auth_client, user):
        """Non-.csv extension rejected."""
        f = SimpleUploadedFile(
            name="test.xlsx",
            content=b"word,translation\napple,olma",
            content_type="application/vnd.ms-excel",
        )
        response = auth_client.post(
            "/api/v1/words/import/csv/validate/",
            {"file": f},
            format="multipart",
        )
        assert response.status_code == 400

    def test_csv_import_awards_xp(self, auth_client, user):
        """Successful import awards XP."""
        csv_file = _make_csv("word,translation\napple,olma\nbanana,banan\n")
        response = auth_client.post(
            "/api/v1/words/import/csv/",
            {"file": csv_file},
            format="multipart",
        )
        assert response.status_code == 201
        data = response.json()["data"]
        assert data["imported"] == 2
        # XP should be present in response
        assert "xp_earned" in data
