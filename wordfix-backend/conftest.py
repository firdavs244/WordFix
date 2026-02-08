"""
Root conftest for WordFix backend tests.

Provides shared fixtures: api_client, user, authenticated_client,
word factory, category factory.
"""

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.infrastructure.models import CustomUser
from apps.words.infrastructure.models import Word, WordCategory


@pytest.fixture
def api_client():
    """Return a DRF APIClient."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create and return a regular user."""
    return CustomUser.objects.create_user(
        email="test@example.com",
        username="testuser",
        password="testpass123",
        full_name="Test User",
    )


@pytest.fixture
def another_user(db):
    """Create and return a second user for isolation tests."""
    return CustomUser.objects.create_user(
        email="another@example.com",
        username="anotheruser",
        password="testpass123",
        full_name="Another User",
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Return an API client authenticated with JWT."""
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return api_client


@pytest.fixture
def another_authenticated_client(api_client, another_user):
    """Return an API client authenticated as another_user."""
    client = APIClient()
    refresh = RefreshToken.for_user(another_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return client


@pytest.fixture
def word_category(user):
    """Create and return a word category for user."""
    return WordCategory.objects.create(
        user=user,
        name="Test Category",
        color="#6C5CE7",
        icon="book",
    )


@pytest.fixture
def sample_word(user, word_category):
    """Create and return a sample word for user."""
    return Word.objects.create(
        user=user,
        original_word="hello",
        translation="salom",
        pronunciation="/həˈloʊ/",
        part_of_speech="interjection",
        definition="Used as a greeting.",
        example_sentence="Hello, how are you?",
        example_translation="Salom, qalaysiz?",
        difficulty_level="easy",
        category=word_category,
    )


@pytest.fixture
def sample_words(user, word_category):
    """Create 5 sample words for testing lists/pagination."""
    words = []
    word_data = [
        ("apple", "olma", "noun", "easy"),
        ("run", "yugurmoq", "verb", "easy"),
        ("beautiful", "chiroyli", "adjective", "medium"),
        ("quickly", "tez", "adverb", "medium"),
        ("hypothesis", "gipoteza", "noun", "hard"),
    ]
    for original, translation, pos, difficulty in word_data:
        w = Word.objects.create(
            user=user,
            original_word=original,
            translation=translation,
            part_of_speech=pos,
            difficulty_level=difficulty,
            category=word_category,
        )
        words.append(w)
    return words
