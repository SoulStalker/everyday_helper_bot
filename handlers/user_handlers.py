import asyncio
import datetime

from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, User
from aiogram_dialog import DialogManager, Dialog, Window, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import LEXICON_RU
from database.orm_query import get_unclosed_shifts, get_results_by_shop
from services.services import shops_and_legals, bot_messages_ids

router = Router()


async def button_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.message.answer('Кажется, ты нажал на кнопку!')


class StartSG(StatesGroup):
    start = State()


# Это хэндлер, обрабатывающий нажатие инлайн-кнопок
async def button_clicked_2(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    another_button = dialog_manager.dialog_data.get('another_button')
    dialog_manager.dialog_data.update(another_button=not another_button)


# Это геттер
async def get_button_status(dialog_manager: DialogManager, **kwargs):
    another_button = dialog_manager.dialog_data.get('another_button')
    return {'button_status': another_button}


start_dialog = Dialog(
    Window(
        Const('На кнопки из этого сообщения можно нажать!'),
        Button(
            text=Const('Нажми меня!'),
            id='button_1',
            on_click=button_clicked_2),
        Button(
            text=Const('И меня нажми!'),
            id='button_2',
            on_click=button_clicked_2,
            when='button_status'),
        state=StartSG.start,
        getter=get_button_status,
    ),
)


# Это геттер
async def get_button_status(dialog_manager: DialogManager, **kwargs):
    another_button = dialog_manager.dialog_data.get('another_button')
    return {'button_status': another_button}


@router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


# Хендлер срабатывает на команду /unclosed и выводит список незакрытых смен
@router.message(Command('unclosed'))
async def process_unclosed_command(message: Message, session: AsyncSession, bot: Bot):
    unclosed_shifts = await get_unclosed_shifts(session)
    if not unclosed_shifts:
        msg = await message.answer(text=LEXICON_RU['no_unclosed'])
        bot_messages_ids.setdefault(message.chat.id, []).append(msg.message_id)
    if len(unclosed_shifts) > 20:
        msg = await message.answer(LEXICON_RU['too_many'])
        bot_messages_ids.setdefault(message.chat.id, []).append(msg.message_id)
    else:
        for shift in unclosed_shifts:
            try:
                text = (f'<b><i>{shops_and_legals["shops"][str(shift.shopindex)]}</i></b>,\n'
                        f'<i>не закрыта смена на кассе {shift.cashnum} фирма {shops_and_legals["legals"][shift.inn]}</i>')
                msg = await message.answer(text=text)
                bot_messages_ids.setdefault(message.chat.id, []).append(msg.message_id)

            except Exception as err:
                await asyncio.sleep(1)
                print(err)
    bot_messages_ids.setdefault(message.chat.id, []).append(message.message_id)


# Хендлер срабатывает на команду /unclosed_list и выводит список незакрытых смен
@router.message(Command('unclosed_list'))
async def process_unclosed_list_command(message: Message, session: AsyncSession, bot: Bot):
    unclosed_shifts = await get_unclosed_shifts(session)
    if not unclosed_shifts:
        msg = await message.answer(text=LEXICON_RU['no_unclosed'])
        bot_messages_ids.setdefault(message.chat.id, []).append(msg.message_id)
    else:
        text = ''
        for shift in unclosed_shifts:
            text += (f'<code>{shops_and_legals["shops"][str(shift.shopindex)]} на кассе {shift.cashnum} фирма'
                     f' {shops_and_legals["legals"][shift.inn]}</code>\n')
        try:
            print(text)
            msg = await message.answer(text=text)
            bot_messages_ids.setdefault(message.chat.id, []).append(msg.message_id)
        except Exception as err:
            await asyncio.sleep(1)
            print(err)
            await message.answer(text=LEXICON_RU['too_long'])
    bot_messages_ids.setdefault(message.chat.id, []).append(message.message_id)


# Хендлер срабатывает на команду /results_by_shop и выводит результаты продаж по магазинам
@router.message(Command('results_by_shop'))
async def process_results_by_shop_command(message: Message, session: AsyncSession, bot: Bot):
    shifts = await get_results_by_shop(session)
    if not shifts:
        msg = await message.answer(text=LEXICON_RU['no_results'])
        bot_messages_ids.setdefault(message.chat.id, []).append(msg.message_id)
    for shop_index, data in shifts.items():
        if shop_index != 'total_summary':
            text = (f"Отчет за {datetime.date.today().strftime('%d.%m.%y')} {shops_and_legals['shops'][str(shop_index)]}:\n"
                    f"Чеки: {data['checks_count']} шт.\n"
                    f"Оборот: {data['sum_by_checks']:,.0f} руб.".replace(',', ' '))
        else:
            text = (f"<strong>Суммарный отчет за {datetime.date.today().strftime('%d.%m.%y')}:</strong>\n"
                    f"<strong>Чеки: {data['checks_count']} шт.</strong>\n"
                    f"<strong>Оборот: {data['sum_by_checks']:,.0f} руб.</strong>".replace(',', ' '))
        if 0 in data['state']:
            text += LEXICON_RU['open_state']
        try:
            print(text)
            msg = await message.answer(text=text)
            bot_messages_ids.setdefault(message.chat.id, []).append(msg.message_id)
        except Exception as err:
            await asyncio.sleep(1)
            print("Error:", err)
    await message.delete()


# Хендлер срабатывает на команду /total и выводит итоговые результаты дня
@router.message(Command('total'))
async def process_total_command(message: Message, session: AsyncSession, bot: Bot):
    shifts = await get_results_by_shop(session)
    if not shifts:
        msg = await message.answer(text=LEXICON_RU['no_results'])
        bot_messages_ids.setdefault(message.chat.id, []).append(msg.message_id)
    data = shifts['total_summary']
    text = (f"<strong>Суммарный отчет за {datetime.date.today().strftime('%d.%m.%y')}:</strong>\n"
            f"<strong>Чеки: {data['checks_count']} шт.</strong>\n"
            f"<strong>Оборот: {data['sum_by_checks']:,.0f} руб.</strong>".replace(',', ' '))
    if 0 in data['state']:
        text += LEXICON_RU['open_state']
    try:
        await message.answer(text=text)
    except Exception as err:
        await asyncio.sleep(1)
        print("Error:", err)
    await message.delete()