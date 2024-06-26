from aiogram import Router
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON_RU


router = Router()


# Этот хендлер срабатывает на сообщение которые не попали в другие хендлеры
@router.message()
async def send_message(message: Message):
    # отключил потому что в группе реагирует на каждое сообщение
    pass
    # await message.answer(text=LEXICON_RU['other_answer'])


# Этот хендлер срабатывает на колбеки которые не попали в другие хендлеры
@router.callback_query()
async def callback_query(callback: CallbackQuery):
    # отключил потому что в группе реагирует на каждое сообщение
    pass
    # text = callback.data
    # await callback.message.answer(f"{text}")
