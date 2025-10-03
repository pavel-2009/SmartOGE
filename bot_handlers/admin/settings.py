from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, BaseFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot_handlers.admin.start import IsAdmin
from bot_handlers.admin.start import admin_router
from database import db
from keyboards.reply import SUBJECTS


class NewSubjectState(StatesGroup):
    """State for adding a new quiz subject."""
    new_subject = State()

class DeleteSubjectState(StatesGroup):
    """State for deleting a quiz subject."""
    subject = State()


@admin_router.message(IsAdmin())
@admin_router.message(F.text == '⚙️ Настройки')
async def admin_settings(message: Message) -> None:
    """Provide settings options for admin users."""
    text = """
Виды настроек:
1. Управление пользователями 
2. Настройки викторины
3. Настройки уведомлений
4. Настройки безопасности."""
    markup = ReplyKeyboardMarkup(
        keyboard=[  
            [KeyboardButton(text='1. Управление пользователями')],
            [KeyboardButton(text='2. Настройки викторины')],
            [KeyboardButton(text='3. Настройки уведомлений')],
            [KeyboardButton(text='🔙 Назад')]
        ],
        resize_keyboard=True
    )
    await message.answer(text, reply_markup=markup)


@admin_router.message(IsAdmin())
@admin_router.message(F.text == '🔙 Назад')
async def back_to_admin_menu(message: Message) -> None:
    """Return to the main admin menu."""
    await message.answer('Вы вернулись в главное меню администратора.', reply_markup=ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📊 Статистика пользователей')],
            [KeyboardButton(text='🏆 Рейтинг')],
            [KeyboardButton(text='❓ Помощь')],
            [KeyboardButton(text='⚙️ Настройки')]
        ],
        resize_keyboard=True
    ))


@admin_router.message(IsAdmin())
@admin_router.message(F.text == '1. Управление пользователями')
async def handle_settings_1(message: Message) -> None:
    """Handle user management settings."""
    users = db.get_all_users()
    user_list = "\n".join([f"ID: {user[0]}, Имя: {user[1]}, Баллы: {user[3]}" for user in users])
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Удалить пользователя')],
            [KeyboardButton(text='🔙 Назад')]
        ],
        resize_keyboard=True
    )
    await message.answer(f"Список всех пользователей:\n{user_list}", reply_markup=markup)


@admin_router.message(IsAdmin())
@admin_router.message(F.text == 'Удалить пользователя')
async def delete_user_prompt(message: Message) -> None:
    """Prompt admin to enter user ID to delete."""
    await message.answer("Введите ID пользователя, которого хотите удалить:")
    await admin_router.message.register(process_delete_user, IsAdmin())


async def process_delete_user(message: Message) -> None:
    """Process the deletion of a user by ID."""
    try:
        user_id = int(message.text)
        success = db.delete_user(user_id)
        if success:
            message.bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id)
            await message.answer(f"Пользователь с ID {user_id} успешно удален.")
        else:
            await message.answer(f"Пользователь с ID {user_id} не найден.")
    except ValueError:
        await message.answer("Пожалуйста, введите корректный числовой ID пользователя.")
    except Exception as e:
        await message.answer(f"Произошла ошибка при удалении пользователя: {e}")


@admin_router.message(IsAdmin())
@admin_router.message(F.text == '2. Настройки викторины')
async def handle_settings_2(message: Message) -> None:
    """Handle quiz settings."""
    text = "Настройки викторины:\n1. Добавить/Удалить предметы"
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='1. Добавить/Удалить предметы')],
            [KeyboardButton(text='🔙 Назад')]
        ],
        resize_keyboard=True
    )
    await message.answer(text, reply_markup=markup)


@admin_router.message(IsAdmin())
@admin_router.message(F.text == '1. Добавить/Удалить предметы')
async def manage_quiz_subjects(message: Message) -> None:
    """Manage quiz subjects."""
    subjects = db.get_all_subjects()
    subject_list = "\n".join([f"- {subject[0]}" for subject in subjects])
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Добавить предмет')],
            [KeyboardButton(text='Удалить предмет')],
            [KeyboardButton(text='🔙 Назад')]
        ],
        resize_keyboard=True
    )
    await message.answer(f"Текущие предметы викторины:\n{subject_list}", reply_markup=markup)


@admin_router.message(IsAdmin())
@admin_router.message(F.text == 'Добавить предмет')
async def add_quiz_subject_prompt(message: Message, state: FSMContext) -> None:
    """Prompt admin to enter a new quiz subject."""
    await message.answer("Введите название нового предмета для викторины:")
    await state.set_state(NewSubjectState.new_subject)


@admin_router.message(IsAdmin())
@admin_router.message(NewSubjectState.new_subject)
async def process_add_quiz_subject(message: Message, state: FSMContext) -> None:
    """Process adding a new quiz subject."""
    new_subject = message.text.strip()
    if new_subject in SUBJECTS:
        await message.answer("Этот предмет уже существует.")
    else:
        db.add_subject(new_subject)
        SUBJECTS.append(new_subject)
        await message.answer(f"Предмет '{new_subject}' успешно добавлен.")
    await state.clear()


@admin_router.message(IsAdmin())
@admin_router.message(F.text == 'Удалить предмет')
async def delete_quiz_subject_prompt(message: Message, state: FSMContext) -> None:
    """Prompt admin to enter a quiz subject to delete."""
    await message.answer("Введите название предмета, который хотите удалить:")
    await state.set_state(DeleteSubjectState.subject)


@admin_router.message(IsAdmin())
@admin_router.message(DeleteSubjectState.subject)
async def process_delete_quiz_subject(message: Message, state: FSMContext) -> None:
    """Process deleting a quiz subject."""
    subject_to_delete = message.text.strip()
    if subject_to_delete not in SUBJECTS:
        await message.answer("Этот предмет не найден.")
    else:
        db.delete_subject(subject_to_delete)
        SUBJECTS.remove(subject_to_delete)
        await message.answer(f"Предмет '{subject_to_delete}' успешно удален.")
    await state.clear()


@admin_router.message(IsAdmin())
@admin_router.message(F.text == '3. Настройки уведомлений')
async def handle_settings_3(message: Message) -> None:
    """Handle notification settings."""
    text = "Настройки уведомлений:\n1. Включить/Выключить уведомления\n2. Настроить время уведомлений"
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='1. Включить/Выключить уведомления')],
            [KeyboardButton(text='2. Настроить время уведомлений')],
            [KeyboardButton(text='🔙 Назад')]
        ],
        resize_keyboard=True
    )
    await message.answer(text, reply_markup=markup)

