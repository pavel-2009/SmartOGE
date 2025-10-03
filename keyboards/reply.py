from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

SUBJECTS = ['Математика', 'Русский язык', 'Физика', 'Информатика']

subjects_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=subject)] for subject in SUBJECTS
    ],
    resize_keyboard=True,
    input_field_placeholder='📚 Выберите предмет:'
)

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📚 Начать викторину'),
    KeyboardButton(text='📈 Моя статистика')],
    [KeyboardButton(text='🏆 Рейтинг'), KeyboardButton(text='❓ Помощь')]
], resize_keyboard=True)


settings_markup = ReplyKeyboardMarkup(
        keyboard=[  
            [KeyboardButton(text='1. Управление пользователями')],
            [KeyboardButton(text='2. Настройки викторины')],
            [KeyboardButton(text='3. Настройки уведомлений')],
            [KeyboardButton(text='🔙 Назад')]
        ],
        resize_keyboard=True
    )

admin_buttons = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📊 Статистика пользователей')],
            [KeyboardButton(text='🏆 Рейтинг')],
            [KeyboardButton(text='❓ Помощь')],
            [KeyboardButton(text='⚙️ Настройки')]
        ],
        resize_keyboard=True
    )