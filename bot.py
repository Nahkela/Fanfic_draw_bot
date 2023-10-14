from aiogram import Bot, Dispatcher
import asyncio
from config.config import load_config, Config
from handlers import register_handlers, other_handlers, start_handlers, drawing_handlers
from menu.menu import set_main_menu


async def main():
    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=config.database.storage)

    await set_main_menu(bot)

    dp.include_router(start_handlers.router)
    dp.include_router(register_handlers.router)
    dp.include_router(drawing_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
