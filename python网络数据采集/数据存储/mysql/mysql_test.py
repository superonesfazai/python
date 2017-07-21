#coding:utf-8

import pymysql

conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock',\
                       user='root', password='root654321', db='python')
cur = conn.cursor()
cur.execute('use python')

cur.execute('select * from people where name = "Jee"')
print(cur.fetchone())
cur.close()
conn.close()


