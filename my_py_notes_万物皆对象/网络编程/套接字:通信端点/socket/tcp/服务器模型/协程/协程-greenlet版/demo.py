# coding = utf-8

'''
@author = super_fazai
@File    : tasks.py
@Time    : 2017/8/18 12:27
@connect : superonesfazai@gmail.com
'''

# 为了更好使用协程来完成多任务，python中的greenlet模块对其封装，从而使得切换任务变的更加简单

from greenlet import greenlet
import time

def a():
    while True:
        print('--a--')
        gr1.swith()
        time.sleep(0.5)

def b():
    while True:
        print('--b--')
        gr2.swith()
        time.sleep(0.5)

gr1 = greenlet(a)
gr2 = greenlet(b)

gr1.swith() # 切换到gr1运行

'''
测试结果：
---A--
---B--
---A--
---B--
---A--
---B--
---A--
---B--
...
'''