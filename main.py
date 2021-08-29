import os
import telebot
import logging
from telebot import types
import weatherAPIwrap as wthr
import ast

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

@bot.inline_handler(lambda query: query.query == 'weather')
def query_text(inline_query):
    try:
        resp = wthr.weather(inline_query)
        if resp.status_code == 200:
            dict_str = resp.content.decode("UTF-8")
            data = ast.literal_eval(dict_str)
            re = types.InlineQueryResultArticle(id='1',
                                                title="{0}".format(data['weather'][0]['description']),
                                                thumb_url="https://openweathermap.org/img/wn/{0}@2x.png".format(data['weather'][0]['icon']),
                                                input_message_content=types.InputTextMessageContent("{0}\n"
                                                            "Темп. {1}\n"
                                                            "Ощущается как {2}\n"
                                                            "Мин {3}\n"
                                                            "Макс {4}\n"
                                                            "Влажность {5}%".format(data['weather'][0]['description'],
                                                                                    data['main']['temp'],
                                                                                    data['main']['feels_like'],
                                                                                    data['main']['temp_min'],
                                                                                    data['main']['temp_max'],
                                                                                    data['main']['humidity'])),
                                                description="{0}\n"
                                                            "Темп. {1}\n"
                                                            "Ощущается как {2}\n"
                                                            "Мин {3}\n"
                                                            "Макс {4}\n"
                                                            "Влажность {5}%".format(data['weather'][0]['description'],
                                                                                    data['main']['temp'],
                                                                                    data['main']['feels_like'],
                                                                                    data['main']['temp_min'],
                                                                                    data['main']['temp_max'],
                                                                                    data['main']['humidity']))
            # r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
            bot.answer_inline_query(inline_query.id, [re])
    except Exception as e:
        print(e)


bot.polling(none_stop=True)
