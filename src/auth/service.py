from sqlalchemy import select

from src.auth.models import User
from src.database import async_session_maker
from src.service.base import BaseService


class UserService(BaseService):
    model = User

    @classmethod
    async def find_user_by_id(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(
                User.id,
                User.email,
                User.is_active,
                User.is_superuser,
                User.is_verified,
                User.created_at
            ).filter_by(id=user_id)
            result = await session.execute(query)
            return result.mappings().one()
