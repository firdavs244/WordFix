"""
Abstract base model for all WordFix models.

Provides common fields: id (UUID), created_at, updated_at, is_active.
"""

import uuid

from django.db import models


class AbstractBaseModel(models.Model):
    """
    Abstract base model that provides common fields for all models.

    Fields:
        id: UUID primary key (auto-generated).
        created_at: Timestamp when the record was created.
        updated_at: Timestamp when the record was last updated.
        is_active: Soft-delete flag.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def soft_delete(self) -> None:
        """Soft delete the record by setting is_active to False."""
        self.is_active = False
        self.save(update_fields=["is_active", "updated_at"])

    def restore(self) -> None:
        """Restore a soft-deleted record."""
        self.is_active = True
        self.save(update_fields=["is_active", "updated_at"])
