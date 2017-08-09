# coding = utf-8

'''
@author = super_fazai
@File    : Pool_apply堵塞式_test.py
@Time    : 2017/8/9 11:11
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

po = Pool(3)        # 定义一个进程池, 最大进程数为3
for i in range(0, 10):
    po.apply(worker, (i,))

print('---start---')
po.close()      # 关闭进程池, 关闭后po 不再接收新的请求
po.join()       # 等待po中所有子进程执行完成，必须放在close()语句之后
print('---end---')

'''
测试结果:
0开始执行, 进程号为6084
0 执行完毕, 耗时1.189
1开始执行, 进程号为6085
1 执行完毕, 耗时1.130
2开始执行, 进程号为6086
2 执行完毕, 耗时0.492
3开始执行, 进程号为6084
3 执行完毕, 耗时0.944
4开始执行, 进程号为6085
4 执行完毕, 耗时0.507
5开始执行, 进程号为6086
5 执行完毕, 耗时1.065
6开始执行, 进程号为6084
6 执行完毕, 耗时0.448
7开始执行, 进程号为6085
7 执行完毕, 耗时1.463
8开始执行, 进程号为6086
8 执行完毕, 耗时0.950
9开始执行, 进程号为6084
9 执行完毕, 耗时0.317
---start---
---end---
'''