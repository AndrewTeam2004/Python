"""
Telegram бот-калькулятор с поддержкой математических функций.
Использует aiogram для взаимодействия с Telegram API.
"""

import asyncio
import math
import re
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Настройка логов
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

TOKEN = "8643515349:AAEYM26nnyEfAUY5OtR_8Qr96OJSyhD37to"

bot = Bot(token=TOKEN)
dp = Dispatcher()


def compute_expression(text: str) -> str:
    original_text = text
    text = text.replace(" ", "")
    logger.debug(f"Вычисляю выражение: {text}")

    if not text:
        return "Ошибка ввода. Введите математическое выражение."

    # Проверка: нельзя вводить просто число, например 123
    if not re.search(r'[\+\-\*/\^]', text) and not re.search(r'\b[a-zA-Z_]+\s*\(', text):
        return "Ошибка ввода. Выражение должно содержать оператор или функцию."

    text = text.replace('^', '**')

    text = re.sub(
        r'\b(Cos|Sin|Tan|Log|Exp|Sqrt|Pow)\b',
        lambda m: m.group(0).lower(),
        text
    )

    try:
        result = eval(text, {"__builtins__": None}, math.__dict__)
        description = f"Результат выражения '{original_text}' = {result}"
        logger.info(f"Успешно вычислено: {original_text} -> {result}")
        return description
    except Exception as e:
        logger.error(f"Ошибка вычисления '{original_text}': {e}")
        return "Ошибка ввода. Пример: 2+2 или sqrt(4) или 3^2"

@dp.message(Command("start"))
async def start(message: types.Message) -> None:
    logger.info(f"Пользователь {message.from_user.id} вызвал /start")
    await message.answer(
        f"Привет, {message.from_user.first_name}! Я калькулятор 🤖\n"
        "Используйте /help для списка команд."
    )


@dp.message(Command("help"))
async def help_cmd(message: types.Message) -> None:
    logger.info(f"Пользователь {message.from_user.id} вызвал /help")
    help_text = (
        "Я бот-калькулятор 😊\n"
        "Напиши пример вида: 2+2, 10*5, sqrt(16), pow(2,3), sin(0), Cos(0)\n"
        "Сложные выражения: 2+2-3^4-sqrt(12^57-5^7)\n"
        "Доступные операторы: +, -, *, /, ^ или ** (возведение в степень)\n"
        "Функции: sqrt, pow, sin, cos, tan, log, exp и др. из модуля math\n"
        "Регистр функций не важен: Cos(0) = cos(0)"
    )
    await message.answer(help_text)


@dp.message()
async def calc(message: types.Message) -> None:
    """
    Обработчик всех текстовых сообщений.
    Вычисляет математические выражения.
    """
    user_text = message.text.strip()
    logger.info(f"Получено сообщение от {message.from_user.id}: {user_text}")

    if not user_text:
        await message.answer("Пожалуйста, напишите математическое выражение.")
        return

    result = compute_expression(user_text)
    await message.answer(result)


async def main() -> None:
    logger.info("Бот запускается...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

# Код полностью сделан через ИИ    
