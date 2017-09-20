# coding = utf-8

'''
@author = super_fazai
@File    : test_insert.py
@Time    : 2017/9/12 15:07
@connect : superonesfazai@gmail.com
'''

from MySQLdb import *

try:
    conn = connect(
        host='localhost',
        port=3306,
        db='python',
        user='root',
        passwd='lrf654321',
        # charset='utf-8',
    )

    cs1 = conn.cursor()
    tmp_name = input('请输入学生姓名: ')
    params = [tmp_name]
    count = cs1.execute('insert into students(name) values(%s)', params)
    print(count)
    conn.commit()
    cs1.close()
    conn.close()
except Exception as e:
    print(e)
# finally:
#     cs1.close()
#     conn.close()
