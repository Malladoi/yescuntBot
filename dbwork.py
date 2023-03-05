import psycopg2


def getstickerresponses(conn:psycopg2.extensions.connection):
    sql_com = 'SELECT "text", sticker_id FROM public.tstickerresponce;'
    curr = conn.cursor()
    curr.execute(sql_com)
    records = curr.fetchall()
    curr.close()
    return records


def getadmins(conn:psycopg2.extensions.connection):
    sql_com = 'SELECT userid FROM public.tadmins;'
    curr = conn.cursor()
    curr.execute(sql_com)
    records = curr.fetchall()
    curr.close()
    return records


def newLog(conn:psycopg2.extensions.connection, application_name: str, host: str, level: str, message: str):
    sql_com = 'INSERT INTO public.log (application_name, host, "level", message) VALUES(\'{application_name}\',' \
              '\'{host}\',' \
              '\'{level}\',' \
              '\'{message}\');'.format(
        application_name=application_name,
        host=host,
        level=level,
        message=message
    )
    curr = conn.cursor()
    curr.execute(sql_com)
    conn.commit()
    curr.close()
