import logging
from datetime import datetime, timedelta
from aiogram import Bot
from database.models import db



async def check_reminders(bot: Bot):
    today = datetime.now().strftime("%d.%m")

    try:
        today_reminders = db.get_today_reminders(today)
        for user_id, name, message in today_reminders:
            try:
                await bot.send_message(
                    user_id,
                    f"🎉 Birthday Reminder! 🎉\n\n"
                    f"Today is {name}'s birthday!\n"
                    f"Message: {message}",
                    parse_mode="HTML"
                )
            except Exception as e:
                logging.error(f"Failed to send birthday reminder to {user_id}: {e}")
    except Exception as e:
        logging.error(f"Error fetching today's reminders: {e}")

    # Send early reminders
    try:
        future_date = datetime.now() + timedelta(days=1)
        future_date_str = future_date.strftime("%d.%m")

        early_reminders = db.get_early_reminders(future_date_str)
        for user_id, name, message, days_before in early_reminders:
            try:
                await bot.send_message(
                    user_id,
                    f"🎁 Early Birthday Reminder! 🎁\n\n"
                    f"{name}'s birthday is in {days_before} days!\n"
                    f"Don't forget to prepare!\n"
                    f"Message: {message}",
                    parse_mode="HTML"
                )
            except Exception as e:
                logging.error(f"Failed to send early reminder to {user_id}: {e}")
    except Exception as e:
        logging.error(f"Error fetching early reminders: {e}")
