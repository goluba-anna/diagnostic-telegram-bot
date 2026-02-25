import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F
from aiogram.types import Update, Message
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from sqlalchemy import select
from datetime import datetime

from app.database import engine, AsyncSessionLocal
from app.models import Base, User, WorkingDay

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@dp.message(F.text == "/start")
async def start_handler(message: Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username
            )
            session.add(user)
            await session.commit()

    await message.answer("Бот работает ✅ Пользователь сохранён в базе.")


@dp.message(F.text.startswith("/add_day"))
async def add_working_day(message: Message):
    admin_id = int(os.getenv("ADMIN_ID"))

    if message.from_user.id != admin_id:
        await message.answer("Нет доступа.")
        return

    try:
        parts = message.text.split()
        _, date_str, start_str, end_str = parts

        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        start_time = datetime.strptime(start_str, "%H:%M").time()
        end_time = datetime.strptime(end_str, "%H:%M").time()

        async with AsyncSessionLocal() as session:
            existing = await session.execute(
                select(WorkingDay).where(WorkingDay.date == date_obj)
            )

            if existing.scalar_one_or_none():
                await message.answer("Этот день уже существует.")
                return

            new_day = WorkingDay(
                date=date_obj,
                start_time=start_time,
                end_time=end_time
            )

            session.add(new_day)
            await session.commit()

        await message.answer("Рабочий день добавлен ✅")

    except Exception:
        await message.answer("Формат: /add_day 2026-03-25 10:00 18:00")


@app.post("/webhook")
async def webhook(request: Request):
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"ok": True}


@app.get("/")
async def root():
    return {"status": "Bot is running"}
