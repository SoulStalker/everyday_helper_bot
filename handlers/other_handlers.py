from aiogram import Router
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON_RU


router = Router()


# Этот хендлер срабатывает на сообщение которые не попали в другие хендлеры
@router.message()
async def send_message(message: Message):
    await message.answer(text=LEXICON_RU['other_answer'])


# Этот хендлер срабатывает на колбеки которые не попали в другие хендлеры
@router.callback_query()
async def callback_query(callback: CallbackQuery):
    text = callback.data
    await callback.message.answer(f"{text}")
