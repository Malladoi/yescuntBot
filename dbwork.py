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

