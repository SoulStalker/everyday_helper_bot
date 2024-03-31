from collections import defaultdict
from datetime import date, timedelta
from typing import Any, Sequence

from sqlalchemy import select, Row, RowMapping, func, case, not_
from sqlalchemy.ext.asyncio import AsyncSession

from database.op_models import Shifts, Purchases
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
        (Shifts.operday >= date.today() - timedelta(days=1)) & (Shifts.state == 0)).order_by(Shifts.shopindex)
    shifts = await session.execute(query)
    shifts = shifts.scalars().all()
    return shifts


# Функция получает список смен с результатами продаж
async def get_results_by_shop(session: AsyncSession):
    results_today = []

    async with session as async_session:
        stmt = select(Shifts.shopindex, Shifts.cashnum, Shifts.numshift, Shifts.operday, Shifts.state, Shifts.inn,
                      func.count(case((Purchases.cash_operation == 0, Purchases.checksumstart), else_=None)).label('check_count'),
                      func.sum(case((Purchases.operationtype, Purchases.checksumend), (~Purchases.operationtype, -Purchases.checksumend),
                                    else_=None)).label('sum_by_checks'))

        stmt = stmt.join(Purchases).filter(Shifts.operday == date.today(), Purchases.checkstatus == 0)
        stmt = stmt.group_by(Shifts.cashnum, Shifts.shopindex, Shifts.numshift, Shifts.operday, Shifts.state, Shifts.inn)
        stmt = stmt.order_by(Shifts.shopindex, Shifts.cashnum)
        result = await async_session.execute(stmt)

        rows = result.fetchall()
        # print(rows)
        for row in rows:
            shift = {
                'shop_index': row[0],
                'cash_num': row[1],
                'num_shift': row[2],
                'operation_day': row[3],
                'state': row[4],
                'inn': row[5],
                'checks_count': row[6],
                'sum_by_checks': row[7],
            }
            results_today.append(shift)

        combined_dict = defaultdict(lambda: {'sum_by_checks': 0, 'checks_count': 0, 'state': set()})

        for shift in results_today:  # Предположим, что у вас есть список shifts, содержащий словари shift
            shop_index = shift['shop_index']
            combined_dict[shop_index]['sum_by_checks'] += shift['sum_by_checks']
            combined_dict[shop_index]['checks_count'] += shift['checks_count']
            combined_dict[shop_index]['state'].add(shift['state'])

        # Преобразование defaultdict в обычный словарь
        combined_dict = dict(combined_dict)
    print(combined_dict)
    return results_today


