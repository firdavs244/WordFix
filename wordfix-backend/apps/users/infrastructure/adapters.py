"""
Custom social account adapter for Google OAuth.
"""

import uuid

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom adapter to link existing accounts and create UserProgress."""

    def pre_social_login(self, request, sociallogin):
        """
        If email already exists, link the social account to existing user.
        """
        email = sociallogin.account.extra_data.get("email", "")
        if email:
            from apps.users.infrastructure.models import CustomUser

            try:
                user = CustomUser.objects.get(email=email.lower())
                sociallogin.connect(request, user)
            except CustomUser.DoesNotExist:
                pass

    def save_user(self, request, sociallogin, form=None):
        """
        Create user from Google data with auto-generated username.
        Also creates UserProgress.
        """
        user = super().save_user(request, sociallogin, form)
        data = sociallogin.account.extra_data
        user.full_name = data.get("name", "")
        if not user.username:
            user.username = f"user_{uuid.uuid4().hex[:8]}"
        user.save()

        # Create UserProgress
        from apps.users.infrastructure.models import UserProgress

        UserProgress.objects.get_or_create(user=user)

        return user
