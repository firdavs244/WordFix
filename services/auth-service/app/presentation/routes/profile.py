"""
Profile routes — GET/PATCH profile, change password.

Mirrors the monolith's profile_views.py API contract.
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Request

from wordfix_shared.exceptions import AuthenticationError
from wordfix_shared.response import build_success_response

from ...application.use_cases.profile import (
    ChangePasswordUseCase,
    GetUserProfileUseCase,
    UpdateUserProfileUseCase,
)
from ...infrastructure.repositories import SQLAlchemyUserRepository
from ..dependencies import get_repository
from ..schemas import ChangePasswordRequest, ProfileUpdateRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Profile"])


def _get_user_id(request: Request) -> UUID:
    """Extract authenticated user_id from request state."""
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise AuthenticationError("Authentication required.")
    return UUID(user_id)


@router.get("/profile/")
async def get_profile(
    request: Request,
    repo: SQLAlchemyUserRepository = Depends(get_repository),
):
    user_id = _get_user_id(request)
    use_case = GetUserProfileUseCase(repo)
    user_entity = await use_case.execute(user_id)

    return build_success_response(
        data=user_entity.to_dict(),
        message="Profile retrieved.",
    )


@router.patch("/profile/")
async def update_profile(
    request: Request,
    data: ProfileUpdateRequest,
    repo: SQLAlchemyUserRepository = Depends(get_repository),
):
    user_id = _get_user_id(request)
    use_case = UpdateUserProfileUseCase(repo)
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    user_entity = await use_case.execute(user_id, update_data)

    return build_success_response(
        data=user_entity.to_dict(),
        message="Profile updated.",
    )


@router.post("/change-password/")
async def change_password(
    request: Request,
    data: ChangePasswordRequest,
    repo: SQLAlchemyUserRepository = Depends(get_repository),
):
    user_id = _get_user_id(request)
    use_case = ChangePasswordUseCase(repo)
    await use_case.execute(
        user_id=user_id,
        old_password=data.old_password,
        new_password=data.new_password,
    )

    return build_success_response(message="Password changed successfully.")
