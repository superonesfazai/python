# coding = utf-8

'''
@author = super_fazai
@File    : os.wait_回收资源.py
@Time    : 2017/8/9 09:08
@connect : superonesfazai@gmail.com
'''

# 创建资源是一种资源分配, 当子进程被父进程创建后,在其执行完成结束后
# 应当由父进程及时回收

# os.wait()方法用来回收子进程占用的资源

import os
import time

pid = os.fork()

if pid == 0:
    for i in range(5):
        print('子进程%d工作中...' % os.getpid())
        time.sleep(1)

else:
    print('父进程%d waiting' % os.getpid())
    # wait()会有2个返回值
    # pid代表回收的子进程编号
    # result代表子进程结束退出时的状态, (0表示正常退出)
    pid, result = os.wait()     # 让父进程可以回收子进程的资源 同时阻塞 , 等待直到子进程执行完成后, wait函数才会调用完成
    print('父进程回收的子进程的pid:%s, result:%s' % (pid, result))
    print('finished')

'''
测试结果:
父进程5056 waiting
子进程5057工作中...
子进程5057工作中...
子进程5057工作中...
子进程5057工作中...
子进程5057工作中...
父进程回收的子进程的pid:5057, result:0
finished
'''