import logging
from datetime import datetime, timedelta
from aiogram import Bot
from database.models import database



async def check_today_reminders(bot: Bot):

    try:
        today = datetime.now().strftime("%d.%m")
        today_reminders = database.get_today_reminders(today)
        for user_id, name, message in today_reminders:
            try:
                await bot.send_message(
                    user_id,
                    f"🎉 Нагадування про день народження! 🎉\n\n"
                    f"Сьогодні день народження у {name}!\n"
                    f"Твоє привітання або повідомлення: {message}",
                    parse_mode="HTML"
                )
            except Exception as e:
                logging.error(f"Failed to send birthday reminder to {user_id}: {e}")
    except Exception as e:
        logging.error(f"Error fetching today's reminders: {e}")

async def check_early_reminders(bot:Bot):

    try:
        today = datetime.now().strftime("%d.%m")
        early_reminders = database.get_early_reminders(today)

        for user_id, name, message, days_before in early_reminders:
            try:
                await bot.send_message(
                    user_id,
                    f"🎁 Завчасне нагадування про день народження! 🎁\n\n"
                    f"У {name} день народження через {days_before} дні!\n"
                    f"Не забудь привітати!\n"
                    f"Твоє привітання або повідомлення: {message}",
                    parse_mode="HTML"
                )
            except Exception as e:
                logging.error(f"Failed to send early reminder to {user_id}: {e}")
    except Exception as e:
        logging.error(f"Error fetching early reminders: {e}")

async def check_reminders(bot:Bot):
    await check_today_reminders(bot)
    await check_early_reminders(bot)
