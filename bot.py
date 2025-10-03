from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from aiogram.types import BotCommand

from dotenv import load_dotenv
from os import getenv

from bot_handlers.start import start_router
from bot_handlers.quiz import quiz_router
from bot_handlers.stats import stats_router
from bot_handlers.raiting import raiting_router
from bot_handlers.admin.start import admin_router
from bot_handlers.admin.stats import admin_stats_router



load_dotenv()


async def main() -> None:
    """Main function to start the bot."""
    bot = Bot(token=getenv("BOT_TOKEN"))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(quiz_router)
    dp.include_router(start_router)
    dp.include_router(stats_router)
    dp.include_router(raiting_router)
    dp.include_router(admin_router)
    dp.include_router(admin_stats_router)

    commands = [
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="quiz", description="Начать викторину"),
        BotCommand(command="stats", description="Моя статистика"),
        BotCommand(command="help", description="Помощь"),
    ]

    await bot.set_my_commands(commands)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
