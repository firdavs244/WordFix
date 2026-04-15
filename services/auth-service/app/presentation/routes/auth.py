"""
Auth routes — register, login, logout, token refresh.

Mirrors the monolith's auth_views.py API contract exactly.
"""

import logging

from fastapi import APIRouter, Depends

from wordfix_shared.response import build_error_response, build_success_response

from ...application.use_cases.login import LoginUserUseCase
from ...application.use_cases.logout import LogoutUseCase
from ...application.use_cases.register import RegisterUserUseCase
from ...application.use_cases.token_refresh import TokenRefreshUseCase
from ...infrastructure.jwt_service import JWTService
from ...infrastructure.repositories import SQLAlchemyUserRepository
from ..dependencies import get_jwt_service, get_repository
from ..schemas import LoginRequest, LogoutRequest, RegisterRequest, TokenRefreshRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register/", status_code=201)
async def register(
    data: RegisterRequest,
    repo: SQLAlchemyUserRepository = Depends(get_repository),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    use_case = RegisterUserUseCase(repo, jwt_service)
    user_entity, tokens = await use_case.execute(data.model_dump())

    return build_success_response(
        data={
            "user": user_entity.to_dict(),
            "tokens": tokens,
        },
        message="Registration successful.",
    )


@router.post("/login/")
async def login(
    data: LoginRequest,
    repo: SQLAlchemyUserRepository = Depends(get_repository),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    use_case = LoginUserUseCase(repo, jwt_service)
    user_entity, tokens = await use_case.execute(
        email=data.email,
        password=data.password,
    )

    return build_success_response(
        data={
            "user": user_entity.to_dict(),
            "tokens": tokens,
        },
        message="Login successful.",
    )


@router.post("/logout/")
async def logout(
    data: LogoutRequest,
    jwt_service: JWTService = Depends(get_jwt_service),
):
    use_case = LogoutUseCase(jwt_service)
    await use_case.execute(data.refresh)
    return build_success_response(message="Logout successful.")


@router.post("/token/refresh/")
async def token_refresh(
    data: TokenRefreshRequest,
    jwt_service: JWTService = Depends(get_jwt_service),
):
    use_case = TokenRefreshUseCase(jwt_service)
    new_access = await use_case.execute(data.refresh)

    return build_success_response(
        data={"access": new_access},
        message="Token refreshed.",
    )
