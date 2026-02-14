"""
Root conftest for WordFix backend tests.

Provides shared fixtures: api_client, user, authenticated_client,
word factory, category factory.
"""

import os

# Force test settings before Django setup — Docker env sets 'development'
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.test"

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


@pytest.fixture
def confusing_pair(user, sample_words):
    """Create a confusing pair between two sample words."""
    from apps.words.infrastructure.models import ConfusingPair
    word_1, word_2 = sample_words[0], sample_words[1]
    # Ensure consistent ordering (smaller UUID first)
    if str(word_1.id) > str(word_2.id):
        word_1, word_2 = word_2, word_1
    return ConfusingPair.objects.create(
        user=user,
        word_1=word_1,
        word_2=word_2,
        confusion_count=3,
    )


@pytest.fixture
def daily_challenge(user):
    """Create a daily challenge for today."""
    from apps.words.infrastructure.models import DailyChallenge
    from datetime import date
    challenge, _ = DailyChallenge.objects.get_or_create(
        user=user,
        date=date.today(),
        defaults={
            "challenges": [
                {"type": "review_words", "target": 5, "current": 0, "completed": False,
                 "xp_reward": 20, "title": "Review 5 words", "icon": "book"},
                {"type": "add_words", "target": 3, "current": 0, "completed": False,
                 "xp_reward": 20, "title": "Add 3 new words", "icon": "plus"},
                {"type": "play_game", "target": 1, "current": 0, "completed": False,
                 "xp_reward": 15, "title": "Play any game", "icon": "gamepad"},
            ],
        },
    )
    return challenge


@pytest.fixture
def word_with_distractors(sample_word):
    """Create a word with pre-generated distractors."""
    from apps.words.infrastructure.models import WordDistractor
    distractor = WordDistractor.objects.create(
        word=sample_word,
        distractors=["goodbye", "sorry", "thanks"],
        language="en",
        generated_by="fallback",
    )
    return sample_word, distractor


@pytest.fixture
def review_session(user):
    """Create a review session for testing."""
    from apps.words.infrastructure.models import ReviewSession
    return ReviewSession.objects.create(
        user=user,
        session_type="review",
        total_words=0,
    )


@pytest.fixture
def test_session(user):
    """Create a test session for testing."""
    from apps.words.infrastructure.models import TestSession
    return TestSession.objects.create(
        user=user,
        test_type="mixed",
        difficulty="adaptive",
        total_questions=5,
    )


@pytest.fixture
def game_session(user):
    """Create a game session for testing."""
    from apps.words.infrastructure.models import GameSession
    return GameSession.objects.create(
        user=user,
        game_type="speed_round",
        max_score=10,
    )
