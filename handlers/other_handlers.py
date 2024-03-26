from aiogram import Router
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON_RU
from services.services import messages


router = Router()


# Этот хендлер срабатывает на сообщение которые не попали в другие хендлеры
@router.message()
async def send_message(message: Message):
    msg = await message.answer(text=LEXICON_RU['other_answer'])
    messages.setdefault(message.chat.id, []).append(msg.message_id)
    await message.delete()


# Этот хендлер срабатывает на колбеки которые на поапали в другие хендлеры
@router.callback_query()
async def callback_query(callback: CallbackQuery):
    text = callback.data
    await callback.message.answer(f"{text}")
