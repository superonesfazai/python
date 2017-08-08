# coding = utf-8

'''
@author = super_fazai
@File    : 装饰器_test.py
@Time    : 2017/8/4 12:33
@connect : superonesfazai@gmail.com
'''
import datetime
# import time

# 定义一个修饰器, 实际上就是一个闭包
def log(fun):
    def inner():
        print(datetime.datetime.now().__str__())
        fun()
        print(datetime.datetime.now().__str__())
    return inner

# 使用装饰器
@log        # send() = log(send_mai)        send_mail == inner
def send_mail():
    print('send mail...')

send_mail()