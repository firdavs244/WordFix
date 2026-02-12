"""
Tests for CSV import functionality.
"""

import io
from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.infrastructure.models import CustomUser, UserProgress
from apps.words.application.use_cases.smart_import import CSVImportUseCase, ValidateCSVUseCase
from apps.words.infrastructure.models import Word, WordCategory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    u = CustomUser.objects.create_user(
        email="csvtest@example.com",
        username="csvtestuser",
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
    """Create a CSV SimpleUploadedFile."""
    return SimpleUploadedFile(
        name="test.csv",
        content=content.encode("utf-8"),
        content_type="text/csv",
    )


class TestValidateCSV:
    """Unit tests for CSV validation."""

    def test_validate_csv_minimal(self):
        """word,translation header → valid preview."""
        uc = ValidateCSVUseCase()
        result = uc.execute("word,translation\napple,olma\nrunning,yugurish\n")
        assert result["valid_rows"] == 2
        assert result["has_translation"] is True
        assert len(result["preview"]) == 2

    def test_validate_csv_full(self):
        """Full headers → all flags True."""
        uc = ValidateCSVUseCase()
        csv = "word,translation,difficulty,category,notes\napple,olma,easy,Food,good\n"
        result = uc.execute(csv)
        assert result["has_translation"] is True
        assert result["has_difficulty"] is True
        assert result["has_category"] is True
        assert result["valid_rows"] == 1

    def test_validate_csv_word_only(self):
        """Only word header → has_translation=False."""
        uc = ValidateCSVUseCase()
        result = uc.execute("word\napple\nbanana\n")
        assert result["has_translation"] is False
        assert result["valid_rows"] == 2

    def test_validate_csv_errors(self):
        """Empty rows and too-long words generate errors."""
        uc = ValidateCSVUseCase()
        long_word = "a" * 101
        csv = f"word,translation\n,empty\n{long_word},too long\napple,olma\n"
        result = uc.execute(csv)
        assert result["valid_rows"] == 1
        assert len(result["errors"]) == 2


class TestCSVImport:
    """Unit tests for CSV import use case."""

    def test_import_csv_success(self, user, db):
        """30 words → imported=30."""
        from apps.words.infrastructure.repositories import DjangoWordRepository

        repo = DjangoWordRepository()
        uc = CSVImportUseCase(word_repo=repo, enrich_task=None, enrichment_enabled=False)

        lines = ["word,translation"]
        for i in range(30):
            lines.append(f"word{i},translation{i}")
        csv_content = "\n".join(lines)

        result = uc.execute(user_id=user.id, file_content=csv_content)
        assert result["imported"] == 30
        assert result["skipped_duplicate"] == 0

    def test_import_csv_duplicates(self, user, db):
        """Existing words get skipped."""
        from apps.words.infrastructure.repositories import DjangoWordRepository

        # Create existing word
        Word.objects.create(user=user, original_word="apple", translation="olma")

        repo = DjangoWordRepository()
        uc = CSVImportUseCase(word_repo=repo, enrich_task=None, enrichment_enabled=False)
        result = uc.execute(
            user_id=user.id,
            file_content="word,translation\napple,olma\nbanana,banan\n",
        )
        assert result["imported"] == 1
        assert result["skipped_duplicate"] == 1

    def test_import_csv_with_categories(self, user, db):
        """Categories auto-created."""
        from apps.words.infrastructure.repositories import DjangoWordRepository

        repo = DjangoWordRepository()
        uc = CSVImportUseCase(word_repo=repo, enrich_task=None, enrichment_enabled=False)
        result = uc.execute(
            user_id=user.id,
            file_content="word,translation,difficulty,category\napple,olma,easy,Food\ncar,mashina,medium,Travel\n",
        )
        assert result["imported"] == 2
        assert "Food" in result["categories_created"]
        assert "Travel" in result["categories_created"]
        assert WordCategory.objects.filter(user=user, name="Food").exists()

    def test_import_csv_auto_enrich(self, user, db):
        """Enrich task called for each word."""
        from apps.words.infrastructure.repositories import DjangoWordRepository

        mock_enrich = patch("apps.words.application.use_cases.smart_import.logger").start()
        enrich_calls = []

        def fake_enrich(word_id, user_id):
            enrich_calls.append((word_id, user_id))

        repo = DjangoWordRepository()
        uc = CSVImportUseCase(word_repo=repo, enrich_task=fake_enrich, enrichment_enabled=True)
        result = uc.execute(
            user_id=user.id,
            file_content="word,translation\nhello,salom\nworld,dunyo\n",
        )
        assert result["imported"] == 2
        assert len(enrich_calls) == 2
        patch.stopall()

    def test_import_csv_encoding_utf8(self, user, db):
        """UTF-8 content parsed correctly."""
        from apps.words.infrastructure.repositories import DjangoWordRepository

        repo = DjangoWordRepository()
        uc = CSVImportUseCase(word_repo=repo, enrich_task=None, enrichment_enabled=False)
        result = uc.execute(
            user_id=user.id,
            file_content="word,translation\ncafé,kofe\nnaïve,sodda\n",
        )
        assert result["imported"] == 2

    def test_import_csv_empty_rows_skipped(self, user, db):
        """Empty rows skipped."""
        from apps.words.infrastructure.repositories import DjangoWordRepository

        repo = DjangoWordRepository()
        uc = CSVImportUseCase(word_repo=repo, enrich_task=None, enrichment_enabled=False)
        result = uc.execute(
            user_id=user.id,
            file_content="word,translation\n,\napple,olma\n,\nbanana,banan\n",
        )
        assert result["imported"] == 2
        assert result["skipped_invalid"] == 2

    def test_import_csv_max_500(self, user, db):
        """More than 500 rows → error."""
        from apps.words.infrastructure.repositories import DjangoWordRepository

        lines = ["word,translation"]
        for i in range(501):
            lines.append(f"word{i},translation{i}")
        csv_content = "\n".join(lines)

        repo = DjangoWordRepository()
        uc = CSVImportUseCase(word_repo=repo, enrich_task=None, enrichment_enabled=False)
        result = uc.execute(user_id=user.id, file_content=csv_content)
        assert result["imported"] == 0
        assert len(result["errors"]) > 0

    def test_import_csv_word_only_header(self, user, db):
        """Only word column — still imports."""
        from apps.words.infrastructure.repositories import DjangoWordRepository

        repo = DjangoWordRepository()
        uc = CSVImportUseCase(word_repo=repo, enrich_task=None, enrichment_enabled=False)
        result = uc.execute(
            user_id=user.id,
            file_content="word\napple\nbanana\n",
        )
        assert result["imported"] == 2


class TestCSVViews:
    """Integration tests for CSV upload views."""

    def test_validate_upload_200(self, auth_client, user):
        """File upload → validate returns 200."""
        csv_file = _make_csv("word,translation\napple,olma\n")
        response = auth_client.post(
            "/api/v1/words/import/csv/validate/",
            {"file": csv_file},
            format="multipart",
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["valid_rows"] == 1

    def test_import_upload_201(self, auth_client, user):
        """File upload → import returns 201."""
        csv_file = _make_csv("word,translation\napple,olma\nbanana,banan\n")
        response = auth_client.post(
            "/api/v1/words/import/csv/",
            {"file": csv_file},
            format="multipart",
        )
        assert response.status_code == 201
        data = response.json()
        assert data["data"]["imported"] == 2

    def test_upload_unauth_401(self, api_client, db):
        """Upload without auth → 401."""
        csv_file = _make_csv("word,translation\napple,olma\n")
        response = api_client.post(
            "/api/v1/words/import/csv/",
            {"file": csv_file},
            format="multipart",
        )
        assert response.status_code == 401

    def test_upload_no_file_400(self, auth_client, user):
        """Upload without file → 400."""
        response = auth_client.post(
            "/api/v1/words/import/csv/",
            {},
            format="multipart",
        )
        assert response.status_code == 400

    def test_validate_csv_too_large(self, auth_client, user):
        """File > 1MB → 400."""
        big_content = "word,translation\n" + "a" * (1024 * 1024 + 1) + ",test\n"
        big_file = SimpleUploadedFile(
            name="big.csv",
            content=big_content.encode("utf-8"),
            content_type="text/csv",
        )
        response = auth_client.post(
            "/api/v1/words/import/csv/validate/",
            {"file": big_file},
            format="multipart",
        )
        assert response.status_code == 400

    def test_validate_csv_not_csv(self, auth_client, user):
        """Non-CSV file → 400."""
        txt_file = SimpleUploadedFile(
            name="test.txt",
            content=b"word,translation\napple,olma",
            content_type="text/plain",
        )
        response = auth_client.post(
            "/api/v1/words/import/csv/validate/",
            {"file": txt_file},
            format="multipart",
        )
        assert response.status_code == 400
