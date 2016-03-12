#-*-coding:utf-8*-
import MySQLdb

HOST = "127.0.0.1"
USER = "root"
PASSWD = "abcABC123"
DB = "mreader"
PORT = 3306


def Connect():
	con = MySQLdb.connect(
		host=HOST, user=USER, passwd =PASSWD, db=DB, port=PORT, charset = 'utf8')
        con.autocommit(1)
	return con

def Exec(con, query, param):
	cur = con.cursor()
	cur.execute(query, param)
	res = cur.fetchall()
	return res
