import asyncio

from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import LEXICON_RU
from database.orm_query import get_unclosed_shifts, get_results_by_shop
from services.services import shops_and_legals, bot_messages_ids

router = Router()


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
    if not unclosed_shifts:
        msg = await message.answer(text=LEXICON_RU['no_unclosed'])
    for shift in unclosed_shifts:
        try:
            text = (f'<b><i>{shops_and_legals["shops"][str(shift.shopindex)]}</i></b>,\n'
                    f'<i>не закрыта смена на кассе {shift.cashnum}</i>')
            msg = await message.answer(text=text)
            bot_messages_ids.setdefault(message.chat.id, []).append(msg.message_id)
        except Exception as err:
            await asyncio.sleep(1)
            print(err)
    # await message.delete()
    await process_do_the_chores(bot)


# Хендлер срабатывает на команду /results_by_shop и выводит список незакрытых смен
@router.message(Command('results_by_shop'))
async def process_results_by_shop_command(message: Message, session: AsyncSession, bot: Bot):
    shifts = await get_results_by_shop(session)
    if not shifts:
        msg = await message.answer(text=LEXICON_RU['no_unclosed'])
        bot_messages_ids.setdefault(message.chat.id, []).append(msg.message_id)
    # for shift in shifts:
    #     print(shift['shop_index'], shift['cash_num'], shift['num_shift'], shift['operation_day'], shift['state'],
    #           shift['inn'], shift['checks_count'], shift['sum_by_checks'])
        # text = (f"Отчет за сегодня {shops_and_legals['shops'][str(shift['shop_index'])]}:\n"
        #         f"Чеки: {shift['checks_count']}\n"
        #         f"Оборот: {shift['sum_by_checks']} руб.\n")
        # try:
        #     print(text)
        #     msg = await message.answer(text=text)
        #     bot_messages_ids.setdefault(message.chat.id, []).append(msg.message_id)
        # except Exception as err:
        #     await asyncio.sleep(1)
        #     print("Error:", err)
    await message.delete()
    await process_do_the_chores(bot)


