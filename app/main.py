import os
import uuid
import asyncio
from datetime import datetime, timedelta

from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F
from aiogram.types import Update, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from sqlalchemy import select

from app.database import engine, AsyncSessionLocal
from app.models import Base, User, Booking

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Юкасса пока не подключаем
YOOKASSA_SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
YOOKASSA_SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")
PAYMENT_RETURN_URL = os.getenv("PAYMENT_RETURN_URL", "https://t.me/ТВОЙ_БОТ")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ---------------- START ----------------
@dp.message(F.text == "/start")
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Записаться на консультацию", callback_data="book_consult")]
    ])
    await message.answer("Выберите действие:", reply_markup=keyboard)


# ---------------- CREATE BOOKING ----------------
@dp.callback_query(F.data == "book_consult")
async def create_booking(callback):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                telegram_id=callback.from_user.id,
                username=callback.from_user.username
            )
            session.add(user)
            await session.commit()

        booking = Booking(
            user_id=user.id,
            date=datetime.utcnow().date(),
            start_time=datetime.utcnow().time(),
            end_time=(datetime.utcnow() + timedelta(hours=1)).time(),
            status="pending"
        )

        session.add(booking)
        await session.commit()
        await session.refresh(booking)

        # ---------------- Информация о брони ----------------
        await callback.message.answer(
            "Бронь создана. Оплата будет доступна после подключения Юкасса."
        )

    # ---------------- Таймер 15 минут ----------------
    async def cancel_booking_if_not_paid(booking_id: int):
        await asyncio.sleep(900)  # 15 минут
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Booking).where(Booking.id == booking_id)
            )
            booking_to_check = result.scalar_one_or_none()
            if booking_to_check and booking_to_check.status == "pending":
                booking_to_check.status = "cancelled"
                await session.commit()
                try:
                    await bot.send_message(
                        booking_to_check.user.telegram_id,
                        "Время на оплату истекло ⏰ Ваша бронь была отменена."
                    )
                except:
                    pass

    asyncio.create_task(cancel_booking_if_not_paid(booking.id))


# ---------------- TELEGRAM WEBHOOK ----------------
@app.post("/webhook")
async def webhook(request: Request):
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"ok": True}


@app.get("/")
async def root():
    return {"status": "Bot is running"}
