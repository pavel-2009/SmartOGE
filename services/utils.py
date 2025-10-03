import requests
import json
import ast
import asyncio
from aiogram import types
from dotenv import load_dotenv
import os

load_dotenv()


def generate_quiz(subject: str, level: str) -> list:
    """Generate a quiz using an AI service."""
    for attempt in range(10):
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"{os.getenv('OPENROUTER_API_KEY')}",
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "model": "mistralai/mixtral-8x7b-instruct",
                    "messages": [
                        {
                            "role": "user",
                            "content": f"""
                        Сгенерируй 10 экзаменационных вопросов для подготовки к ОГЭ по предмету "{subject}" уровня сложности "{level}".

                        Каждый вопрос — список из 4 элементов:
                        [
                        "Вопрос",
                        {{
                            "A": "...",
                            "B": "...",
                            "C": "...",
                            "D": "..."
                        }},
                        "Правильный вариант (A|B|C|D) (только буква, без ответа)",
                        "Объяснение"
]

Ответ: только **валидный Python-список из 10 таких списков**. Без заголовков, markdown, LaTeX, пояснений. Всё на русском.
Объяснение должно быть подробным, как в задачах из Школково. Все математические термины на английском заменять на русские.
"""
                        }
                    ]
                })
            )

            result = response.json()

            content = result['choices'][0]['message']['content'].strip()

            try:
                quiz_list = ast.literal_eval(content)
            except Exception as parse_err:
                print(f"⚠️ Ошибка парсинга ответа: {parse_err}")
                continue

            if (
                isinstance(quiz_list, list)
                and len(quiz_list) == 10
                and all(
                    isinstance(q, list)
                    and len(q) == 4
                    and isinstance(q[0], str)
                    and isinstance(q[1], dict)
                    and isinstance(q[2], str)
                    and isinstance(q[3], str)
                    for q in quiz_list
                )
            ):
                print(quiz_list)
                return quiz_list
            else:
                print("⚠️ Невалидная структура данных.")
                continue

        except Exception as e:
            print(f"⚠️ Попытка #{attempt + 1} не удалась: {e}")
            if hasattr(response, "text"):
                print("Ответ сервера:\n", response.text)
            continue

    raise ValueError(
        "❌ Не удалось получить валидный список от ИИ после 10 попыток.")


def answer_isright(answer_num: int, answer: str, quiz: list) -> bool:
    """Check if the provided answer is correct."""
    return quiz[answer_num][2].lower() == answer.lower()


async def show_loading_animation(message: types.Message, task: asyncio.Task) -> any:
    """Show a loading animation while waiting for a task to complete.
    """
    loading_text = "Генерируется квиз"
    dots = ["", ".", "..", "..."]
    i = 0

    msg = await message.answer(f"<b>{loading_text}{dots[i]}</b>" + '' * (4 - i), parse_mode='html')

    while not task.done():
        i = (i + 1) % len(dots)
        try:
            await msg.edit_text(f"<b>{loading_text}{dots[i]}</b>" + '' * (4 - i), parse_mode='html')
        except Exception:
            pass
        await asyncio.sleep(0.3)

    return await task
