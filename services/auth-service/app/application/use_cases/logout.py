"""
Logout use case — blacklist refresh token.
"""

import jwt as pyjwt

from wordfix_shared.exceptions import ValidationError

from ...infrastructure.jwt_service import JWTService


class LogoutUseCase:
    """Blacklist a refresh token."""

    def __init__(self, jwt_service: JWTService):
        self.jwt_service = jwt_service

    async def execute(self, refresh_token: str) -> None:
        if not refresh_token:
            raise ValidationError("Refresh token is required.")

        try:
            payload = self.jwt_service.validate_token(refresh_token)
            if payload.get("token_type") != "refresh":
                raise ValidationError("Invalid token type.")
        except pyjwt.ExpiredSignatureError:
            # Expired tokens don't need blacklisting
            return
        except pyjwt.InvalidTokenError:
            raise ValidationError("Invalid or expired token.")

        await self.jwt_service.blacklist_refresh_token(refresh_token)
