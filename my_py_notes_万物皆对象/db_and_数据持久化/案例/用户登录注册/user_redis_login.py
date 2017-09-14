# coding = utf-8

'''
@author = super_fazai
@File    : user_redis_login.py
@Time    : 2017/9/14 20:35
@connect : superonesfazai@gmail.com
'''

from MySQLdb import *
from hashlib import sha1
from redis import *

def mysql_login():
    try:
        # mongodb中没有则到mysql中查询
        # 根据用户名查询密码
        sql = 'select upwd from py_users where uname=%s'
        params = [uname]
        conn = connect(
            host='localhost',
            port=3306,
            db='python',
            user='root',
            passwd='lrf654321'
        )

        cur = conn.cursor()
        cur.execute(sql, params)
        result = cur.fetchone()

        if result == None:
            print('用户名错误, 登录失败, 数据来源于mysql')
        else:
            # 当查询到用户及对应的密码时, 将数据加入到redis, 以供后续登录使用
            r.set(uname, upwd_sha1)
            # 判断密码是否正确
            if result[0] == upwd_sha1:
                print('登录成功, 数据来源于mysql')
            else:
                print('密码错误, 登录失败，数据来源于mysql')
        cur.close()
        conn.close()

    except Exception as e:
        print('登录失败，错误原因: %s' % e)

try:
    #接收输入用户名、密码
    uname = input('请输入用户名：')
    upwd = input('请输入密码：')

    #对密码加密
    s1 = sha1()
    s1.update(upwd.encode())
    upwd_sha1 = s1.hexdigest()

    #根据用户名查询密码
    #先到redis上查，没有再到mysql上查
    r = StrictRedis()
    result = r.get(uname)

    if result == None:
        mysql_login()
    else:
        #redis中找到了这个用户名的数据
        if result==upwd_sha1:
            print('登录成功，数据来源于redis')
        else:
            print('密码错误，登录失败，数据来源于redis')
except Exception as e:
    print('登录失败，错误原因：%s' % e)
