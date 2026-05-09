from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    user_id: int | None = None
    username: str | None = None
    password_hash: str | None = None
    role: str | None = None
    is_active: bool | None = None
    created_at: datetime | None = None