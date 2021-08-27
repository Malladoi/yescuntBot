import os
import telebot
import logging

token = os.environ["TELEGRAM_TOKEN"]
api_token = os.environ["API_TOKEN"]

logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)  # Outputs debug messages to console.
bot = telebot.AsyncTeleBot(token + ":" + api_token)


@bot.message_handler(content_types=["text"])
def sendcunt(message):
    if str(message.text).lower() == 'да':
        bot.send_sticker(message.chat.id,
                         'CAACAgIAAxkBAAIEcWEo5-u9aIvKB5C0W5hGpuVD9BoIAALjEgAC9dC2HQhKdZuwAd7OIAQ',
                         message.id)


bot.polling(none_stop=True)
