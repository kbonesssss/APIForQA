from pydantic import BaseModel, Field
from typing import List, Dict
from uuid import UUID, uuid4
from datetime import datetime
from .enums import ReactionType # <--- ДОБАВИТЬ ИМПОРТ

# Дополнительная модель для хранения реакции
class Reaction(BaseModel):
    user_id: UUID
    type: ReactionType

class PostBase(BaseModel):
    title: str = Field(..., description="Заголовок, который никто не будет читать дальше")
    content: str = Field(..., description="Содержимое поста, полное экзистенциальной тоски")

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: UUID = Field(default_factory=uuid4)
    owner_id: UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # Заменяем likes на более сложную структуру
    reactions: List[Reaction] = Field([], description="Коллекция вздохов и фейспалмов от благодарной аудитории")

    class Config:
        orm_mode = True