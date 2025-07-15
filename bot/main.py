# mooncasino/bot/main.py

from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo
from aiogram.utils import executor
import asyncio
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Пример: "@MoonCasino777"
WEBAPP_URL = os.getenv("WEBAPP_URL")  # URL мини-приложения

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

def init_db():
    with sqlite3.connect("db.sqlite") as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 1000
        )
        """)
        conn.commit()

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    with sqlite3.connect("db.sqlite") as conn:
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
    await message.answer("Добро пожаловать в MoonCasino! На ваш счёт зачислено 1000₮")

@dp.message_handler(commands=['balance'])
async def balance_cmd(message: types.Message):
    user_id = message.from_user.id
    with sqlite3.connect("db.sqlite") as conn:
        cur = conn.cursor()
        cur.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
    bal = row[0] if row else 0
    await message.answer(f"Ваш баланс: {bal}₮")

@dp.message_handler(commands=['miniapp'])
async def miniapp_cmd(message: types.Message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🎰 Играть", web_app=WebAppInfo(url=WEBAPP_URL)))
    await message.answer("Открой мини-игры:", reply_markup=kb)

# Обработка WebApp callback будет добавлена позже

if __name__ == '__main__':
    init_db()
    executor.start_polling(dp, skip_updates=True)# main.py для бота
