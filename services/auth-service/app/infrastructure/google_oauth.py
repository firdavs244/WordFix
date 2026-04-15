"""
Google OAuth token verification.

Port of GoogleLoginView._verify_google_token from the monolith.
"""

import logging

import httpx

logger = logging.getLogger(__name__)


async def verify_google_token(token: str, client_id: str) -> dict | None:
    """
    Verify a Google OAuth token and return user info.

    Tries userinfo endpoint (access_token), then tokeninfo (id_token).

    Returns:
        {"email": ..., "name": ..., "google_id": ...} or None
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Try userinfo endpoint with access_token
        try:
            resp = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {token}"},
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("email"):
                    return {
                        "email": data["email"],
                        "name": data.get("name", ""),
                        "google_id": data.get("sub", ""),
                    }
        except Exception:
            logger.debug("Google userinfo endpoint failed")

        # Try tokeninfo endpoint for id_token
        try:
            resp = await client.get(
                f"https://oauth2.googleapis.com/tokeninfo?id_token={token}",
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("email") and data.get("aud") == client_id:
                    return {
                        "email": data["email"],
                        "name": data.get("name", ""),
                        "google_id": data.get("sub", ""),
                    }
        except Exception:
            logger.debug("Google tokeninfo endpoint failed")

    return None
