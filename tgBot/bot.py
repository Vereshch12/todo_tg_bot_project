import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from handlers import router as main_router
from task_handlers import router as task_router
from dialogs import task_dialog

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting bot...")
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(main_router)
    dp.include_router(task_router)
    dp.include_router(task_dialog)

    setup_dialogs(dp)

    logger.info("Bot is running and polling for updates...")
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
        logger.info("Bot stopped.")

if __name__ == "__main__":
    asyncio.run(main())