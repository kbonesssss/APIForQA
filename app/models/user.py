from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID, uuid4
from .enums import UserStatus

class UserBase(BaseModel):
    username: str = Field(..., description="Имя пользователя, которое он забудет через неделю")
    email: str = Field(..., description="Почта для спама и уведомлений, которые никто не читает")

class UserCreate(UserBase):
    password: str = Field(..., description="Пароль, который легко угадать. Например, '123456'")

class User(UserBase):
    id: UUID = Field(default_factory=uuid4, description="Уникальный идентификатор, доказывающий, что ты не просто набор данных")
    is_active: bool = Field(True, description="Активен ли пользователь или просто занимает место в базе данных")
    status: Optional[UserStatus] = Field(None, description="Текущее экзистенциальное состояние") # <--- НОВОЕ ПОЛЕ

    class Config:
        orm_mode = True
        # Этот параметр убран, так как orm_mode уже устарел в Pydantic v2.
        # Вместо него используется from_attributes = True, но для наших целей это не критично.