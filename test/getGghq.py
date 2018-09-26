import mysql.connector
import datetime
from requests_html import HTMLSession


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

        return conn
    except Exception as e:
        print(e)


def getcursor(conn):
    cursor = None
    try:
        cursor = conn.cursor()
        return cursor
    except Exception as e:
        print(e)


conn = getconn(connstr)
cursor = getcursor(conn)


# 获取当前日期，及当天是否已获取个股行情
def istodayget():
    today = datetime.date.today().strftime("%Y-%M-%d")
    cursor.execute("select * from gghq where day = " + today)
    result = True
    if cursor.rowcount < 1:
        result = False
    return result


# 爬取个股行情
def getgghq():
    gglist = list()
    today = datetime.date.today().strftime("%Y-%m-%d")
    session = HTMLSession()
    r = session.get("http://q.10jqka.com.cn/index/index/board/hs/field/zdf/order/desc/page/1/ajax/1/")
    pageinfo = r.html.xpath("//span")[0].text
    # 页面总数
    pagenum = pageinfo.split("/")[1]
    for index in range(1, int(pagenum)+1):
        url = "http://q.10jqka.com.cn/index/index/board/hs/field/zdf/order/desc/page/" + str(index) + "/ajax/1/"
        r = session.get(url)
        trs = r.html.xpath("//tr")
        del(trs[0])
        for tr in trs:
            tds = tr.xpath("//td")
            stockCode = tds[1].text
            stockName = tds[2].text
            xj = tds[3].text
            dzf = tds[4].text
            gg = [today, stockCode, stockName, xj, dzf]
            gglist.append(gg)
    return gglist


# 个股行情存入数据库
def gghqstore(gglist):
    if istodayget():
        print("today is got")
        exit(0)
    for gg in gglist:
        try:
            float(gg[3])
        except Exception as e:
            gg[3] = "0"
        try:
            float(gg[4])
        except Exception as e:
            gg[4] = "0"
        insertstr = 'insert into gghq (day,stockCode,stockName,xj,dzf) values ("' + gg[0] + '","' + gg[1] + '",'
        insertstr = insertstr + '"' + gg[2] + '",' + gg[3] + ',' + gg[4] + ')'
        print(insertstr)
        cursor.execute(insertstr)
    conn.commit()



# 调试代码
gglist = getgghq()
    #[["2018-08-27", "603590", "N康辰", "35.05", "44.00"], ]
gghqstore(gglist)
cursor.close()
conn.close