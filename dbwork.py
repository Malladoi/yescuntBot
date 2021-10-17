import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

def getcitiesforchat(chatid):
    sql_com = 'SELECT chatid, city	FROM public."tSavedCities" where chatid = {0};'.format(chatid)
    cursor = conn.cursor()
    cursor.execute(sql_com)
    records = cursor.fetchall()
    cursor.close()
    return records

def getchatsettings(chatid):
    sql_com = 'SELECT chatid, respmode	FROM public."tChatSetting" where chatid = {0};'.format(chatid)
    cursor = conn.cursor()
    cursor.execute(sql_com)
    records = cursor.fetchall()
    cursor.close()
    return records

def setchatsettings(chatid, respmode):
    sql_com = 'INSERT INTO public."tChatSetting"(chatid, respmode)	VALUES ({0}, {1});'.format(chatid, respmode)
    cursor = conn.cursor()
    cursor.execute(sql_com)
    conn.commit()
    cursor.close()

def updarechatsettings(chatid, respmode):
    sql_com = 'update public."tChatSetting" set respmode = {0} where chatid = {1};'.format(respmode, chatid)
    cursor = conn.cursor()
    cursor.execute(sql_com)
    conn.commit()
    cursor.close()

def addnewcity(chatid, city):
    with conn.cursor() as cursor:
        sql_com = 'INSERT INTO public."tSavedCities"(chatid, city)	VALUES ({0}, \'{1}\');'.format(chatid, city)
        cursor.execute(sql_com)
        conn.commit()
        cursor.close()

def removecity(chatid, city):
    with conn.cursor() as cursor:
        sql_com = 'DELETE FROM public."tSavedCities" where chatid = {0} and city = \'{1}\';'.format(chatid, city)
        cursor.execute(sql_com)
        conn.commit()
        cursor.close()

def getAllRunes():
    sql_com = 'SELECT * FROM public."tRunes" ORDER BY id ASC'
    cursor = conn.cursor()
    cursor.execute(sql_com)
    records = cursor.fetchall()
    cursor.close()
    return records

def getRune(id: int):
    sql_com = 'SELECT * FROM public."tRunes" where id = {0}'.format(str(id))
    cursor = conn.cursor()
    cursor.execute(sql_com)
    records = cursor.fetchall()
    cursor.close()
    return records