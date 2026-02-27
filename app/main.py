from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Ссылки на документы (будут подставляться через переменные окружения на Railway)
PUBLIC_OFFER_URL = "https://example.com/public_offer"
PERSONAL_DATA_POLICY_URL = "https://example.com/personal_data_policy"
AGREEMENTS_FILE_URL = "https://example.com/agreements"

# ====== Приветственное сообщение ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.first_name
    text = f"""
Привет, {username}! Я бот метода
<b>СОВ — Системы Осознанного Выбора</b>
Я помогу тебе понять, какие программы сейчас активны в твоей жизни — и как именно они влияют на отношения, самооценку, деньги и решения.

Диагностика займёт 2–3 минуты.
Здесь главное честность, перед самим собой.

<b>📄 Важные документы:</b>
• <a href="{PUBLIC_OFFER_URL}">Публичная оферта</a>
• <a href="{PERSONAL_DATA_POLICY_URL}">Согласие на обработку персональных данных</a>
• <a href="{AGREEMENTS_FILE_URL}">Согласие на получение рекламно-информационных материалов</a>

<b>Готов(-а) начать?</b>
"""
    keyboard = [
        [InlineKeyboardButton("Начать диагностику", callback_data="start_diag")],
        [InlineKeyboardButton("О методе СОВ", callback_data="about_method")],
        [InlineKeyboardButton("Условия и документы", callback_data="docs")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="HTML", disable_web_page_preview=True)

# ====== Сообщение о методе СОВ ======
async def about_method_text():
    text = f"""
📚 <b>О методе СОВ — Системы Осознанного Выбора</b>

<b>Что такое СОВ?</b>
СОВ — это системный подход, который соединяет психологию и механизмы выбора. Он помогает понять, какие программы управляют вашими решениями в жизни.

<b>Основные принципы метода:</b>
• <b>Системность</b> — рассматривает психику как целостную систему
• <b>Осознанность</b> — помогает увидеть автоматические реакции
• <b>Выбор</b> — учит делать осознанные решения вместо автоматических реакций

<b>Что такое «программы»?</b>
Программы — это глубинные схемы поведения, которые:
• Формируются в детстве, передаются от родителей
• Работают автоматически
• Влияют на отношения, карьеру, финансы
• Часто приводят к повторяющимся сценариям и кризисам

<b>Как работает диагностика?</b>
1. Вы отвечаете на вопросы
2. Система анализирует ваши ответы
3. Выявляет 3 ведущие программы
4. Дает понимание их влияния на жизнь

<b>Что вы получите после диагностики?</b>
• Понимание своих ведущих программ
• Осознание, как они влияют на вашу жизнь
• Направление для дальнейшего развития

<b>📄 Важные документы:</b>
• <a href="{PUBLIC_OFFER_URL}">Публичная оферта</a>
• <a href="{PERSONAL_DATA_POLICY_URL}">Согласие на обработку персональных данных</a>
• <a href="{AGREEMENTS_FILE_URL}">Согласие на получение рекламно-информационных материалов</a>

<b>Готовы начать диагностику?</b>
"""
    return text

# ====== Обработка кнопок ======
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "start_diag":
        keyboard = [
            [InlineKeyboardButton("Я согласен(а)", callback_data="agree")],
            [InlineKeyboardButton("Ознакомиться с условиями", callback_data="read_docs")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"Перед началом диагностики нужно дать согласие на условия. Ознакомьтесь с перечнем документов ниже.", 
            reply_markup=reply_markup
        )
        
    elif query.data == "agree":
        await query.edit_message_text("Отлично, начинаем диагностику!")
        # Тут можно запускать функцию с самим опросом
        
    elif query.data == "read_docs":
        await query.edit_message_text(
            f"Вот ссылки на документы:\n• <a href='{PUBLIC_OFFER_URL}'>Публичная оферта</a>\n• <a href='{PERSONAL_DATA_POLICY_URL}'>Согласие на обработку персональных данных</a>\n• <a href='{AGREEMENTS_FILE_URL}'>Согласие на получение рекламно-информационных материалов</a>",
            parse_mode="HTML"
        )
        
    elif query.data == "about_method":
        text = await about_method_text()
        keyboard = [[InlineKeyboardButton("Начать диагностику", callback_data="start_diag")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=reply_markup)
        
    elif query.data == "docs":
        text = f"Вот ссылки на условия и документы:\n• <a href='{PUBLIC_OFFER_URL}'>Публичная оферта</a>\n• <a href='{PERSONAL_DATA_POLICY_URL}'>Согласие на обработку персональных данных</a>\n• <a href='{AGREEMENTS_FILE_URL}'>Согласие на получение рекламно-информационных материалов</a>"
        keyboard = [[InlineKeyboardButton("Начать диагностику", callback_data="start_diag")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=reply_markup)

# ====== Запуск бота ======
if __name__ == "__main__":
    import os
    TOKEN = os.getenv("BOT_TOKEN")  # В Railway передаем через переменные окружения
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Бот запущен...")
    app.run_polling()
