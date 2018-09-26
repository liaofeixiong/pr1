from requests_html import HTMLSession
import mysql.connector
import logging

logger = logging.getLogger(__name__)
handle = logging.FileHandler("D:\\log.txt")
logger.addHandler(handle)
logger.setLevel(logging.INFO)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

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
        logger.error(str(e))
        exit(1)


def getcursor(conn):
    cursor = None
    try:
        cursor = conn.cursor()
        logger.info("cursor got")
        return cursor
    except Exception as e:
        logger.error(e.__context__)

        exit(1)


conn = getconn(connstr)
cursor = getcursor(conn)

def get_page_lsjy_info(stock_code, year, jidu):
    url = "http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/"
    url = url + stock_code + ".phtml?year=" + str(year) + "&jidu=" + str(jidu)
    session = HTMLSession()
    r = session.get(url)
    tables = r.html.xpath("//table[@id='FundHoldSharesTable']")
    if len(tables) > 0:
        table = tables[0]
    else:
        return []
    trs = table.xpath("//tr")
    del(trs[0])
    del(trs[0])
    jymx_list = list()
    for tr in trs:
        tds = tr.xpath("//td")
        jymx_list.append([stock_code, tds[0].text, tds[1].text, tds[2].text, tds[3].text, tds[4].text, tds[5].text])
    return jymx_list


def jymx_list_to_db(jymxlist):
    try:
        if len(jymxlist) < 1: return
        for jymx in jymxlist:
            sql = "insert into lsjy (stockCode,day,kpj,zgj,spj,zdj,jyl) values ('{}','{}',{},{},{},{},{})"
            sql = sql.format(*jymx)
            #print(sql)
            cursor.execute(sql)
        conn.commit()
        logger.info("{} record store to db".format(len(jymxlist)))
    except Exception as e:
        logger.error(str(e)+":::"+str(e.__context__)+":::"+str(e.__cause__))
        exit(1)






if __name__ == "__main__":
    # 测试
    #cursor.execute("select stockCode from stockInfo")
    #for row in cursor.fetchall():
        #stock_code = row[0]
    dayl= list()
    dayl.append()
        for jidu in range(1,4):
            l = get_page_lsjy_info(stock_code, 2018, jidu)
            jymx_list_to_db(l)
        print("code {} is stored".format(stock_code))
    print("all is stored")
    cursor.close()
    conn.close()