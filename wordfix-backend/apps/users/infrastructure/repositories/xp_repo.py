"""
XP transaction repository implementation using Django ORM.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import UUID

from django.db.models import Sum
from django.db.models.functions import TruncDate

from apps.users.infrastructure.models import XPTransaction


@dataclass
class XPTransactionEntity:
    id: UUID
    user_id: UUID
    amount: int
    reason: str
    description: str
    created_at: datetime


class DjangoXPTransactionRepository:
    """Repository for XPTransaction."""

    def create(self, user_id: UUID, amount: int, reason: str,
               description: str = "") -> XPTransactionEntity:
        t = XPTransaction.objects.create(
            user_id=user_id, amount=amount, reason=reason, description=description,
        )
        return XPTransactionEntity(
            id=t.id, user_id=t.user_id, amount=t.amount,
            reason=t.reason, description=t.description, created_at=t.created_at,
        )

    def get_daily_totals(self, user_id: UUID, days: int = 7) -> list:
        """Get daily XP totals for the last N days."""
        since = datetime.now(timezone.utc) - timedelta(days=days)
        qs = (
            XPTransaction.objects.filter(user_id=user_id, created_at__gte=since)
            .annotate(date=TruncDate("created_at"))
            .values("date")
            .annotate(total_xp=Sum("amount"))
            .order_by("date")
        )
        # Fill missing days with 0
        result = {}
        for i in range(days):
            d = (datetime.now(timezone.utc) - timedelta(days=days - 1 - i)).date()
            result[str(d)] = 0
        for row in qs:
            result[str(row["date"])] = row["total_xp"]
        return [{"date": k, "xp": v} for k, v in result.items()]
