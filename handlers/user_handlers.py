from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import LEXICON_RU
from database.orm_query import get_unclosed_shifts
from services.services import shops_and_legals

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
        text = f'Магазин № {shops_and_legals["shops"][str(shift.shopindex)]}, не закрыта смена на кассе {shift.cashnum}'
        await message.answer(text=text)
