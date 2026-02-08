"""
Tests for Word use cases.
"""

import uuid

import pytest

from apps.common.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    ValidationError,
)
from apps.words.application.use_cases import (
    AddWordUseCase,
    BulkAddWordsUseCase,
    DeleteWordUseCase,
    GetWordDetailUseCase,
    GetWordsUseCase,
    GetWordStatsUseCase,
    SearchWordsUseCase,
    UpdateWordUseCase,
)
from apps.words.infrastructure.repositories import DjangoWordRepository


@pytest.mark.django_db
class TestAddWordUseCase:
    @pytest.fixture
    def use_case(self):
        return AddWordUseCase(repository=DjangoWordRepository())

    def test_add_word(self, use_case, user):
        entity = use_case.execute(
            user_id=user.id,
            data={"original_word": "test", "translation": "sinov"},
        )
        assert entity.original_word == "test"

    def test_add_duplicate_raises(self, use_case, user, sample_word):
        with pytest.raises(EntityAlreadyExistsError):
            use_case.execute(
                user_id=user.id,
                data={"original_word": sample_word.original_word},
            )

    def test_add_word_empty_raises(self, use_case, user):
        with pytest.raises(ValidationError):
            use_case.execute(user_id=user.id, data={"original_word": ""})

    def test_add_word_whitespace_raises(self, use_case, user):
        with pytest.raises(ValidationError):
            use_case.execute(user_id=user.id, data={"original_word": "   "})


@pytest.mark.django_db
class TestGetWordsUseCase:
    @pytest.fixture
    def use_case(self):
        return GetWordsUseCase(repository=DjangoWordRepository())

    def test_get_words(self, use_case, user, sample_words):
        words, total = use_case.execute(user_id=user.id)
        assert total == 5

    def test_get_words_with_filters(self, use_case, user, sample_words):
        words, total = use_case.execute(
            user_id=user.id, filters={"difficulty_level": "hard"}
        )
        assert total == 1

    def test_get_words_empty(self, use_case, user):
        words, total = use_case.execute(user_id=user.id)
        assert total == 0


@pytest.mark.django_db
class TestGetWordDetailUseCase:
    @pytest.fixture
    def use_case(self):
        return GetWordDetailUseCase(repository=DjangoWordRepository())

    def test_get_detail(self, use_case, user, sample_word):
        entity = use_case.execute(word_id=sample_word.id, user_id=user.id)
        assert entity.original_word == sample_word.original_word

    def test_not_found(self, use_case, user):
        with pytest.raises(EntityNotFoundError):
            use_case.execute(word_id=uuid.uuid4(), user_id=user.id)


@pytest.mark.django_db
class TestUpdateWordUseCase:
    @pytest.fixture
    def use_case(self):
        return UpdateWordUseCase(repository=DjangoWordRepository())

    def test_update(self, use_case, user, sample_word):
        entity = use_case.execute(
            word_id=sample_word.id,
            user_id=user.id,
            data={"translation": "yangi"},
        )
        assert entity.translation == "yangi"

    def test_update_ignores_original_word(self, use_case, user, sample_word):
        entity = use_case.execute(
            word_id=sample_word.id,
            user_id=user.id,
            data={"original_word": "changed", "translation": "ok"},
        )
        assert entity.original_word == sample_word.original_word

    def test_update_not_found(self, use_case, user):
        with pytest.raises(EntityNotFoundError):
            use_case.execute(
                word_id=uuid.uuid4(), user_id=user.id, data={"translation": "x"}
            )


@pytest.mark.django_db
class TestDeleteWordUseCase:
    @pytest.fixture
    def use_case(self):
        return DeleteWordUseCase(repository=DjangoWordRepository())

    def test_delete(self, use_case, user, sample_word):
        use_case.execute(word_id=sample_word.id, user_id=user.id)
        from apps.words.infrastructure.models import Word
        assert not Word.objects.filter(id=sample_word.id).exists()

    def test_delete_not_found(self, use_case, user):
        with pytest.raises(EntityNotFoundError):
            use_case.execute(word_id=uuid.uuid4(), user_id=user.id)


@pytest.mark.django_db
class TestBulkAddWordsUseCase:
    @pytest.fixture
    def use_case(self):
        return BulkAddWordsUseCase(repository=DjangoWordRepository())

    def test_bulk_add(self, use_case, user):
        result = use_case.execute(
            user_id=user.id,
            words_data=[
                {"original_word": "b1", "translation": "t1"},
                {"original_word": "b2", "translation": "t2"},
            ],
        )
        assert result["created"] == 2

    def test_bulk_skip_duplicates(self, use_case, user, sample_word):
        result = use_case.execute(
            user_id=user.id,
            words_data=[
                {"original_word": sample_word.original_word, "translation": "dup"},
            ],
        )
        assert result["skipped"] == 1


@pytest.mark.django_db
class TestGetWordStatsUseCase:
    @pytest.fixture
    def use_case(self):
        return GetWordStatsUseCase(repository=DjangoWordRepository())

    def test_stats(self, use_case, user, sample_words):
        stats = use_case.execute(user_id=user.id)
        assert stats["total"] == 5

    def test_stats_empty(self, use_case, user):
        stats = use_case.execute(user_id=user.id)
        assert stats["total"] == 0


@pytest.mark.django_db
class TestSearchWordsUseCase:
    @pytest.fixture
    def use_case(self):
        return SearchWordsUseCase(repository=DjangoWordRepository())

    def test_search(self, use_case, user, sample_words):
        words, total = use_case.execute(user_id=user.id, query="apple")
        assert total >= 1

    def test_search_no_results(self, use_case, user, sample_words):
        words, total = use_case.execute(user_id=user.id, query="zzzzzzz")
        assert total == 0
