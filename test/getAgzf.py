from requests_html import HTMLSession
import datetime
import re
import mysql.connector
import logging

formatstr = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#logging.basicConfig(level=logging.INFO, filename="D:\\log.txt", format=logging.Formatter(formatstr))
logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler("D:\\log.txt"))
logger.setLevel(logging.INFO)
def error(e):
    logger.error(str(e))
    logger.error(str(e.__cause__))
    logger.error(str(e.__context__))

def info(message):
    logger.info(str(message))

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
        #info("db connection got")
        return conn
    except Exception as e:
        error(e)
        exit(1)


conn = getconn(connstr)

def getcursor(conn):
    cursor = None
    try:
        cursor = conn.cursor()
        #info("cursor got")
        return cursor
    except Exception as e:
        error(e)
        exit(1)


cursor = getcursor(conn)


def get_agzf_page_list(page_num):
    session = HTMLSession()
    url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page="
    url = url + str(page_num) + "&num=80&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=sort"
    r = session.get(url)
    l = re.split("[\[\]{}]", r.content.decode("gbk"))
    fl = filter(lambda x: len(x) > 3, l)
    ff = [string.replace('"', "") for string in fl]
    print("get page {0}".format(page_num))
    return ff

def store_agzf_page_list(page_list):
    try:
        today = datetime.date.today().strftime("%Y-%m-%d")
        for line in page_list:
            row = list()
            row.append('"' + today + '"')
            for index, col in enumerate(line.split(",")):
                if index < 3 or index ==15:
                    row.append('"' + col.split(":")[1] + '"')
                else:
                    row.append(col.split(":")[1])
            sql = 'insert into agzf values ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},  '
            sql = sql + "{}, {}, {})"
            sql = sql.format(*row)
            #print(sql)
            cursor.execute(sql)
        conn.commit()

    except Exception as e:
        error(e)


if __name__ == "__main__":
    for index in range(1, 46):
        l = get_agzf_page_list(index)
        store_agzf_page_list(l)

    cursor.close()
    conn.close()