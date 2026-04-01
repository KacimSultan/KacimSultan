import telebot
import os
import time
import google.generativeai as genai
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ---------------- CONFIG ----------------

TOKEN = os.getenv("TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if not TOKEN:
    raise Exception("TOKEN Telegram manquant")

if not GEMINI_KEY:
    raise Exception("GEMINI_API_KEY manquante")

genai.configure(api_key=GEMINI_KEY)

# ✅ MODELE GEMINI STABLE (FREE)
MODEL_NAME = "gemini-2.0-flash"
print("MODELE UTILISÉ =", MODEL_NAME)

model = genai.GenerativeModel(MODEL_NAME)

bot = telebot.TeleBot(TOKEN)

# Anti-spam IA (évite erreur 429)
last_request = {}

# ---------------- START ----------------

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
        "👋 Bienvenue ! Choisis une option :",
        reply_markup=markup
    )

# ---------------- HELP ----------------

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "/start - afficher le menu")

# ---------------- BOUTONS ----------------

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    if call.data == "info":
        bot.send_message(call.message.chat.id, "🤖 Je suis un bot IA gratuit !")

    elif call.data == "hello":
        bot.send_message(call.message.chat.id, "Salut 😄")

    elif call.data == "contact":
        bot.send_message(call.message.chat.id, "📞 Contact : @ton_username")

    elif call.data == "settings":
        bot.send_message(call.message.chat.id, "⚙️ Paramètres bientôt disponibles...")

# ---------------- IA GEMINI ----------------

@bot.message_handler(func=lambda message: True)
def chat_ai(message):

    # ❌ ignore les commandes
    if message.text.startswith("/"):
        return

    user_id = message.from_user.id
    now = time.time()

    # ✅ anti spam (1 requête / 5 sec)
    if user_id in last_request and now - last_request[user_id] < 5:
        bot.reply_to(message, "⏳ Attends quelques secondes...")
        return

    last_request[user_id] = now

    try:
        bot.send_chat_action(message.chat.id, "typing")

        response = model.generate_content(message.text)

        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "⚠️ Réponse vide.")

    except Exception as e:
        print("===== ERREUR GEMINI =====")
        print(e)
        bot.reply_to(message, "⚠️ IA temporairement indisponible.")

# ---------------- RUN ----------------

print("Bot is running...")
bot.infinity_polling(skip_pending=True)
