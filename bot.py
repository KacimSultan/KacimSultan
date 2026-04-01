import telebot
import os
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

bot = telebot.TeleBot(TOKEN)


# -------- START --------
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


# -------- HELP --------
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "/start - afficher le menu")


# -------- ACTION BOUTONS --------
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


# -------- IA GRATUITE TOGETHER --------
@bot.message_handler(func=lambda message: True)
def chat_ai(message):

    try:
        bot.send_chat_action(message.chat.id, "typing")

        url = "https://api.together.xyz/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/Mistral-7B-Instruct-v0.2",
            "messages": [
                {"role": "user", "content": message.text}
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        result = response.json()
        print(result)

        if "choices" not in result:
            bot.reply_to(message, "⚠️ IA indisponible")
            return

        reply = result["choices"][0]["message"]["content"]

        bot.reply_to(message, reply)

    except Exception as e:
        print("ERREUR:", e)
        bot.reply_to(message, "⚠️ Erreur IA gratuite")


print("Bot is running...")
bot.infinity_polling(skip_pending=True)
