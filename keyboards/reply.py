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
