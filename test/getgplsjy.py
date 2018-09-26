import mysql.connector
from requests_html import HTMLSession
import logging

formatstr = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=formatstr)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("D:\\log.txt"))
#log info
def info(msg):
    logger.info(str(msg))


#log exception
def error(msg):
    logger.error(str(msg))
    if isinstance(msg, Exception):
        logger.error(msg.__context__)
        logger.error(msg.__cause__)



connstr = {"host": "127.0.0.1",
           "user": "root",
           "password": "123456",
           "database": "stock",
           "port": "3306",
           'buffered': True}


def getconn(connectstring):
    conn = None
    try:
        conn = mysql.connector.connect(**connectstring)
        logger.info("db connection got")
        return conn
    except Exception as e:
        error(e)
        exit(1)


def getcursor(conn):
    cursor = None
    try:
        cursor = conn.cursor()
        info("cursor got")
        return cursor
    except Exception as e:
        error(e)
        exit(1)

def get_symbol_list(cursor):
    l = list()
    try:
        cursor.execute("select symbol from stockinfo order by symbol")
        for row in cursor:
            l.append(row[0])
    except Exception as e:
        error(e)
    finally:
        return l

def get_day_list(cursor):
    l = list()
    try:
        cursor.execute("select distinct(day) from daylist order by day")
        for row in cursor:
            l.append(str(row[0]))
        l.append("2018-09-07")
        l.append("2018-09-10")

    except Exception as e:
        error(e)
    finally:
        return l



def store_symbol_page(symbol, day, cursor):
    s = HTMLSession()
    url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?symbol={}&date={}"
    r = s.get(url.format(symbol,day))
    tds = r.html.xpath('//*[@id="quote_area"]/div[2]/table//td')
    tds = tds[1:16:2]
    col_list = list()
    col_list.append(str(symbol))
    col_list.append(str(day))
    for index, td in enumerate(tds):
        text = td.text
        if index == 1:
            text = text[0:len(text)-1]
        elif index > 7:
            break
        col_list.append(text)
    if float(col_list[2]) == 0.0 and float(col_list[3]) == 0.0 and float(col_list[4]) == 0.0: return
    sql = 'insert into lsjy values ("{}","{}",{},{},{},{},{},{},{},{})'.format(*col_list)
    try:
        cursor.execute(sql)
    except Exception as e:
        error(e)

f = open("D:\\fails.txt", "a")
def w(str):
    f.writelines(str)


if __name__ == "__main__":
    conn = getconn(connstr)
    cursor = getcursor(conn)
    dayl = list()
    #dayl.append("2018-09-19")
    dayl.append("2018-09-21")
    for symbol in get_symbol_list(cursor):
        #for day in get_day_list(cursor):
        for day in dayl:
            try:
                store_symbol_page(symbol, day, cursor)
                #info("{},{} success".format(symbol,day))
            except Exception as e:
                error(e)
                w(str(symbol)+","+str(day))
        info(symbol+" is success")
        conn.commit()

    cursor.close()
    conn.close

