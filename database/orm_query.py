from datetime import date, timedelta
from typing import Any, Sequence

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from database.op_models import Shifts
from database.models import User, Settings


# # Функция возвращает пользователя по его telegram ID
# async def orm_get_user_by_id(session: AsyncSession, user_id: int) -> User:
#     query = select(User).where(User.username == user_id)
#     users = await session.execute(query)
#     user = users.scalars().first()
#     return user


# Функция получает список незакрытых смен за текущий день
async def get_unclosed_shifts(session: AsyncSession) -> Sequence[Row[Any] | RowMapping | Any]:
    query = select(Shifts).where(
        (Shifts.operday >= date.today() - timedelta(days=1)) & (Shifts.state == 0))
    shifts = await session.execute(query)
    shifts = shifts.scalars().all()
    return shifts
