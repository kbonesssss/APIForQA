from fastapi import APIRouter
from pydantic import BaseModel
from collections import Counter

# Импортируем "базы данных" напрямую
from .posts import fake_posts_db
from .users import fake_users_db
from .comments import fake_comments_db

router = APIRouter()


class UselessStats(BaseModel):
    total_users: int
    total_posts: int
    total_comments: int
    most_common_reaction: str
    most_active_procrastinator: str
    average_comments_per_post: float


@router.get("/", response_model=UselessStats, summary="Получить бесполезную, но красивую статистику")
def get_stats():
    """
    Собирает и вычисляет метрики, которые ничего не значат,
    но могут впечатлить на совещании.
    """
    total_users = len(fake_users_db)
    total_posts = len(fake_posts_db)
    total_comments = len(fake_comments_db)

    # Самая частая реакция
    all_reactions = [r.type.value for post in fake_posts_db for r in post.reactions]
    most_common_reaction = "N/A"
    if all_reactions:
        most_common_reaction = Counter(all_reactions).most_common(1)[0][0]

    # Самый активный "прокрастинатор" (по числу постов и комментов)
    activity = Counter()
    for post in fake_posts_db:
        activity[post.owner_id] += 1
    for comment in fake_comments_db:
        activity[comment.owner_id] += 1

    most_active_user_id = None
    if activity:
        most_active_user_id = activity.most_common(1)[0][0]

    most_active_procrastinator = "N/A"
    if most_active_user_id:
        user = next((u for u in fake_users_db if u.id == most_active_user_id), None)
        if user:
            most_active_procrastinator = user.username

    # Среднее число комментов на пост
    average_comments_per_post = 0
    if total_posts > 0:
        average_comments_per_post = round(total_comments / total_posts, 2)

    return UselessStats(
        total_users=total_users,
        total_posts=total_posts,
        total_comments=total_comments,
        most_common_reaction=most_common_reaction,
        most_active_procrastinator=most_active_procrastinator,
        average_comments_per_post=average_comments_per_post
    )