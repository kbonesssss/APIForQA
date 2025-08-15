from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime


class PostBase(BaseModel):
    title: str = Field(..., description="Заголовок, который никто не будет читать дальше")
    content: str = Field(..., description="Содержимое поста, полное экзистенциальной тоски")


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: UUID = Field(default_factory=uuid4)
    owner_id: UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)
    likes: int = Field(0, description="Количество людей, случайно нажавших на кнопку 'лайк'")

    class Config:
        orm_mode = True

