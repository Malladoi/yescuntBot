import os
import psycopg2
from psycopg2 import pool

DATABASE_URL = os.environ['DATABASE_URL']

# conn = psycopg2.connect(DATABASE_URL, sslmode='require')
connpool = psycopg2.pool.SimpleConnectionPool(1, 100, DATABASE_URL, sslmode='require')

def getcitiesforchat(chatid):
    sql_com = 'SELECT chatid, city	FROM public."tSavedCities" where chatid = {0};'.format(chatid)
    conn = connpool.getconn()
    cursor = conn.cursor()
    cursor.execute(sql_com)
    records = cursor.fetchall()
    cursor.close()
    connpool.putconn(conn)
    return records

def getchatsettings(chatid):
    sql_com = 'SELECT chatid, respmode	FROM public."tChatSetting" where chatid = {0};'.format(chatid)
    conn = connpool.getconn()
    cursor = conn.cursor()
    cursor.execute(sql_com)
    records = cursor.fetchall()
    cursor.close()
    connpool.putconn(conn)
    return records

def setchatsettings(chatid, respmode):
    sql_com = 'INSERT INTO public."tChatSetting"(chatid, respmode)	VALUES ({0}, {1});'.format(chatid, respmode)
    conn = connpool.getconn()
    cursor = conn.cursor()
    cursor.execute(sql_com)
    conn.commit()
    connpool.putconn(conn)
    cursor.close()

def updarechatsettings(chatid, respmode):
    sql_com = 'update public."tChatSetting" set respmode = {0} where chatid = {1};'.format(respmode, chatid)
    conn = connpool.getconn()
    cursor = conn.cursor()
    cursor.execute(sql_com)
    conn.commit()
    connpool.putconn(conn)
    cursor.close()

def addnewcity(chatid, city):
    conn = connpool.getconn()
    with conn.cursor() as cursor:
        sql_com = 'INSERT INTO public."tSavedCities"(chatid, city)	VALUES ({0}, \'{1}\');'.format(chatid, city)
        cursor.execute(sql_com)
        conn.commit()
        connpool.putconn(conn)
        cursor.close()

def removecity(chatid, city):
    conn = connpool.getconn()
    with conn.cursor() as cursor:
        sql_com = 'DELETE FROM public."tSavedCities" where chatid = {0} and city = \'{1}\';'.format(chatid, city)
        cursor.execute(sql_com)
        conn.commit()
        connpool.putconn(conn)
        cursor.close()

def getAllRunes():
    conn = connpool.getconn()
    sql_com = 'SELECT * FROM public."tRunes" ORDER BY id ASC'
    cursor = conn.cursor()
    cursor.execute(sql_com)
    records = cursor.fetchall()
    cursor.close()
    connpool.putconn(conn)
    return records

def getRune(id: int):
    conn = connpool.getconn()
    sql_com = 'SELECT * FROM public."tRunes" where id = {0}'.format(str(id))
    cursor = conn.cursor()
    cursor.execute(sql_com)
    records = cursor.fetchall()
    cursor.close()
    connpool.putconn(conn)
    return records

def getRunewords():
    conn = connpool.getconn()
    sql_com = "SELECT distinct rw.*, '[' || STRING_AGG(r.title, ';') OVER(PARTITION BY rw.id) || ']' as runes " \
              "FROM public.\"tRuneToRunewordLink\" l " \
              "join public.\"tRuneWords\" rw on rw.id  =  l.id_runeword	" \
              "join public.\"tRunes\" r on r.id  =  l.id_rune " \
              "order by rw.name asc"
    cursor = conn.cursor()
    cursor.execute(sql_com)
    records = cursor.fetchall()
    cursor.close()
    connpool.putconn(conn)
    return records

def getRunewords4Chat(chatid:int):
    conn = connpool.getconn()
    sql_com = "SELECT distinct rw.*, '[' || STRING_AGG(r.title, ';') OVER(PARTITION BY rw.id) || ']' as runes " \
              "FROM public.\"tRuneToRunewordLink\" l " \
              "join public.\"tRuneWords\" rw on rw.id  =  l.id_runeword	" \
              "join public.\"tRunes\" r on r.id  =  l.id_rune " \
              "order by rw.name asc"
    cursor = conn.cursor()
    cursor.execute(sql_com)
    records = cursor.fetchall()
    cursor.close()
    connpool.putconn(conn)
    return records

def getRuneSettinds(chatid):
    conn = connpool.getconn()
    sql_com = 'SELECT runeid FROM public."tChatRunesSettings" where chatid = {0}'.format(chatid)
    cursor = conn.cursor()
    cursor.execute(sql_com)
    records = cursor.fetchall()
    cursor.close()
    connpool.putconn(conn)
    return records

def setRuneSettings(chatid, runeid):
    conn = connpool.getconn()
    cursor = conn.cursor()
    try:
        sql_com = "INSERT INTO public.\"tChatRunesSettings\"(chatid, runeid) VALUES (%s, %s)"
        cursor.execute(sql_com, (chatid, runeid))
        conn.commit()
    except:
        conn.rollback()
        sql_com = "DELETE FROM public.\"tChatRunesSettings\" WHERE chatid = %s and runeid = %s"
        cursor.execute(sql_com, (chatid, runeid))
    conn.commit()
    connpool.putconn(conn)
    cursor.close()


def getRunewordsByChatId(chatid: int):
    conn = connpool.getconn()
    sql_com = "with pre as (SELECT runeid " \
              "FROM public.\"tChatRunesSettings\" " \
              "where chatid = {0})," \
              "pre_sel as (" \
              "SELECT id_runeword, " \
              "l.id_rune, " \
              "count(id_rune) " \
              "over(partition by id_runeword) as total_cnt, " \
              "count(runeid) over(partition by id_runeword) as match_cnt " \
              "FROM public.\"tRuneToRunewordLink\" l " \
              "left join pre p on l.id_rune = p.runeid) " \
              "select distinct rw.*, STRING_AGG(r.title, '+') OVER(PARTITION BY ps.id_runeword) as runes " \
              "from public.\"tRuneWords\" rw " \
              "join pre_sel ps on ps.id_runeword = rw.id " \
              "join public.\"tRunes\" r on r.id = ps.id_rune " \
              "where total_cnt = match_cnt".format(chatid)
    cursor = conn.cursor()
    cursor.execute(sql_com)
    records = cursor.fetchall()
    cursor.close()
    connpool.putconn(conn)
    return records