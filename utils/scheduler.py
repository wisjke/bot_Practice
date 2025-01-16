from datetime import datetime
from aiogram import Bot
from database.models import Database
from apscheduler.triggers.cron import CronTrigger
import asyncio


db = Database()


async def check_reminders(bot: Bot):
    today = datetime.now().strftime("%d.%m")
    reminders = db.get_today_reminders(today)

    for user_id, name, message in reminders:
        await bot.send_message(
            user_id,
            f"🎉 Birthday Reminder! 🎉\n\n"
            f"Today is {name}'s birthday!\n"
            f"Message: {message}",
            parse_mode="HTML"
        )
