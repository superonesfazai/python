# -*- coding:utf-8 -*-
# file: PyMySQL.py
#

import MySQLdb											# 导入MySQLdb模块
db = MySQLdb.connect(host='localhost',								# 连接到数据库，服务器为本机
		user='root',									# 用户为root
		passwd='root654321',								# 密码为root654321
		db='python')									# 数据库名为python
cur = db.cursor()										# 获得数据库游标
cur.execute('insert into people (name,age,sex) values (\'Jee\',21,\'F\')')			# 执行SQL语句
r = cur.execute('delete from people where age=20')						# 执行SQL语句
r = cur.execute('select * from people')								# 执行SQL语句
db.commit()											# 提交事务
r = cur.fetchall()										# 获取数据
print(r)												# 输出数据
cur.close()											# 关闭游标
db.close()											# 关闭数据库连接