from aiogram import Bot
from aiogram.types import BotCommand, ReplyKeyboardMarkup, KeyboardButton


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Почати роботу з ботом 🚀"),
        BotCommand(command="newreminder", description="Додати нове нагадування 🎂"),
        BotCommand(command="myreminders", description="Показати всі мої нагадування 📋"),
        BotCommand(command="help", description="Отримати допомогу ℹ️"),
    ]
    await bot.set_my_commands(commands)


async def get_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/start")],
            [KeyboardButton(text="/newreminder")],
            [KeyboardButton(text="/myreminders")],
            [KeyboardButton(text="/help")],
        ],
        resize_keyboard=True
    )
    return keyboard
