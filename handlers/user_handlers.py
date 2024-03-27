import asyncio

from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import LEXICON_RU
from database.orm_query import get_unclosed_shifts
from services.services import shops_and_legals, bot_messages_ids

router = Router()


# Хендлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    msg = await message.answer(
        text=LEXICON_RU['/start']
    )
    bot_messages_ids.setdefault(message.chat.id, []).append(msg.message_id)
    await message.delete()


# Хендлер срабатывает на команду /unclosed и выводит список незакрытых смен
@router.message(Command('unclosed'))
async def process_unclosed_command(message: Message, session: AsyncSession, bot: Bot):
    unclosed_shifts = await get_unclosed_shifts(session)
    for shift in unclosed_shifts:
        text = (f'<b><i>Магазин № {shops_and_legals["shops"][str(shift.shopindex)]}</i></b>,\n'
                f'<i>не закрыта смена на кассе {shift.cashnum}</i>')
        msg = await message.answer(text=text)
        bot_messages_ids.setdefault(message.chat.id, []).append(msg.message_id)
    await message.delete()
    await process_do_the_chores(bot)


# функция для удаления старых сообщений
async def process_do_the_chores(bot: Bot):
    await asyncio.sleep(120)
    for chat in bot_messages_ids.keys():
        for message_id in bot_messages_ids[chat]:
            try:
                await bot.delete_message(chat_id=chat, message_id=message_id)
            except Exception as err:
                print(err)
    bot_messages_ids.clear()
