"""
Google OAuth routes.

Mirrors the monolith's GoogleLoginView and GoogleAuthStatusView.
"""

import logging

from fastapi import APIRouter, Depends

from wordfix_shared.response import build_error_response, build_success_response

from ...application.use_cases.google_login import GoogleLoginUseCase
from ...config import settings
from ...infrastructure.google_oauth import verify_google_token
from ...infrastructure.jwt_service import JWTService
from ...infrastructure.repositories import SQLAlchemyUserRepository
from ..dependencies import get_jwt_service, get_repository
from ..schemas import GoogleLoginRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Google OAuth"])


@router.post("/google/")
async def google_login(
    data: GoogleLoginRequest,
    repo: SQLAlchemyUserRepository = Depends(get_repository),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    client_id = settings.GOOGLE_CLIENT_ID
    if not client_id:
        return build_error_response(message="Google OAuth is not configured.")

    # Verify token with Google
    token = data.access_token or data.id_token
    google_user_info = await verify_google_token(token, client_id)
    if not google_user_info:
        return build_error_response(message="Invalid Google token.")

    use_case = GoogleLoginUseCase(repo, jwt_service)
    user_entity, tokens, is_new_user = await use_case.execute(google_user_info)

    return build_success_response(
        data={
            "user": user_entity.to_dict(),
            "tokens": tokens,
            "is_new_user": is_new_user,
        },
        message="Google login successful.",
    )


@router.get("/providers/")
async def providers_status():
    is_configured = bool(settings.GOOGLE_CLIENT_ID)
    return build_success_response(
        data={"google_enabled": is_configured},
        message="Auth providers status.",
    )
