"""
Factory Boy factories for User app tests.
"""

import factory
from apps.users.infrastructure.models import CustomUser


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for CustomUser model."""

    class Meta:
        model = CustomUser
        django_get_or_create = ("email",)

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")
    full_name = factory.Faker("name")
    native_language = "uz"
    learning_language = "en"
    proficiency_level = "A1"
    daily_goal = 10
    is_active = True
