# -*- coding:utf-8 -*-
# file: ODBC.py
#
import odbc										# 导入odbc模块
con = odbc.odbc('podbc')								# 连接到数据库，即在数据源名中填写的名字
cursor = con.cursor()									# 创建cursor对象
cursor.execute('select id,name from people where id = 1')				# 执行SQL语句查询ID为1的记录
r = cursor.fetchall()									# 获得所有记录
print r											# 输出记录
cursor.execute('insert into people (name,age,sex) values (\'Jee\',21,\'female\')')	# 添加记录
cursor.execute('DELETE FROM people where id = 3')					# 删除ID为3的记录
con.commit()										# 提交事务
cursor.close()										# 关闭cursor
con.close()										# 关闭连接