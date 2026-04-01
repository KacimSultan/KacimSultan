import telebot
import os
import google.generativeai as genai
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# =============================
# CONFIG
# =============================

TOKEN = os.getenv("TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

print("GEMINI KEY =", GEMINI_KEY)

bot = telebot.TeleBot(TOKEN)

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# =============================
# START COMMAND
# =============================

@bot.message_handler(commands=['start'])
def start(message):

    markup = InlineKeyboardMarkup(row_width=2)

    btn1 = InlineKeyboardButton("ℹ️ Info", callback_data="info")
    btn2 = InlineKeyboardButton("👋 Salut", callback_data="hello")
    btn3 = InlineKeyboardButton("📞 Contact", callback_data="contact")
    btn4 = InlineKeyboardButton("⚙️ Paramètres", callback_data="settings")

    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(
        message.chat.id,
        "👋 Bienvenue ! Je suis ton bot IA gratuit.\nÉcris-moi un message 🤖",
        reply_markup=markup
    )

# =============================
# HELP
# =============================

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "Envoie simplement un message pour parler avec l'IA.")

# =============================
# BUTTON ACTIONS
# =============================

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    if call.data == "info":
        bot.send_message(call.message.chat.id, "🤖 Bot IA gratuit avec Gemini.")

    elif call.data == "hello":
        bot.send_message(call.message.chat.id, "Salut 😄")

    elif call.data == "contact":
        bot.send_message(call.message.chat.id, "📞 Contact : @ton_username")

    elif call.data == "settings":
        bot.send_message(call.message.chat.id, "⚙️ Paramètres bientôt disponibles.")

# =============================
# GEMINI AI CHAT
# =============================

@bot.message_handler(func=lambda message: True)
def chat_ai(message):

    try:
        bot.send_chat_action(message.chat.id, "typing")

        response = model.generate_content(message.text)

        bot.reply_to(message, response.text)

    except Exception as e:
        print("===== ERREUR GEMINI =====")
        print(e)
        bot.reply_to(message, f"⚠️ Erreur IA:\n{e}")

# =============================
# RUN BOT
# =============================

print("Bot is running...")
bot.infinity_polling(skip_pending=True)
