"""
gRPC AuthService and UserService implementations.

These servicers handle gRPC calls from the API Gateway
and other microservices.

Note: gRPC stubs (auth_pb2, auth_pb2_grpc) are generated from
protos/auth/v1/auth.proto using grpcio-tools. Until stubs are
generated, this file serves as the implementation reference.
"""

import logging
from uuid import UUID

from wordfix_shared.exceptions import (
    AuthenticationError,
    EntityAlreadyExistsError,
    EntityNotFoundError,
    ValidationError,
)

from ...application.use_cases.google_login import GoogleLoginUseCase
from ...application.use_cases.login import LoginUserUseCase
from ...application.use_cases.logout import LogoutUseCase
from ...application.use_cases.profile import (
    ChangePasswordUseCase,
    GetUserProfileUseCase,
    UpdateUserProfileUseCase,
)
from ...application.use_cases.register import RegisterUserUseCase
from ...application.use_cases.token_refresh import TokenRefreshUseCase
from ...config import settings
from ...database import async_session_factory
from ...infrastructure.google_oauth import verify_google_token
from ...infrastructure.jwt_service import JWTService
from ...infrastructure.repositories import SQLAlchemyUserRepository

logger = logging.getLogger(__name__)


def _entity_to_user_profile(entity) -> dict:
    """Convert UserEntity to gRPC UserProfile message fields."""
    return {
        "id": str(entity.id),
        "email": entity.email,
        "username": entity.username,
        "full_name": entity.full_name or "",
        "avatar": entity.avatar or "",
        "native_language": entity.native_language,
        "learning_language": entity.learning_language,
        "proficiency_level": entity.proficiency_level,
        "daily_goal": entity.daily_goal,
        "timezone": entity.timezone,
        "is_premium": entity.is_premium,
        "is_premium_active": entity.is_premium_active,
        "has_completed_onboarding": entity.has_completed_onboarding,
        "date_joined": entity.date_joined.isoformat() if entity.date_joined else "",
        "last_login": entity.last_login.isoformat() if entity.last_login else "",
    }


class AuthServiceServicer:
    """
    gRPC AuthService implementation.

    This class implements the AuthService defined in auth.proto.
    When gRPC stubs are generated, this class should inherit from
    auth_pb2_grpc.AuthServiceServicer.
    """

    def __init__(self):
        self.jwt_service = JWTService(settings.REDIS_URL)

    async def _get_repo(self, session):
        return SQLAlchemyUserRepository(session)

    async def Register(self, request, context):
        """Handle Register RPC."""
        async with async_session_factory() as session:
            try:
                repo = SQLAlchemyUserRepository(session)
                use_case = RegisterUserUseCase(repo, self.jwt_service)
                user_entity, tokens = await use_case.execute({
                    "email": request.email,
                    "username": request.username,
                    "password": request.password,
                    "full_name": request.full_name,
                    "native_language": request.native_language or "uz",
                    "learning_language": request.learning_language or "en",
                })
                await session.commit()

                return {
                    "success": True,
                    "user": _entity_to_user_profile(user_entity),
                    "tokens": {"access": tokens["access"], "refresh": tokens["refresh"]},
                    "message": "Registration successful.",
                }
            except (EntityAlreadyExistsError, ValidationError) as e:
                await session.rollback()
                return {"success": False, "message": str(e.detail)}

    async def Login(self, request, context):
        """Handle Login RPC."""
        async with async_session_factory() as session:
            try:
                repo = SQLAlchemyUserRepository(session)
                use_case = LoginUserUseCase(repo, self.jwt_service)
                user_entity, tokens = await use_case.execute(
                    email=request.email,
                    password=request.password,
                )
                await session.commit()

                return {
                    "success": True,
                    "user": _entity_to_user_profile(user_entity),
                    "tokens": {"access": tokens["access"], "refresh": tokens["refresh"]},
                    "message": "Login successful.",
                }
            except AuthenticationError as e:
                return {"success": False, "message": str(e.detail)}

    async def GoogleLogin(self, request, context):
        """Handle GoogleLogin RPC."""
        client_id = settings.GOOGLE_CLIENT_ID
        if not client_id:
            return {"success": False, "message": "Google OAuth is not configured."}

        token = request.access_token or request.id_token
        google_info = await verify_google_token(token, client_id)
        if not google_info:
            return {"success": False, "message": "Invalid Google token."}

        async with async_session_factory() as session:
            try:
                repo = SQLAlchemyUserRepository(session)
                use_case = GoogleLoginUseCase(repo, self.jwt_service)
                user_entity, tokens, is_new_user = await use_case.execute(google_info)
                await session.commit()

                return {
                    "success": True,
                    "user": _entity_to_user_profile(user_entity),
                    "tokens": {"access": tokens["access"], "refresh": tokens["refresh"]},
                    "is_new_user": is_new_user,
                    "message": "Google login successful.",
                }
            except Exception as e:
                await session.rollback()
                return {"success": False, "message": str(e)}

    async def Logout(self, request, context):
        """Handle Logout RPC."""
        try:
            use_case = LogoutUseCase(self.jwt_service)
            await use_case.execute(request.refresh_token)
            return {"success": True, "message": "Logout successful."}
        except ValidationError as e:
            return {"success": False, "message": str(e.detail)}

    async def RefreshToken(self, request, context):
        """Handle RefreshToken RPC."""
        try:
            use_case = TokenRefreshUseCase(self.jwt_service)
            new_access = await use_case.execute(request.refresh_token)
            return {"success": True, "access": new_access, "message": "Token refreshed."}
        except AuthenticationError as e:
            return {"success": False, "message": str(e.detail)}

    async def ChangePassword(self, request, context):
        """Handle ChangePassword RPC."""
        async with async_session_factory() as session:
            try:
                repo = SQLAlchemyUserRepository(session)
                use_case = ChangePasswordUseCase(repo)
                await use_case.execute(
                    user_id=UUID(request.user_id),
                    old_password=request.old_password,
                    new_password=request.new_password,
                )
                await session.commit()
                return {"success": True, "message": "Password changed successfully."}
            except ValidationError as e:
                await session.rollback()
                return {"success": False, "message": str(e.detail)}

    async def GetProviders(self, request, context):
        """Handle GetProviders RPC."""
        return {
            "success": True,
            "google_enabled": bool(settings.GOOGLE_CLIENT_ID),
            "message": "Auth providers status.",
        }


class UserServiceServicer:
    """
    gRPC UserService implementation.

    Provides user lookup and token validation for other services.
    """

    async def GetProfile(self, request, context):
        """Get user profile by user_id."""
        async with async_session_factory() as session:
            try:
                repo = SQLAlchemyUserRepository(session)
                use_case = GetUserProfileUseCase(repo)
                user_entity = await use_case.execute(UUID(request.user_id))
                return {
                    "success": True,
                    "user": _entity_to_user_profile(user_entity),
                    "message": "Profile retrieved.",
                }
            except EntityNotFoundError as e:
                return {"success": False, "message": str(e.detail)}

    async def UpdateProfile(self, request, context):
        """Update user profile."""
        async with async_session_factory() as session:
            try:
                repo = SQLAlchemyUserRepository(session)
                use_case = UpdateUserProfileUseCase(repo)
                update_data = {}
                for field in ["full_name", "native_language", "learning_language",
                             "proficiency_level", "timezone"]:
                    if request.HasField(field):
                        update_data[field] = getattr(request, field)
                if request.HasField("daily_goal"):
                    update_data["daily_goal"] = request.daily_goal

                user_entity = await use_case.execute(UUID(request.user_id), update_data)
                await session.commit()
                return {
                    "success": True,
                    "user": _entity_to_user_profile(user_entity),
                    "message": "Profile updated.",
                }
            except Exception as e:
                await session.rollback()
                return {"success": False, "message": str(e)}

    async def GetUserById(self, request, context):
        """Get user by ID (for inter-service lookups)."""
        return await self.GetProfile(request, context)

    async def ValidateToken(self, request, context):
        """Validate a JWT token and return user info."""
        jwt_service = JWTService(settings.REDIS_URL)
        try:
            payload = jwt_service.validate_token(request.access_token)
            return {
                "valid": True,
                "user_id": payload.get("user_id", ""),
                "email": payload.get("email", ""),
            }
        except Exception:
            return {"valid": False, "user_id": "", "email": ""}
