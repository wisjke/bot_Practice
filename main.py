import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot.handlers.user_handlers import router


async def main() -> None:

    load_dotenv('.env')
    token = os.getenv('TOKEN_API')
    bot = Bot(token=token)
    dp = Dispatcher()

    dp.include_router(router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)  # Ensure no pending updates
        await dp.start_polling(bot)
    except Exception as _ex:
        print(_ex)

if __name__ == '__main__':
    asyncio.run(main())
