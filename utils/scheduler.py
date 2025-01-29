import logging
from datetime import datetime
from aiogram import Bot
from database.models import database


async def check_today_reminders(bot: Bot):

    try:
        today = datetime.now().strftime("%d.%m")
        today_reminders = database.get_today_reminders(today)
        for user_id, name, message in today_reminders:
            await send_birthday_message(bot=bot, user_id=user_id, name=name, message=message)
    except Exception as e:
        logging.error(f"Error fetching today's reminders: {e}")


async def send_birthday_message(bot: Bot, user_id: int, name: str, message: str) -> None:
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


async def check_early_reminders(bot: Bot):

    try:
        today = datetime.now().strftime("%d.%m")
        early_reminders = database.get_early_reminders(today)

        for user_id, name, message, days_before in early_reminders:
            await send_early_birthday_message(bot=bot, user_id=user_id, name=name,
                                              message=message, days_before=days_before)
    except Exception as e:
        logging.error(f"Error fetching early reminders: {e}")


async def send_early_birthday_message(bot: Bot, user_id: int, name: str, message: str, days_before: int):
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


async def check_reminders(bot: Bot):
    await check_today_reminders(bot)
    await check_early_reminders(bot)
