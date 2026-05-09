from fastapi import APIRouter, HTTPException, Depends
from src.services.auth_service import AuthService
from src.api.schemas.auth_schema import (
    UserCreateRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
)
from src.domain.user import User
from src.api.dependencies.security import get_current_user, require_admin, require_operator_or_admin


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", response_model=UserResponse)
def register_user(request: UserCreateRequest, current_user: User = Depends(require_admin)):
    service = AuthService()

    try:
        user = service.register_user(
            username=request.username,
            password=request.password,
            role=request.role,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return UserResponse(
        user_id=user.user_id,
        username=user.username,
        role=user.role,
        is_active=user.is_active,
    )


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    service = AuthService()

    try:
        token = service.login(
            username=request.username,
            password=request.password
        )
    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )

    return TokenResponse(
        access_token=token,
        token_type="bearer"
    )

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        user_id=current_user.user_id,
        username=current_user.username,
        role=current_user.role,
        is_active=current_user.is_active,
    )