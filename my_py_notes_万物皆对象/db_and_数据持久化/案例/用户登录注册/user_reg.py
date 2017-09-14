# coding = utf-8

'''
@author = super_fazai
@File    : user_reg.py
@Time    : 2017/9/14 18:19
@connect : superonesfazai@gmail.com
'''

from MySQLdb import *
from hashlib import sha1

try:
    # 接收用户输入
    uname = input('请输入用户名：')
    upwd = input('请输入密码：')

    # 对密码进行加密
    s1 = sha1()
    s1.update(upwd.encode())
    upwd_sha1 = s1.hexdigest()

    # 打开数据库连接
    conn = connect(
        host='localhost',
        port=3306,
        db = 'python',
        user = 'root',
        passwd = 'lrf654321',
    )

    cur = conn.cursor()

    # 判断用户名是否存在
    sql='select count(*) from py_users where uname=%s'
    params=[uname]
    cur.execute(sql, params)
    result = cur.fetchone()

    if result[0]==1:
        print('用户名已经存在，注册失败')
    else:
        # 用户名不存在
        sql='insert into py_users(uname, upwd) values(%s, %s)'
        params=[uname, upwd_sha1]
        result=cur.execute(sql, params)
        conn.commit()
        if result==1:
            print('注册成功')
        else:
            print('注册失败')

    cur.close()
    conn.close()
except Exception as e:
    print('注册失败，原因是：%s'%e)
# finally:
#     cur.close()
#     conn.close()