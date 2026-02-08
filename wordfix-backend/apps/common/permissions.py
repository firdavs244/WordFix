"""
Base permission classes for WordFix API.
"""

from rest_framework.permissions import BasePermission


class IsActiveUser(BasePermission):
    """
    Permission that only allows active users to access the view.
    """

    message = "Your account is not active."

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
        )


class IsOwner(BasePermission):
    """
    Permission that only allows owners of an object to access it.

    Expects the object to have a 'user' attribute or 'owner' attribute.
    """

    message = "You are not the owner of this resource."

    def has_object_permission(self, request, view, obj) -> bool:
        owner = getattr(obj, "user", None) or getattr(obj, "owner", None)
        return owner == request.user
