# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

import gevent
from gevent import Greenlet
from gevent import monkey
import gevent.pool
import sys

# 在进行IO操作时，默认切换协程
monkey.patch_all()

def run_Spider(url):
    '''假设我在这里调用了你的爬虫类接口'''
    # do anything what u want
    pass

if __name__ == '__main__':
    # 假如你的url写在文件中 用第一个参数传进来
    # 限制并发数20
    pool = gevent.pool.Pool(20)
    # 这里也可以用pool.map, 我这么写比较无脑
    tasks = []
    with open(sys.argv[1], "r") as f:
        for line in f:
            tasks.append(pool.spawn(run_Spider, line.strip()))

    gevent.joinall(tasks)
    print("finish")