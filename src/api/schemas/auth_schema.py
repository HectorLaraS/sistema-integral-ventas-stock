from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    username: str
    password: str
    role: str = "operator"


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    user_id: int
    username: str
    role: str
    is_active: bool