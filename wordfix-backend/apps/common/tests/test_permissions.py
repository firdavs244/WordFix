"""
Tests for base permission classes.
"""

from unittest.mock import MagicMock

import pytest

from apps.common.permissions import IsActiveUser, IsOwner


class TestIsActiveUser:
    """Tests for IsActiveUser permission."""

    def test_active_authenticated_user_allowed(self):
        perm = IsActiveUser()
        request = MagicMock()
        request.user.is_authenticated = True
        request.user.is_active = True
        assert perm.has_permission(request, None) is True

    def test_inactive_user_denied(self):
        perm = IsActiveUser()
        request = MagicMock()
        request.user.is_authenticated = True
        request.user.is_active = False
        assert perm.has_permission(request, None) is False

    def test_unauthenticated_user_denied(self):
        perm = IsActiveUser()
        request = MagicMock()
        request.user.is_authenticated = False
        request.user.is_active = True
        assert perm.has_permission(request, None) is False

    def test_anonymous_user_denied(self):
        perm = IsActiveUser()
        request = MagicMock()
        request.user = None
        assert perm.has_permission(request, None) is False


class TestIsOwner:
    """Tests for IsOwner permission."""

    def test_owner_allowed(self):
        perm = IsOwner()
        request = MagicMock()
        user = MagicMock()
        request.user = user
        obj = MagicMock()
        obj.user = user
        assert perm.has_object_permission(request, None, obj) is True

    def test_non_owner_denied(self):
        perm = IsOwner()
        request = MagicMock()
        request.user = MagicMock()
        obj = MagicMock()
        obj.user = MagicMock()
        obj.owner = None
        assert perm.has_object_permission(request, None, obj) is False

    def test_owner_via_owner_attr(self):
        perm = IsOwner()
        request = MagicMock()
        user = MagicMock()
        request.user = user
        obj = MagicMock(spec=[])  # no .user attribute
        obj.owner = user
        assert perm.has_object_permission(request, None, obj) is True
