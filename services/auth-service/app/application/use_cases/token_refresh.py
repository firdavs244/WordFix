"""
Token refresh use case.
"""

import jwt as pyjwt

from wordfix_shared.exceptions import AuthenticationError

from ...infrastructure.jwt_service import JWTService


class TokenRefreshUseCase:
    """Refresh an access token using a valid refresh token."""

    def __init__(self, jwt_service: JWTService):
        self.jwt_service = jwt_service

    async def execute(self, refresh_token: str) -> str:
        """
        Validate refresh token and return a new access token.

        Returns: new access token string
        """
        if not refresh_token:
            raise AuthenticationError("Refresh token is required.")

        # Check blacklist
        if await self.jwt_service.is_token_blacklisted(refresh_token):
            raise AuthenticationError("Token has been revoked.")

        try:
            payload = self.jwt_service.validate_token(refresh_token)
        except pyjwt.ExpiredSignatureError:
            raise AuthenticationError("Refresh token has expired.")
        except pyjwt.InvalidTokenError:
            raise AuthenticationError("Invalid refresh token.")

        if payload.get("token_type") != "refresh":
            raise AuthenticationError("Invalid token type.")

        user_id = payload.get("user_id")
        if not user_id:
            raise AuthenticationError("Invalid token payload.")

        return self.jwt_service.generate_access_token(user_id)
