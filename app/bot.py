# bot.py
import os
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from app.schemas import run_conversation, user_contexts
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.environ['TELEGRAM_BOT_API_TOKEN']
# Initialize bot and dispatcher
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_contexts[message.from_user.id] = []
    await message.answer(
        "Привет!  Я ваш ассистент в поиске квартир в аренду и автомобилей")


@dp.message()
async def process_message(message: Message):
    user_id = message.from_user.id
    question = message.text
    response = run_conversation(user_id, question)
    if response:
        await message.answer(str(response.choices[0].message.content), end='', flush=True)
    else:
        await message.answer("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова позже.")


@dp.message(Command("ai"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    question = message.text
    response = run_conversation(user_id, question)
    if response:
        await message.answer(str(response.choices[0].message.content), end='', flush=True)
    else:
        await message.answer("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова позже.")
