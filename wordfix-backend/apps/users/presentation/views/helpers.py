"""
Helper utilities shared across user views.
"""

from dataclasses import asdict


def _user_entity_to_dict(entity) -> dict:
    """Convert UserEntity dataclass to serializable dict."""
    data = asdict(entity)
    data["id"] = str(data["id"])
    if data.get("date_joined"):
        data["date_joined"] = entity.date_joined.isoformat() if entity.date_joined else None
    if data.get("last_login"):
        data["last_login"] = entity.last_login.isoformat() if entity.last_login else None
    if data.get("premium_until"):
        data["premium_until"] = entity.premium_until.isoformat() if entity.premium_until else None
    data["is_premium_active"] = entity.is_premium_active
    # Remove sensitive fields
    data.pop("is_staff", None)
    return data
