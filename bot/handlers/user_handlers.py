from aiogram import types, Dispatcher, Router
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=["start", "help"]))
async def cmd_start(message: types.Message) -> None:
    """Processes CMD START
    """
    await message.answer(
        text='Hello'
    )
