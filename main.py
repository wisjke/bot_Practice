import asyncio
import os

from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.storage.memory import MemoryStorage
from database.models import database
from handlers import common, reminder
from utils.scheduler import check_reminders
from utils.commands import set_bot_commands


async def main() -> None:
    load_dotenv('.env')
    token = os.getenv('TOKEN_API')

    # bot
    bot = Bot(token=token)

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    scheduler = AsyncIOScheduler()
    database.create_tables()

    # register handlers
    dp.include_router(common.router)
    dp.include_router(reminder.router)

    # schedule the reminder check job
    trigger = CronTrigger(hour=15, minute=35)
    scheduler.add_job(check_reminders, trigger=trigger, args=[bot])
    scheduler.start()

    try:
        # Start polling
        await bot.delete_webhook(drop_pending_updates=True)
        await set_bot_commands(bot)
        await dp.start_polling(bot)
    finally:
        # Shut down properly
        await bot.session.close()
        scheduler.shutdown()


if __name__ == '__main__':
    asyncio.run(main())
