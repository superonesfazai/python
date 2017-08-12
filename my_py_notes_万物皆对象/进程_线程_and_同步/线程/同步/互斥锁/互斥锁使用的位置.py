# coding = utf-8

'''
@author = super_fazai
@File    : 互斥锁使用的位置.py
@Time    : 2017/8/12 09:22
@connect : superonesfazai@gmail.com
'''

from threading import Thread, Lock
import time

g_num = 0
def test1():
    global g_num
    # 测试: 把锁放在外面
    # 对于线程锁使用的范围越小越好, 仅需保证操作的原子性即可, 也就是锁住出现资源竞争的语句就好
    # ** 所以还是建议在把锁放在eg.阻塞方式使用互斥锁.py的那个位置
    mutex.acquire()     # 这样放的位置表示只能等单个线程完成修改后解锁, 第二个线程才能进行修改
    for i in range(1000000):
        g_num += 1
    print("---test1---g_num=%d"%g_num)
    mutex.release()

def test2():
    global g_num
    mutex.acquire()
    for i in range(1000000):
        g_num += 1
    print("---test2---g_num=%d"%g_num)
    mutex.release()

# 创建⼀个互斥锁
# 这个锁默认是未上锁的状态
mutex = Lock()
p1 = Thread(target=test1)
p1.start()
p2 = Thread(target=test2)
p2.start()
print("---g_num=%d---"%g_num)
