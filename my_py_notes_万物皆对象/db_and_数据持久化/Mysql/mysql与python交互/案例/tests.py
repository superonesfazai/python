# coding = utf-8

'''
@author = super_fazai
@File    : tests.py
@Time    : 2017/9/12 15:33
@connect : superonesfazai@gmail.com
'''

from MySQLdb import *

class tests():
    # 初始化对象, 提供连接数据库的参数
    def __init__(self, host, port, db, user, passwd):   # charset='utf8'
        self.__host = host
        self.__port = port
        self.__db = db
        self.__user = user
        self.__passwd = passwd
        # self.__charset = charset

    # 建立连接并获得cursor对象
    def __open(self):
        self.__conn = connect(
            host=self.__host,
            port=self.__port,
            db=self.__db,
            user=self.__user,
            passwd=self.__passwd,
            # charset=self.__charset
        )

        self.__cursor = self.__conn.cursor()

    # 关闭cursor及conn对象
    def __close(self):
        self.__cursor.close()
        self.__conn.close()

    # 查询所有未删除的问题
    def select(self):
        try:
            self.__open()

            # 构造select语句
            sql = 'select * from tests where isdelete=0'
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()

            # 判断结果并返回
            if len(result) > 0:
                return result
            else:
                return None
        except Exception as e:
            print(e)
        finally:
            self.__close()

    # 执行insert语句
    def insert(self, title):
        try:
            self.__open()

            # 构造insert语句及参数
            sql = 'insert into tests(title) values(%s)'
            params = [title]
            result = self.__cursor.execute(sql, params)
            self.__conn.commit()

            # 判断是否成功
            if result == 1:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        finally:
            self.__close()

    # 执行update语句
    def update(self, title, tid):
        try:
            self.__open()

            # 构造update语句及参数
            sql = 'update tests set title=%s where id=%s'
            params = [title, tid]
            result = self.__cursor.execute(sql, params)
            self.__conn.commit()

            # 判断是否成功
            if result == 1:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        finally:
            self.__close()

    # 执行删除操作: 使用逻辑删除
    def delete(self, tid):
        try:
            self.__open()

            # 构造逻辑删除的语句
            sql = 'update tests set isdelete = 1 where id = %s'
            params = [tid]
            result = self.__cursor.execute(sql, params)
            self.__conn.commit()

            # 判断是否成功
            if result == 1:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        finally:
            self.__close()


