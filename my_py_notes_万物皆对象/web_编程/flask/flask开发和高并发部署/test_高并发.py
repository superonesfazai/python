# coding:utf-8

'''
@author = super_fazai
@File    : test_高并发.py
@Time    : 2017/10/21 21:37
@connect : superonesfazai@gmail.com
'''

# import urllib
from urllib.request import urlopen
import json
import time

url = 'http://localhost:5000/'

while True:
    t1 = time.time()
    print(t1)
    res = json.loads(urlopen(url, timeout=10).read().decode('utf-8'))
    dt = time.time() - t1
    print("耗时"+"%.2f秒" % dt)
    print(res)
    time.sleep(0.01)