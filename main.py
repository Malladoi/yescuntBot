import os
import telebot
import dbwork
import psycopg2
from psycopg2 import pool
from urllib.parse import urlparse
import db_logging
import atexit

token = os.environ["TELEGRAM_TOKEN"]
api_token = os.environ["API_TOKEN"]
bot_name = os.environ["BOT_NAME"]

bot = telebot.TeleBot(token + ":" + api_token)

pg_connection_dict = {
    'dbname': os.environ["POSTGRE_DB"],
    'user': os.environ["POSTGRE_USER"],
    'password': os.environ["POSTGRE_PASSW"],
    'port': os.environ["POSTGRE_PORT"],
    'host': os.environ["POSTGRE_HOST"],
    'application_name': bot_name
}

dbconnectionpool = psycopg2.pool.SimpleConnectionPool(1, 100, **pg_connection_dict)

logconn = dbconnectionpool.getconn()
logger = db_logging.dblogger(appName=os.environ["BOT_NAME"],
                             connection=logconn)

logger.LogInfo(message='Bot started!')

pconn = dbconnectionpool.getconn()
stickerResponses = dict(dbwork.getstickerresponses(conn=pconn))
logger.LogInfo(message='Refresh sticker responses on start!')
dbconnectionpool.putconn(pconn)


@bot.message_handler(commands=["reloadparams"])
def reloadparams(message):
    try:
        conn = dbconnectionpool.getconn()
        adminids = dbwork.getadmins(conn=conn)
        if message.from_user.id in [admin[0] for admin in adminids]:
            stickerResponses.clear()
            stickerResponses.update(dict(dbwork.getstickerresponses(conn=conn)))
            bot.reply_to(message=message, text='Params reloaded')
            logger.LogInfo(message='Params reloaded by userid:{userid}'.format(userid=message.from_user.id))
    except Exception as e:
        logger.LogError(message='Params reload failed by userid:{userid}. Error message:{errmsg}'.format(
            userid=message.from_user.id,
            errmsg=str(e)))
    finally:
        dbconnectionpool.putconn(conn)


@bot.message_handler(content_types=["text"])
def stickerresponce(message):
    try:
        if str(message.text).lower() in stickerResponses.keys():
            bot.send_sticker(message.chat.id,
                             stickerResponses[str(message.text).lower()],
                             message.id)
    except Exception as e:
        logger.LogError(message='Sticker answer err. Userid:{userid}. Error message:{errmsg}'.format(
            userid=message.from_user.id,
            errmsg=str(e)))


def exit_handler():
    logger.LogInfo(message='Bot ended!')
    dbconnectionpool.putconn(logconn)


bot.polling(non_stop=True)
atexit.register(exit_handler)
