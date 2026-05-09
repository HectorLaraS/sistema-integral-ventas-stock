from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from src.domain.user import User
from src.repositories.user_psql import UserPSQL

from src.config.settings import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class AuthService:
    def __init__(self):
        self._user_repository = UserPSQL()

    def register_user(
        self,
        username: str,
        password: str,
        role: str
    ) -> User:
        existing_user = self._user_repository.get_user_by_username(username)

        if existing_user is not None:
            raise ValueError("Username already exists")

        password_hash = self.hash_password(password)

        user = User(
            username=username,
            password_hash=password_hash,
            role=role,
            is_active=True,
        )

        return self._user_repository.create_user(user)

    def login(
        self,
        username: str,
        password: str
    ) -> str:
        user = self._user_repository.get_user_by_username(username)

        if user is None:
            raise ValueError("Invalid username or password")

        if not user.is_active:
            raise ValueError("User is inactive")

        valid_password = self.verify_password(
            password,
            user.password_hash
        )

        if not valid_password:
            raise ValueError("Invalid username or password")

        token = self.create_access_token({
            "sub": user.username,
            "user_id": user.user_id,
            "role": user.role
        })

        return token
    
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(
        self,
        plain_password: str,
        password_hash: str
    ) -> bool:
        return pwd_context.verify(
            plain_password,
            password_hash
        )

    def create_access_token(
        self,
        data: dict
    ) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_EXPIRE_MINUTES
        )

        to_encode.update({
            "exp": expire
        })

        return jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )