import telebot
import os

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)


# -------- START --------
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Bienvenue ! Tape /menu")


# -------- HELP --------
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, """
📌 Commandes:
/start
/help
/menu
""")


# -------- MENU AVEC BOUTONS --------
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = InlineKeyboardMarkup(row_width=2)

    btn1 = InlineKeyboardButton("ℹ️ Info", callback_data="info")
    btn2 = InlineKeyboardButton("👋 Salut", callback_data="hello")
    btn3 = InlineKeyboardButton("📞 Contact", callback_data="contact")
    btn4 = InlineKeyboardButton("⚙️ Paramètres", callback_data="settings")

    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(
        message.chat.id,
        "📋 Menu principal :",
        reply_markup=markup
    )
def menu(message):
    markup = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton("ℹ️ Info", callback_data="info")
    btn2 = InlineKeyboardButton("👋 Salut", callback_data="hello")

    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, "Choisis une option :", reply_markup=markup)


# -------- ACTION BOUTONS --------
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    if call.data == "info":
        bot.send_message(call.message.chat.id, "Je suis un bot amélioré 🚀")

    elif call.data == "hello":
        bot.send_message(call.message.chat.id, "Salut 😄")


print("Bot is running...")
bot.infinity_polling(skip_pending=True)