# coding = utf-8

'''
@author = super_fazai
@File    : test_select.py
@Time    : 2017/9/12 15:21
@connect : superonesfazai@gmail.com
'''

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
    count = cs1.execute('insert into students(name) values("张良")')
    conn.commit()
    print(count)
    # 查询一行数据
    cs1.execute('select * from students where id=2')
    result = cs1.fetchone()
    print(result)
    # 查询多行数据
    cs1.execute('select * from students')
    result = cs1.fetchall()
    print(result)
    cs1.close()
    conn.close()
except Exception as e:
    print(e)
# finally:
#     cs1.close()
#     conn.close()
