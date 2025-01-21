import os

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from utils.commands import get_reply_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message:Message):


    await message.answer(
        "👋 Ласкаво просимо до Бота Нагадувань про День Народження! 🎉\n\n"
        "Доступні команди:\n"
        "• /newreminder - Додати нове нагадування 🎂\n"
        "• /myreminders - Показати всі мої нагадування \n"
        "• /help - Отримати допомогу ℹ️\n\n"
        "💡 Виберіть команду з меню або введіть її вручну!\n",
    )

@router.message(Command(commands=['help']))
async def cmd_help(message:Message):
    await message.answer(
        "Доступні команди:\n"
        "• /newreminder - Додати нове нагадування 🎂\n"
        "• /myreminders - Показати всі мої нагадування \n"
        "• /help - Отримати допомогу ℹ️\n"
    )