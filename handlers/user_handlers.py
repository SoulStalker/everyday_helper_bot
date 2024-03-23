from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery

from lexicon.lexicon import LEXICON_RU

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/start']
    )
