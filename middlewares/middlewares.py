from aiogram import BaseMiddleware
from bot_handlers.admin.start import IsAdmin

from database import db

class AdminStatsMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        message = event
        if message and message.from_user:
            user_id = message.from_user.id
            if IsAdmin.is_admin(user_id):
                db.increment_admin_stat(chat_id=user_id, stat_field="commands_used", increment=1)
        return await handler(event, data)
    
