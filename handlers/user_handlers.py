from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import LEXICON_RU
from database.orm_query import get_unclosed_shifts

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/start']
    )


@router.message(Command('unclosed'))
async def process_unclosed_command(message: Message, session: AsyncSession):
    unclosed_shifts = await get_unclosed_shifts(session)
    for shift in unclosed_shifts:
        print(shift.shopindex, shift.cashnum, shift.operday)
        await message.answer(text=f'Магазин № {shift.shopindex}, касса № {shift.cashnum}, дата смены {shift.operday}')
