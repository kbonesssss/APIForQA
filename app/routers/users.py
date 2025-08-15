from fastapi import APIRouter, HTTPException, status
from typing import List
from uuid import UUID
from ..models.user import User, UserCreate

router = APIRouter()

# "База данных" пользователей. В реальном мире здесь был бы коннект к БД.
# Для обучения — сойдет и так.
fake_users_db = []


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED, summary="Создать нового бедолагу")
async def create_user(user_in: UserCreate):
    """
    Регистрирует нового пользователя в системе.
    - **username**: Имя, которое скоро станет частью статистики.
    - **email**: Адрес для получения рекламы казино.
    - **password**: Секретная комбинация, известная вашему провайдеру.
    """
    if any(u.email == user_in.email for u in fake_users_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Эта почта уже занята кем-то более удачливым."
        )

    new_user = User(username=user_in.username, email=user_in.email)
    fake_users_db.append(new_user)
    return new_user


@router.get("/", response_model=List[User], summary="Получить список всех, кто попался")
async def read_users():
    """
    Возвращает список всех зарегистрированных пользователей.
    Идеально для спам-рассылок.
    """
    if not fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Никто еще не совершил ошибку и не зарегистрировался. База пуста, как и наши надежды."
        )
    return fake_users_db


@router.get("/{user_id}", response_model=User, summary="Найти конкретного страдальца")
async def read_user(user_id: UUID):
    """
    Ищет пользователя по его уникальному ID.
    Если не найден — значит, ему повезло.
    """
    user = next((user for user in fake_users_db if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пользователь не найден. Возможно, он обрёл свободу.")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Стереть из бытия")
async def delete_user(user_id: UUID):
    """
    Удаляет пользователя. Навсегда. Без права на восстановление.
    Как твой первый коммит в master.
    """
    global fake_users_db
    user_found = any(user.id == user_id for user in fake_users_db)
    if not user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Нельзя удалить того, кого не существует. Философия, однако.")

    fake_users_db = [user for user in fake_users_db if user.id != user_id]
    return