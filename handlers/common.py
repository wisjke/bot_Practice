from aiogram import types, Router
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def cmd_start(message:types.Message):
    await message.answer(
        "Welcome to Birthday Reminder Bot!\n\n"
        "Commands:\n"
        "/newreminder - Add a new birthday reminder\n"
        "/myreminders - List all your reminders\n"
        "/help - Show this help message"
    )