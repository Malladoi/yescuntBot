import os
import telebot
import logging
from telebot import types
import weatherAPIwrap as wthr
import ast
import dbwork
from datetime import datetime

degree_sign = u'\N{DEGREE SIGN}'

# Openweathermap Weather codes and corressponding emojis
weatheremoji = {"thunderstorm": u'\U0001F4A8',
                "drizzle": u'\U0001F4A7',
                "rain": u'\U00002614',
                "snow": u'\U00002744',
                "snowman": u'\U000026C4',
                "atmosphere": u'\U0001F301',
                "clear": u'\U00002600',
                "clouds": u'\U000026C5',
                "defaultemoji": u'\U0001F300'}

getWeatherEmoji = lambda emojiname: weatheremoji[emojiname] if emojiname in weatheremoji.keys() else weatheremoji[
    'defaultemoji']

token = os.environ["TELEGRAM_TOKEN"]
api_token = os.environ["API_TOKEN"]
bot_name = os.environ["BOT_NAME"]

logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)  # Outputs debug messages to console.
bot = telebot.AsyncTeleBot(token + ":" + api_token)


def refreshinlineButtonMarkup(message):
    markup = types.InlineKeyboardMarkup()
    cities = dbwork.getcitiesforchat(message.chat.id)
    for city in cities:
        markup.add(types.InlineKeyboardButton(text=city[1],
                                              callback_data="['city', '" + city[1] + "']"),
                   types.InlineKeyboardButton(text="Прогноз 24 ч.",
                                              callback_data="['forecast', '" + city[1] + "']"),
                   types.InlineKeyboardButton(text=u'\U0000274C',
                                              callback_data="['delete', '" + city[1] + "']")
                   )
    markup.add(types.InlineKeyboardButton("Добавить", callback_data="btn_add_city"))
    return markup


@bot.message_handler(commands=["weather"])
def weather(message):
    try:
        if message.text in ["/weather", "/weather@{0}".format(bot_name)]:
            bot.send_message(message.chat.id,
                             'Выбери ранее введенный город или добавь новый',
                             reply_markup=refreshinlineButtonMarkup(message))
        else:
            print('lol')
    except Exception as e:
        print(e)


@bot.callback_query_handler(func=lambda call: call.data == 'btn_add_city')
def addnewcity(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Пришли в ответ на это сообщение название нового города',
                          parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if ast.literal_eval(call.data)[0] == 'delete':
        dbwork.removecity(call.message.chat.id, ast.literal_eval(call.data)[1])
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=refreshinlineButtonMarkup(call.message))
    if ast.literal_eval(call.data)[0] == 'city':
        resp = wthr.weatherbycity(ast.literal_eval(call.data)[1])
        if resp.status_code == 200:
            dict_str = resp.content.decode("UTF-8")
            data = ast.literal_eval(dict_str)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.id,
                                  text="Погода для н\п {0} на {1}\n"
                                       "{2} {3}\n"
                                       "Т. {4} {5}\n"
                                       "Ощущается {6} {7}\n"
                                  # "Мин {8} {9}\n"
                                  # "Макс {10} {11}\n"
                                       "Влажность {8}%".format(data['name'],
                                                               datetime.utcfromtimestamp(
                                                                   data['dt'] + data['timezone']).strftime(
                                                                   '%H:%M %d-%m-%Y'),
                                                               getWeatherEmoji(
                                                                   str(data['weather'][0]['main']).lower()),
                                                               data['weather'][0]['description'],
                                                               data['main']['temp'], "C{0}".format(degree_sign),
                                                               data['main']['feels_like'], "C{0}".format(degree_sign),
                                                               # data['main']['temp_min'], "C{0}".format(degree_sign),
                                                               # data['main']['temp_max'], "C{0}".format(degree_sign),
                                                               data['main']['humidity']))
    if ast.literal_eval(call.data)[0] == 'forecast':
        resp = wthr.weatherbycityforecast5day(ast.literal_eval(call.data)[1], 9)
        if resp.status_code == 200:
            dict_str = resp.content.decode("UTF-8")
            data = ast.literal_eval(dict_str)
            messagetext = "Прогноз на сутки для н\п {0}\n".format(data['city']['name'])
            for forecast in data['list']:
                messagetext += "{0} {1} {2} " \
                               "Т. {3} {4} " \
                               "Ощ. {5} {6} " \
                               "Вл. {7}%\n".format(datetime.utcfromtimestamp(
                    forecast['dt'] + data['city']['timezone']).strftime(
                    '%H:%M %d-%m'),
                    getWeatherEmoji(
                        str(forecast['weather'][0]['main']).lower()),
                    forecast['weather'][0]['description'],
                    forecast['main']['temp'], "C{0}".format(degree_sign),
                    forecast['main']['feels_like'], "C{0}".format(degree_sign),
                    forecast['main']['humidity'])
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.id,
                                  text=messagetext)


@bot.message_handler(content_types=["text"])
def sendcunt(message):
    try:
        if str(message.text).lower() == 'да':
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAIEcWEo5-u9aIvKB5C0W5hGpuVD9BoIAALjEgAC9dC2HQhKdZuwAd7OIAQ',
                             message.id)
        if message.reply_to_message is not None:
            if str(
                    message.reply_to_message.text).lower() == 'Пришли в ответ на это сообщение название нового города'.lower() \
                    and message.reply_to_message.from_user.username == bot_name:
                dbwork.addnewcity(message.chat.id, message.text)
                bot.edit_message_text(chat_id=message.reply_to_message.chat.id,
                                      message_id=message.reply_to_message.id,
                                      text='Выбери ранее введенный город или добавь новый',
                                      reply_markup=refreshinlineButtonMarkup(message))
    except Exception as e:
        print(e)


bot.polling(none_stop=True)
