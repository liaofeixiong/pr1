from mylog.mylogger import *
from stockpredict import db

conn = db.getconn()
cursor = db.getcursor(conn)


def store_stock_dzf(symbol="sh600000"):
    cursor.execute("select dzf from lsjy where symbol = '{}' order by day asc".format(symbol))
    dzf_list = cursor.fetchall()
    cur = 0
    for dzf in dzf_list:
        dzf = float(dzf[0])
        if cur == 0:
            if dzf > 0 :
                cur = 1
            elif dzf < 0:
                cur = -1
        elif cur > 0:
            if dzf > 0:
                cur += 1
            elif dzf < 0:
                sql = "insert into dzfnum values (null,'{}',{})".format(symbol, cur)
                cursor.execute(sql)
                cur = -1
        elif cur < 0:
            if dzf > 0:
                sql = "insert into dzfnum values (null,'{}',{})".format(symbol, cur)
                cursor.execute(sql)
                cur = 1
            elif dzf < 0:
                cur -= 1




if __name__ == "__main__":
    symbol_list = db.execute("select symbol from stockinfo")
    for (symbol, ) in symbol_list:
        store_stock_dzf(symbol)
        conn.commit()
        info("{} is sucess".format(symbol))
    cursor.close()
    conn.close()
