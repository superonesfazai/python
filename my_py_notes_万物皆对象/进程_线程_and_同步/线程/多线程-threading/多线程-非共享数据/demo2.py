# coding = utf-8

'''
@author = super_fazai
@File    : demo2.py
@Time    : 2017/8/9 17:38
@connect : superonesfazai@gmail.com
'''

import threading
from time import sleep

def test(sleepTime):
    num=1
    sleep(sleepTime)
    num+=1
    print('---(%s)--num=%d'%(threading.current_thread(), num))

t1 = threading.Thread(target = test,args=(5,))
t2 = threading.Thread(target = test,args=(1,))
t1.start()
t2.start()