"""
Factory definitions for words app tests.
"""

import factory
from django.utils import timezone

from apps.users.infrastructure.models import CustomUser
from apps.words.infrastructure.models import Word, WordCategory


class WordUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Sequence(lambda n: f"worduser{n}@example.com")
    username = factory.Sequence(lambda n: f"worduser{n}")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")


class WordCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WordCategory

    user = factory.SubFactory(WordUserFactory)
    name = factory.Sequence(lambda n: f"Category {n}")
    color = "#6C5CE7"
    icon = "book"


class WordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Word

    user = factory.SubFactory(WordUserFactory)
    original_word = factory.Sequence(lambda n: f"word{n}")
    translation = factory.LazyAttribute(lambda o: f"{o.original_word}_translation")
    difficulty_level = "medium"
    part_of_speech = "noun"
