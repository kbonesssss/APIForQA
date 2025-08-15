from fastapi import APIRouter, HTTPException, status
from typing import List
from uuid import UUID
from ..models.post import Post, PostCreate
from .users import fake_users_db  # Импортируем нашу "базу" юзеров

router = APIRouter()

# "База данных" постов.
fake_posts_db = []


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED, summary="Выплеснуть мысль в пустоту")
async def create_post(user_id: UUID, post_in: PostCreate):
    """
    Создает новый пост от имени пользователя.
    - **user_id**: ID того, кто решил поделиться своей болью.
    - **title**: Кликбейтный заголовок.
    - **content**: Текст, который никто не дочитает до конца.
    """
    user = next((user for user in fake_users_db if user.id == user_id), None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Нельзя постить от имени несуществующего пользователя. Это уже шизофрения."
        )

    new_post = Post(title=post_in.title, content=post_in.content, owner_id=user_id)
    fake_posts_db.append(new_post)
    return new_post


@router.get("/", response_model=List[Post], summary="Посмотреть на всеобщее уныние")
async def read_posts():
    """
    Возвращает все посты. Читайте и плачьте.
    """
    if not fake_posts_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Здесь пусто. Так же, как и в душе автора этого API."
        )
    return fake_posts_db


@router.get("/{post_id}", response_model=Post, summary="Найти конкретный крик души")
async def read_post(post_id: UUID):
    """
    Ищет пост по его ID.
    """
    post = next((post for post in fake_posts_db if post.id == post_id), None)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пост не найден. Наверное, его удалили из-за чрезмерного оптимизма.")
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить чужое мнение")
async def delete_post(post_id: UUID):
    """
    Удаляет пост. Потому что можешь.
    """
    global fake_posts_db
    post_found = any(post.id == post_id for post in fake_posts_db)
    if not post_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Удалять нечего. Мир и так пуст.")

    fake_posts_db = [post for post in fake_posts_db if post.id != post_id]
    return