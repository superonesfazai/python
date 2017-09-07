# coding = utf-8

'''
@author = super_fazai
@File    : process_youyuan_mysql.py
@Time    : 2017/9/7 17:28
@connect : superonesfazai@gmail.com
'''

"""
存入mysql
    1. 启动mysql：mysql.server start
    2. 登录到root用户：mysql -uroot -p
    3. 创建数据库youyuan:create database youyuan;
    4. 切换到指定数据库：use youyuan
    5. 创建表beijing_18_25以及所有字段的列名和数据类型
    6. 执行下面程序
"""

import json
import redis
import MySQLdb

def main():
    # 指定redis数据库信息
    rediscli = redis.StrictRedis(host='192.168.199.108', port = 6379, db = 0)
    # 指定mysql数据库
    mysqlcli = MySQLdb.connect(host='127.0.0.1', user='power', passwd='xxxxxxx', db = 'youyuan', port=3306, use_unicode=True)

    while True:
        # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
        source, data = rediscli.blpop(["youyuan:items"])
        item = json.loads(data)

        try:
            # 使用cursor()方法获取操作游标
            cur = mysqlcli.cursor()
            # 使用execute方法执行SQL INSERT语句
            cur.execute("INSERT INTO beijing_18_25 (username, crawled, age, spider, header_url, source, pic_urls, monologue, source_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s )", [item['username'], item['crawled'], item['age'], item['spider'], item['header_url'], item['source'], item['pic_urls'], item['monologue'], item['source_url']])
            # 提交sql事务
            mysqlcli.commit()
            #关闭本次操作
            cur.close()
            print("inserted %s" % item['source_url'])
        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

if __name__ == '__main__':
    main()
