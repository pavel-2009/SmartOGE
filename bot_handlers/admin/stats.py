from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot_handlers.admin.start import IsAdmin

admin_stats_router = Router()


@admin_stats_router.message((F.text == '📊 Статистика пользователей') & IsAdmin() & Command("help"))
async def admin_stats(message: Message) -> None:
    """Handle the /stats command for admin users."""
    await message.answer("Здесь будет отображаться статистика пользователей.")





def get_user_stats() -> str:
    """Generate a string representation of user statistics."""
    
    return 