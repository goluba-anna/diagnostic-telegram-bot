import os
from datetime import datetime, timedelta

from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F
from aiogram.types import Update, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy import select

from app.database import engine, AsyncSessionLocal
from app.models import Base, User, Booking

# ---------------- ENV ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
app = FastAPI()


# ---------------- STARTUP ----------------
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ---------------- /start ----------------
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

        # Временно без Юкасса
        await callback.message.answer(
            "Бронь создана. Оплата будет доступна после подключения Юкасса."
        )


# ---------------- YOOKASSA PAYMENT ----------------
# Этот блок закомментирован до подписания договора с Юкасса
# from yookassa import Payment, Configuration
# import uuid
#
# YOOKASSA_SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
# YOOKASSA_SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")
# PAYMENT_RETURN_URL = "https://t.me/ТВОЙ_БОТ"  # замени на ссылку своего бота
#
# Configuration.account_id = YOOKASSA_SHOP_ID
# Configuration.secret_key = YOOKASSA_SECRET_KEY
#
# def create_yookassa_payment(booking_id: int, amount: int):
#     payment = Payment.create({
#         "amount": {
#             "value": str(amount),
#             "currency": "RUB"
#         },
#         "confirmation": {
#             "type": "redirect",
#             "return_url": PAYMENT_RETURN_URL
#         },
#         "capture": True,
#         "description": f"Booking #{booking_id}"
#     }, str(uuid.uuid4()))
#
#     if not hasattr(payment, "confirmation"):
#         print("YOOKASSA ERROR:", payment)
#         raise Exception("Ошибка создания платежа")
#
#     return payment.confirmation.confirmation_url


# ---------------- TELEGRAM WEBHOOK ----------------
@app.post("/webhook")
async def webhook(request: Request):
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"ok": True}


# ---------------- ROOT ----------------
@app.get("/")
async def root():
    return {"status": "Bot is running"}
