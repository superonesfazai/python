# coding = utf-8

'''
@author = super_fazai
@File    : 装饰器.py
@Time    : 2017/8/24 10:09
@connect : superonesfazai@gmail.com
'''
import time

def time_log(fun):
    def inner():
        print('开始运行时间:', time.ctime())
        fun()
        print('结束运行时间:', time.ctime())
    return inner

@time_log
def test():
    print('o' * 30)

test()

'''
测试结果:
开始运行时间: Thu Aug 24 10:14:37 2017
oooooooooooooooooooooooooooooo
结束运行时间: Thu Aug 24 10:14:37 2017
'''