# coding = utf-8

'''
@author = super_fazai
@File    : 在多线程中修改全局变量_demo.py
@Time    : 2017/8/9 16:59
@connect : superonesfazai@gmail.com
'''

from threading import Thread
import time

g_num = 100
def work1():
    global g_num
    for i in range(3):
        g_num += 1
        print("----in work1, g_num is %d---" % g_num)

def work2():
    global g_num
    print("----in work2, g_num is %d---" % g_num)
    print("----线程创建之后g_num is %d---" % g_num)

print("----线程创建之前g_num is %d---" % g_num)
t1 = Thread(target=work1)
t1.start()
#延时⼀会， 保证t1线程中的事情做完
time.sleep(1)
t2 = Thread(target=work2)
t2.start()

'''
测试结果:
----线程创建之前g_num is 100---
----in work1, g_num is 101---
----in work1, g_num is 102---
----in work1, g_num is 103---
----in work2, g_num is 103---
----线程创建之后g_num is 103---
'''