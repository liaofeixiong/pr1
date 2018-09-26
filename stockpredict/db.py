from mylog.mylogger import *
import mysql.connector

conf = {"host": "localhost",
        "user": "root",
        "password": "123456",
        "port": "3306",
        "database": "stock",
        "buffered": True
        }


def getconn(db_conf=conf):
    try:
        conn = mysql.connector.connect(**db_conf)
        info("get database connection ")
        return conn
    except Exception as e:
        info(e)
        raise e


def getcursor(conn):
    if conn == None:
        return None
    try:
        cursor = conn.cursor()
        info("get database cursor ")
        return cursor
    except Exception as e:
        error(e)
        raise e


def execute(sql):
    try:
        conn = getconn()
        cursor = getcursor(conn)
        cursor.execute(sql)
        l = None
        try:
            l = cursor.fetchall()
        except Exception as ex:
            error(ex)
        conn.commit()
        cursor.close()
        conn.close
        info("execute: "+sql)
        return l
    except Exception as e:
        error(e)
        raise e




if __name__ == "__main__":
    dzf_list = execute("select dzf from lsjy where symbol = '{}' order by day asc".format("sh600000"))
    print(dzf_list)
