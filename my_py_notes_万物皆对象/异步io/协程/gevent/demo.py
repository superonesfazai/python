# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

"""
notice: 当我们在受限于网络或IO的函数中使用gevent，这些函数会被协作式的调度, gevent的真正能力会得到发挥
Gevent处理了所有的细节， 来保证你的网络库会在可能的时候，隐式交出greenlet上下文的执行权。
"""

from gevent.pool import Pool as GeventPool
from gevent import joinall
from gevent import monkey
from gevent import Greenlet
from sys import argv
from time import sleep

# 猴子补丁
# 在进行IO操作时，默认切换协程
monkey.patch_all()

def run_Spider(url):
    '''假设我在这里调用了你的爬虫类接口'''
    # do anything what u want
    sleep(1.)

if __name__ == '__main__':
    # 假如你的url写在文件中 用第一个参数传进来
    # 限制并发数20
    pool = GeventPool(20)
    # 这里也可以用pool.map, 我这么写比较无脑
    tasks = []
    with open(argv[1], "r") as f:
        for line in f:
            tasks.append(pool.spawn(run_Spider, line.strip()))

    one_res = joinall(tasks)
    for g in one_res:
        res = g.get()
        print(res)

    print("finish")