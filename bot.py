import telebot
import os

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def reply(message):
    bot.reply_to(message, "Bonjour, je suis ton bot 🤖")

print("Bot is running...")
bot.infinity_polling()