from aiogram import types
from aiogram.fsm.context import FSMContext

import logging

from main import dp, bot

@dp.errors_handler()
async def global_error_handler(update: types.Update, exception: Exception, state: FSMContext) -> bool:
    """
    Global error handler for the bot.
    Logs the error and notifies the user.
    """
    # Log the error (you can replace this with your logging mechanism)
    logging.error(f"An error occurred: {exception}")

    if update.message:
        await bot.send_message(update.message.chat.id, "Случилась непредвиденная ошибка. Пожалуйста, попробуйте позже.")
    elif update.callback_query:
        await bot.send_message(update.callback_query.message.chat.id, "Случилась непредвиденная ошибка. Пожалуйста, попробуйте позже.")

    if state:
        await state.finish()

    return True