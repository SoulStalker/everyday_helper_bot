import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs

from config_data.config import load_config
from handlers.user_handlers import start_dialog
from keyboards.set_menu import set_main_menu
from handlers import other_handlers, user_handlers
from database.engine import op_session_maker
from middlewares.outer import DbMiddleware, ShadowBanMiddleware


async def main():
    config = load_config('.env')
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    # Настраиваем меню бота
    await set_main_menu(bot)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)
    dp.include_router(start_dialog)
    setup_dialogs(dp)

    # Подключается мидлваря для блокировки всех кроме админа
    dp.update.middleware(ShadowBanMiddleware(config.tg_bot.admin_ids))
    # Мидлваря для подключения базы данных
    dp.update.middleware(DbMiddleware(session_pool=op_session_maker))
    
    # Удаляем необработанные обновления
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
