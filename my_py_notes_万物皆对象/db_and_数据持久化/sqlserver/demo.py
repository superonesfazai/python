# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@Time    : 2016/8/14 14:40
@connect : superonesfazai@gmail.com
'''

"""
使用pymssql进行中文操作时候可能会出现中文乱码，我解决的方案是：
文件头加上 # coding=utf8
sql语句中有中文的时候进行encode
   insertSql = "insert into WeiBo([UserId],[WeiBoContent],[PublishDate]) values(1,'测试','2012/2/1')".encode("utf8")
 连接的时候加入charset设置信息
    pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
"""

import pymssql

class MSSQL(object):
    """
    对pymssql简单的封装
    """
    def __init__(self, host, user, pwd, db):    # 类的构造函数，初始化数据库连接ip或者域名，以及用户名，密码，要连接的数据库名称
        self.host =host
        self.user = user
        self.pwd = pwd
        self.db = db

    def get_connect(self):
        '''
        得到数据库连接信息
        :return: conn.cursor()
        '''
        if not self.db:
            raise(NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset='utf8')
        cur = self.conn.cursor()  # 将数据库连接信息，赋值给cur。
        if not cur:
            raise(NameError, "连接数据库失败")
        else:
            return cur

    def exec_query(self, sql):
        '''
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

        调用示例：
                ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
                result_list = ms.exec_query("SELECT id,NickName FROM WeiBoUser")
                for (id, nick_name) in result_list:
                    print(str(id), nick_name)
        :param sql:
        :return:
        '''
        cur = self.get_connect()        # 获得数据库连接信息
        cur.execute(sql)                # 执行Sql语句
        result_list = cur.fetchall()    # 获得所有的查询结果

        # 查询完毕后必须关闭连接
        self.conn.close()   # 返回查询结果
        return result_list

    def exec_non_query(self, sql):
        '''
        执行非查询语句
        :param sql:
        :return:
        '''
        cur = self.get_connect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

def main():
    ms = MSSQL(
        host='',
        user='',
        pwd='',
        db=''
    )

    sql = 'select * from test'
    result_list = ms.exec_query(sql)
    print(result_list)
    params = [
        'cc',
        '阿诚',
    ]
    # sql2 = 'insert into test([id], [name]) values(%s, %s)'.format(params).encode('utf-8')
    # ms.exec_non_query(sql2)

    cur = ms.get_connect()
    sql2 = 'insert into test(id, name) values(%s, %s)'

    cur.execute(sql2, ('cc', '阿诚'))
    ms.conn.commit()
    cur.close()

    result_list = ms.exec_query(sql)
    print(result_list)

main()