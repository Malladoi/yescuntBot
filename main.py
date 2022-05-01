import os
import telebot
import logging
from telebot import types
import picGen
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

pic_emoji = u'\U0001F5BC'
text_emoji = u'\U0001F4C4'
check_emoji = u'\U00002714'
uncheck_emoji = u'\U00002610'

getWeatherEmoji = lambda emojiname: weatheremoji[emojiname] if emojiname in weatheremoji.keys() else weatheremoji[
    'defaultemoji']
getRespmodeEmoji = lambda respmode: text_emoji if respmode == 1 else pic_emoji

token = os.environ["TELEGRAM_TOKEN"]
api_token = os.environ["API_TOKEN"]
bot_name = os.environ["BOT_NAME"]

logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)  # Outputs debug messages to console.
bot = telebot.AsyncTeleBot(token + ":" + api_token)

runewords = dbwork.getRunewords()


def refreshinlineButtonMarkup(message):
    markup = types.InlineKeyboardMarkup()
    cities = dbwork.getcitiesforchat(message.chat.id)
    settings = dbwork.getchatsettings(message.chat.id)
    if len(settings) == 0:
        dbwork.setchatsettings(message.chat.id, 1)
        settings = dbwork.getchatsettings(message.chat.id)
    for city in cities:
        markup.add(types.InlineKeyboardButton(text=city[1],
                                              callback_data="['city', '" + city[1] + "']"),
                   types.InlineKeyboardButton(text="Прогноз 24 ч.",
                                              callback_data="['forecast', '" + city[1] + "']"),
                   types.InlineKeyboardButton(text=u'\U0000274C',
                                              callback_data="['delete', '" + city[1] + "']")
                   )
    markup.add(types.InlineKeyboardButton("Добавить", callback_data="['btn_add_city']"),
               types.InlineKeyboardButton(getRespmodeEmoji(settings[0][1]),
                                          callback_data="['btn_respmode', {0}]".format(str(settings[0][1]))))
    return markup


def refreshinlineButtonMarkupRunes(message):
    markup = types.InlineKeyboardMarkup()
    runes = dbwork.getAllRunes()
    for tier in range(0, 11):
        markup.add(types.InlineKeyboardButton(text=runes[tier][1],
                                              callback_data="['rune', {0}]".format(str(runes[tier][0]))),
                   types.InlineKeyboardButton(text=runes[tier + 11][1],
                                              callback_data="['rune', {0}]".format(str(runes[tier + 11][0]))),
                   types.InlineKeyboardButton(text=runes[tier + 22][1],
                                              callback_data="['rune', {0}]".format(str(runes[tier + 22][0])))
                   )
    return markup


def refreshinlineButtonMarkupRunes4Runeword(message):
    markup = types.InlineKeyboardMarkup()
    runes = dbwork.getAllRunes()
    runeSettings = dbwork.getRuneSettinds(message.chat.id)
    ifRuneCheckedBool = lambda rid: True if rid in [rs[0] for rs in runeSettings] else False
    ifRuneCheckedEmoji = lambda ifCheked: check_emoji if ifCheked else uncheck_emoji
    for tier in range(0, 11):
        markup.add(types.InlineKeyboardButton(
            text="{0}{1}".format(runes[tier][1], ifRuneCheckedEmoji(ifRuneCheckedBool(runes[tier][0]))),
            callback_data="['rune_check', {0}, {1}]".format(str(runes[tier][0]),
                                                            str(ifRuneCheckedBool(
                                                                runes[tier][
                                                                    0])))

        ),
            types.InlineKeyboardButton(
                text="{0}{1}".format(runes[tier + 11][1],
                                     ifRuneCheckedEmoji(ifRuneCheckedBool(runes[tier + 11][0]))),
                callback_data="['rune_check', {0}, {1}]".format(str(runes[tier + 11][0]),
                                                                str(ifRuneCheckedBool(
                                                                    runes[tier + 11][
                                                                        0])))

            ),
            types.InlineKeyboardButton(
                text="{0}{1}".format(runes[tier + 22][1],
                                     ifRuneCheckedEmoji(ifRuneCheckedBool(runes[tier + 22][0]))),
                callback_data="['rune_check', {0}, {1}]".format(str(runes[tier + 22][0]),
                                                                str(ifRuneCheckedBool(
                                                                    runes[tier + 22][
                                                                        0])))

            )
        )

    markup.add(types.InlineKeyboardButton("Check runewords", callback_data="['check_runewords']"))
    return markup


@bot.message_handler(commands=["weather"])
def weather(message):
    try:
        if message.text in ["/weather", "/weather@{0}".format(bot_name)]:
            bot.send_message(message.chat.id,
                             'Выбери ранее введенный город или добавь новый',
                             reply_markup=refreshinlineButtonMarkup(message))
    except Exception as e:
        print(e)


@bot.message_handler(commands=["runes"])
def weather(message):
    try:
        if message.text in ["/runes", "/runes@{0}".format(bot_name)]:
            bot.send_message(message.chat.id,
                             'List of all runes',
                             reply_markup=refreshinlineButtonMarkupRunes(message))
    except Exception as e:
        print(e)


@bot.message_handler(commands=["pickupruneword"])
def weather(message):
    try:
        if message.text in ["/pickupruneword", "/pickupruneword@{0}".format(bot_name)]:
            bot.send_message(message.chat.id,
                             'List of all runes. Pick runes you got.',
                             reply_markup=refreshinlineButtonMarkupRunes4Runeword(message))
    except Exception as e:
        print(e)


@bot.callback_query_handler(func=lambda call: ast.literal_eval(call.data)[0] == 'btn_add_city')
def addnewcity(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Пришли в ответ на это сообщение название нового города',
                          parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: ast.literal_eval(call.data)[0] == 'rune_check')
def checkRune(call):
    rune = ast.literal_eval(call.data)
    dbwork.setRuneSettings(call.message.chat.id, rune[1])
    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=refreshinlineButtonMarkupRunes4Runeword(call.message))


@bot.callback_query_handler(func=lambda call: ast.literal_eval(call.data)[0] == 'btn_respmode')
def setrespsettings(call):
    dbwork.updarechatsettings(call.message.chat.id,
                              (lambda respmode: 1 if ast.literal_eval(call.data)[1] == 2 else 2)(
                                  ast.literal_eval(call.data)[1]))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=refreshinlineButtonMarkup(call.message))


@bot.callback_query_handler(func=lambda call: ast.literal_eval(call.data)[0] == 'delete')
def deleteCity(call):
    dbwork.removecity(call.message.chat.id, ast.literal_eval(call.data)[1])
    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=refreshinlineButtonMarkup(call.message))


@bot.callback_query_handler(func=lambda call: ast.literal_eval(call.data)[0] == 'city')
def currWather(call):
    resp = wthr.weatherbycity(ast.literal_eval(call.data)[1])
    if resp.status_code == 200:
        dict_str = resp.content.decode("UTF-8")
        data = ast.literal_eval(dict_str)
        if dbwork.getchatsettings(call.message.chat.id)[0][1] == 1:
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
                                                               data['main']['feels_like'],
                                                               "C{0}".format(degree_sign),
                                                               # data['main']['temp_min'], "C{0}".format(degree_sign),
                                                               # data['main']['temp_max'], "C{0}".format(degree_sign),
                                                               data['main']['humidity']))
        else:
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_photo(chat_id=call.message.chat.id, photo=
            picGen.createCurrWeatherImg(data['weather'][0]['icon'],
                                        4,
                                        datetime.utcfromtimestamp(data['dt'] + data['timezone']).strftime(
                                            '%H:%M %d-%m-%Y'),
                                        data['name'],
                                        data['main']['temp'],
                                        data['weather'][0]['description'],
                                        data['main']['feels_like'],
                                        data['main']['humidity']))


@bot.callback_query_handler(func=lambda call: ast.literal_eval(call.data)[0] == 'forecast')
def forecast(call):
    if ast.literal_eval(call.data)[0] == 'forecast':
        resp = wthr.weatherbycityforecast5day(ast.literal_eval(call.data)[1], 9)
        if resp.status_code == 200:
            dict_str = resp.content.decode("UTF-8")
            data = ast.literal_eval(dict_str)
            if dbwork.getchatsettings(call.message.chat.id)[0][1] == 1:
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
            else:
                bot.delete_message(call.message.chat.id, call.message.id)
                bot.send_photo(chat_id=call.message.chat.id, photo=
                picGen.createWeatherForecastImg(data, 4))


@bot.callback_query_handler(func=lambda call: ast.literal_eval(call.data)[0] == 'rune')
def runeInfo(call):
    runeInfo = dbwork.getRune(ast.literal_eval(call.data)[1])
    bot.delete_message(call.message.chat.id, call.message.id)
    tier = None
    if runeInfo[0][0] <= 11:
        tier = 'low'
    elif runeInfo[0][0] <= 22:
        tier = 'mid'
    else:
        tier = 'high'
    text = "Rune: {0}\n\n" \
           "Tier: {1}\n\n" \
           "Minimum clvl: {2}\n\n" \
           "Weapon effects:\n{3}\n\n" \
           "Armor effects:\n{4}\n\n" \
           "Recipe for a rune:\n{5}".format(runeInfo[0][1], tier, runeInfo[0][2], runeInfo[0][3], runeInfo[0][4],
                                            runeInfo[0][5])
    bot.send_message(call.message.chat.id, text)


@bot.callback_query_handler(func=lambda call: ast.literal_eval(call.data)[0] == 'check_runewords')
def runewordCheck(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    string = "Runeword:\n{0}\n\n" \
             "Item(s)\n{1}\n\n" \
             "Sockets count:\n{2}\n\n" \
             "Runes:\n{3}\n\n" \
             "Effect:\n{4}\n\n"
    for runeword in dbwork.getRunewordsByChatId(call.message.chat.id):
        bot.send_message(call.message.chat.id,
                         string.format(runeword[1], runeword[3], runeword[2], runeword[5], runeword[4]))


@bot.message_handler(content_types=["text"])
def sendcunt(message):
    try:
        if str(message.text).lower() in ['да','da']:
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
