import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command

# ====== Переменные окружения ======
BOT_TOKEN = os.getenv("BOT_TOKEN")
PUBLIC_OFFER_URL = os.getenv("PUBLIC_OFFER_URL")
PERSONAL_DATA_POLICY_URL = os.getenv("PERSONAL_DATA_POLICY_URL")
AGREEMENTS_FILE_URL = os.getenv("AGREEMENTS_FILE_URL")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# ====== Приветственное сообщение ======
@dp.message(Command("start"))
async def start(message: types.Message):
    username = message.from_user.first_name
    text = f"""
Привет, {username}! ❤️

Бывает, что жизнь будто ходит по одному и тому же кругу:
• Одни и те же ссоры в отношениях
• Деньги утекают сквозь пальцы
• Всё время попадаешь в похожие ситуации
• Внутри живёт ощущение, что что-то не так

Это не случайности. Это твои внутренние программы — способы, которыми психика когда-то научилась защищаться. Они влияют на твои решения, отношения и то, как ты себя чувствуешь.

Я — бот метода <b>СОВ (Системы Осознанного Выбора)</b>.  
Через диагностику я пойму твои основные программы и покажу, как они влияют на твою жизнь.

Хочешь узнать себя глубже? 👀

<b>Готов(-а) начать?</b>
"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Начать диагностику", callback_data="start_diag")],
        [InlineKeyboardButton("О методе СОВ", callback_data="about_method")],
        [InlineKeyboardButton("Условия и документы", callback_data="docs")]
    ])
    await message.answer(text, reply_markup=keyboard)

# ====== Обработка кнопок ======
@dp.callback_query(lambda c: True)
async def button_handler(callback: types.CallbackQuery):
    data = callback.data

    if data == "start_diag":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("Я согласен(а)", callback_data="agree")],
            [InlineKeyboardButton("Ознакомиться с условиями", callback_data="read_docs")]
        ])
        await callback.message.edit_text(
            "Перед началом диагностики нужно дать согласие на условия. Ознакомьтесь с перечнем документов ниже.",
            reply_markup=keyboard
        )

    elif data == "agree":
        await callback.message.edit_text("Отлично, начинаем диагностику!")

    elif data == "read_docs":
        await callback.message.edit_text(
            f"Вот ссылки на документы:\n"
            f"• <a href='{PUBLIC_OFFER_URL}'>Публичная оферта</a>\n"
            f"• <a href='{PERSONAL_DATA_POLICY_URL}'>Согласие на обработку персональных данных</a>\n"
            f"• <a href='{AGREEMENTS_FILE_URL}'>Согласие на получение информационных материалов</a>"
        )

    elif data == "about_method":
        text = f"""
📚 <b>О методе СОВ — Системы Осознанного Выбора</b>

СОВ — это простой и бережный способ увидеть свои внутренние программы и понять, как они влияют на жизнь.

🔍 <b>Что такое программы?</b>
Это автоматические реакции, которые родом из детства. Когда-то они помогали выжить, а теперь могут мешать жить.

🎯 <b>Как работает диагностика:</b>
• Ты отвечаешь на вопросы — честно и не задумываясь
• Бот определяет твои основные программы
• Ты получаешь понятные описания и видишь, что влияет на твои отношения, деньги и самооценку

Диагностика занимает 5–7 минут. 

<b>Готовы начать диагностику?</b>
"""
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("Начать диагностику", callback_data="start_diag")]
        ])
        await callback.message.edit_text(text, reply_markup=keyboard)

    elif data == "docs":
        text = f"С условиями и документами ты можешь ознакомиться по ссылкам:\n" \
               f"• <a href='{PUBLIC_OFFER_URL}'>Публичная оферта</a>\n" \
               f"• <a href='{PERSONAL_DATA_POLICY_URL}'>Согласие на обработку персональных данных</a>\n" \
               f"• <a href='{AGREEMENTS_FILE_URL}'>Согласие на получение информационных материалов</a>"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("Начать диагностику", callback_data="start_diag")]
        ])
        await callback.message.edit_text(text, reply_markup=keyboard)

# ====== Запуск бота ======
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
