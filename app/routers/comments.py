from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from uuid import UUID
from ..models.comment import Comment, CommentCreate
from .users import fake_users_db
from .posts import fake_posts_db

router = APIRouter()

# "База данных" комментариев
fake_comments_db: List[Comment] = []


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED, summary="Вставить свои пять копеек")
def create_comment_for_post(post_id: UUID, user_id: UUID, comment_in: CommentCreate):
    """
    Добавляет комментарий к посту от имени пользователя.
    Требует существования и поста, и пользователя. Иначе какой в этом смысл?
    """
    post_exists = any(p.id == post_id for p in fake_posts_db)
    if not post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пост не найден. Мысль потеряна, как и все наши мечты.")

    user_exists = any(u.id == user_id for u in fake_users_db)
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пользователь не найден. Нельзя комментировать из небытия.")

    new_comment = Comment(**comment_in.dict(), post_id=post_id, owner_id=user_id)
    fake_comments_db.append(new_comment)
    return new_comment


@router.get("/", response_model=List[Comment], summary="Прочитать все мнения (на свой страх и риск)")
def get_comments_for_post(post_id: UUID):
    """
    Возвращает список всех комментариев для конкретного поста.
    """
    post_exists = any(p.id == post_id for p in fake_posts_db)
    if not post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пост не существует, как и объективность.")

    comments = [c for c in fake_comments_db if c.post_id == post_id]
    if not comments:
        return []
    return comments