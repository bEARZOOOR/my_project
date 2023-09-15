import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import user_handlers, other_handlers
from keyboards.main_menu import set_main_menu
from database.database import DatabaseManager

logger = logging.getLogger(__name__)



async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s"
    )
 
    logger.info("Starting bot..")
 
    config: Config = load_config()

    storage: MemoryStorage = MemoryStorage()

    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode="html")
    dp: Dispatcher = Dispatcher(storage=storage)

    db_manager: DatabaseManager = DatabaseManager()

    await db_manager.create_table()
    await set_main_menu(bot)
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot,
                           allowed_updates=[])
    

if __name__ == "__main__":
    asyncio.run(main())
