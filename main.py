import os
import telebot
import logging
from telebot import types
import weatherAPIwrap as wthr
import ast
import dbwork

token = os.environ["TELEGRAM_TOKEN"]
api_token = os.environ["API_TOKEN"]
bot_name = os.environ["BOT_NAME"]

logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)  # Outputs debug messages to console.
bot = telebot.AsyncTeleBot(token + ":" + api_token)


@bot.message_handler(commands=["weather"])
def weather(message):
    try:
        if message.text in ["/weather", "/weather@{0}".format(bot_name)]:
            markup = types.InlineKeyboardMarkup()
            cities = dbwork.getcitiesforchat(message.chat.id)
            for city in cities:
                markup.add(types.InlineKeyboardButton(text=city[1],
                                                      callback_data="['city', '" + city[1] + "']"),
                           types.InlineKeyboardButton(text=u'\U0000274C',
                                                      callback_data="['delete', '" + city[1] + "']"))
            btnNewCity = types.InlineKeyboardButton("Добавить", callback_data="btn_add_city")
            markup.add(btnNewCity)
            bot.send_message(message.chat.id,
                             'Выбери ранее введенный город или добавь новый',
                             reply_markup=markup)
            # result = task.wait()
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
        markup = types.InlineKeyboardMarkup()
        cities = dbwork.getcitiesforchat(call.message.chat.id)
        for city in cities:
            markup.add(types.InlineKeyboardButton(text=city[1],
                                                  callback_data="['city', '" + city[1] + "']"),
                       types.InlineKeyboardButton(text=u'\U0000274C',
                                                  callback_data="['delete', '" + city[1] + "']"))
        btnNewCity = types.InlineKeyboardButton("Добавить", callback_data="btn_add_city")
        markup.add(btnNewCity)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markup)
    if ast.literal_eval(call.data)[0] == 'city':
        resp = wthr.weatherbycity(ast.literal_eval(call.data)[1])
        if resp.status_code == 200:
            dict_str = resp.content.decode("UTF-8")
            data = ast.literal_eval(dict_str)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.id,
                                  text="{0}\n"
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
                markup = types.InlineKeyboardMarkup()
                cities = dbwork.getcitiesforchat(message.chat.id)
                for city in cities:
                    markup.add(types.InlineKeyboardButton(text=city[1],
                                                          callback_data="['city', '" + city[1] + "']"),
                               types.InlineKeyboardButton(text=u'\U0000274C',
                                                          callback_data="['delete', '" + city[1] + "']"))
                btnNewCity = types.InlineKeyboardButton("Добавить", callback_data="btn_add_city")
                markup.add(btnNewCity)
                bot.edit_message_text(chat_id=message.reply_to_message.chat.id,
                                      message_id=message.reply_to_message.id,
                                      text='Выбери ранее введенный город или добавь новый',
                                      reply_markup=markup)
    except Exception as e:
        print(e)


bot.polling(none_stop=True)
