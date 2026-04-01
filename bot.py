import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)


# -------- START (AVEC MENU DIRECT) --------
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
    bot.reply_to(message, """
📌 Commandes:
/start - afficher le menu
/help - aide
""")


# -------- ACTION DES BOUTONS --------
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    if call.data == "info":
        bot.send_message(call.message.chat.id,
                         "🤖 Je suis un bot amélioré 🚀")

    elif call.data == "hello":
        bot.send_message(call.message.chat.id,
                         "Salut 😄")

    elif call.data == "contact":
        bot.send_message(call.message.chat.id,
                         "📞 Contact : @ton_username")

    elif call.data == "settings":
        bot.send_message(call.message.chat.id,
                         "⚙️ Paramètres bientôt disponibles...")


print("Bot is running...")
bot.infinity_polling(skip_pending=True)