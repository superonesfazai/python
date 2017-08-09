# coding = utf-8

'''
@author = super_fazai
@File    : 僵尸进程.py
@Time    : 2017/8/9 09:30
@connect : superonesfazai@gmail.com
'''

# 子进程运行完成, 但是父进程迟迟没有进行回收
# 此时子进程实际上并没有退出, 其仍然占用着系统资源
# 这样的子进程称为僵尸进程

import os
import time

pid = os.fork()

if pid == 0:
    print("⼦进程%d:⼉⼦先⾏⼀步， ⽗亲保重啊。 。 。 " % os.getpid())
else:
    while True:
        print("⽗进程%d:吃个嫖赌中， 就是不管⼉⼦" % os.getpid())
        time.sleep(1)

'''
⽗进程5437:吃个嫖赌中， 就是不管⼉⼦
⼦进程5438:⼉⼦先⾏⼀步， ⽗亲保重啊。 。 。 
⽗进程5437:吃个嫖赌中， 就是不管⼉⼦
⽗进程5437:吃个嫖赌中， 就是不管⼉⼦
⽗进程5437:吃个嫖赌中， 就是不管⼉⼦
⽗进程5437:吃个嫖赌中， 就是不管⼉⼦
⽗进程5437:吃个嫖赌中， 就是不管⼉⼦
...
'''