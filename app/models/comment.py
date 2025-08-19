from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class CommentBase(BaseModel):
    content: str = Field(..., description="Непрошеный совет или пассивно-агрессивное замечание")

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: UUID = Field(default_factory=uuid4)
    post_id: UUID
    owner_id: UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)