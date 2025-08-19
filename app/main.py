from fastapi import FastAPI
from .routers import users, posts, comments, stats

app = FastAPI(
    title="Cynical Circle API",
    description="Тестовый API для тех, кто понял жизнь. Здесь можно создавать бессмысленных пользователей и писать тленные посты.",
    version="0.0.1",
    contact={
        "name": "Ваш покорный слуга",
        "url": "https://github.com/kbonesssss", # Замени на свой GitHub
    },
    license_info={
        "name": "Лицензия 'Делай что хочешь'",
        "url": "https://choosealicense.com/licenses/unlicense/",
    },
)

# Подключаем роутеры
app.include_router(users.router, prefix="/users", tags=["Пользователи"])
app.include_router(posts.router, prefix="/posts", tags=["Посты"])
app.include_router(comments.router, prefix="/posts/{post_id}/comments", tags=["Комментарии"])
app.include_router(stats.router, prefix="/stats", tags=["Статистика"])

@app.get("/", summary="Проверка пульса")
async def root():
    """
    Корневой эндпоинт. Если он отвечает, значит, сервер еще не сдался.
    """
    return {"message": "Сервер работает, но энтузиазма в этом мало."}