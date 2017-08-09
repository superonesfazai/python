# coding = utf-8

'''
@author = super_fazai
@File    : 进程池_Pool_test.py
@Time    : 2017/8/9 10:54
@connect : superonesfazai@gmail.com
'''

from multiprocessing import Pool
import os, time, random

def worker(msg):
    t_start = time.time()
    print('%s开始执行, 进程号为%d' % (msg, os.getpid()))
    # random.random()随机生成0-1之间的浮点数
    time.sleep(random.random() * 2)
    t_stop = time.time()
    print(msg, '执行完毕, 耗时%0.3f' % (t_stop-t_start))

po = Pool(3)        # 定义一个进程池, 最大进程数为3, 参数表示进程池预先创建的进程个数
for i in range(0, 10):
    # Pool.apply_async(要调用的目标, (传递给目标的参数元组,))
    # 每次循环将会用空闲的子进程去调用目标
    po.apply_async(worker, (i,))

print('---start---')
po.close()      # 关闭进程池, 关闭后po 不再接收新的请求
po.join()       # 等待po中所有子进程执行完成，必须放在close()语句之后
print('---end---')

'''
测试结果:
---start---
0开始执行, 进程号为6049
1开始执行, 进程号为6050
2开始执行, 进程号为6051
1 执行完毕, 耗时0.957
3开始执行, 进程号为6050
0 执行完毕, 耗时1.087
4开始执行, 进程号为6049
2 执行完毕, 耗时1.616
5开始执行, 进程号为6051
3 执行完毕, 耗时1.226
6开始执行, 进程号为6050
4 执行完毕, 耗时1.518
7开始执行, 进程号为6049
5 执行完毕, 耗时1.944
8开始执行, 进程号为6051
6 执行完毕, 耗时1.627
9开始执行, 进程号为6050
7 执行完毕, 耗时1.538
8 执行完毕, 耗时0.583
9 执行完毕, 耗时1.381
---end---
'''