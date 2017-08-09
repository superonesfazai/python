# coding = utf-8

'''
@author = super_fazai
@File    : multiprocessing_Process_demo2.py
@Time    : 2017/8/9 10:11
@connect : superonesfazai@gmail.com
'''

from multiprocessing import Process
import time
import os

#两个⼦进程将会调⽤的两个⽅法
def worker_1(interval):
    print("worker_1,⽗进程(%s),当前进程(%s)" % (os.getppid(),os.getpid()))
    t_start = time.time()
    time.sleep(interval) #程序将会被挂起interval秒
    t_end = time.time()
    print("worker_1,执⾏时间为'%0.2f'秒" % (t_end - t_start))

def worker_2(interval):
    print("worker_2,⽗进程(%s),当前进程(%s)" % (os.getppid(),os.getpid()))
    t_start = time.time()
    time.sleep(interval)
    t_end = time.time()
    print("worker_2,执⾏时间为'%0.2f'秒" % (t_end - t_start))


print("进程ID： %s"%os.getpid())       # 输出当前程序的ID
# 因为worker_1⽅法就⼀个interval参数， 这⾥传递⼀个整数2给它，
# 如果不指定name参数， 默认的进程对象名称为Process-N， N为⼀个递增的整数
p1 = Process(target=worker_1, args=(2,))     # 创建两个进程对象, target指向这个进程对象要执⾏的对象名称  # args后⾯的元组中, 是要传递给worker_1⽅法的参数
p2 = Process(target=worker_2, name="dongGe", args=(1,))
# 使⽤"进程对象名称.start()"来创建并执⾏⼀个⼦进程，
# 这两个进程对象在start后， 就会分别去执⾏worker_1和worker_2⽅法中的内容进程的创建-multiprocessing
p1.start()
p2.start()

print("p2.is_alive=%s" % p2.is_alive())       # 同时⽗进程仍然往下执⾏, 如果p2进程还在执⾏, 将会返回True

print("p1.name=%s" % p1.name)
print("p1.pid=%s" % p1.pid)
print("p2.name=%s" % p2.name)
print("p2.pid=%s" % p2.pid)

print('p1.is_alive=%s' % p1.is_alive())     # 如果不写这么一句p1.join(), 那么正如这一句的is_alive判断将会是True, 在shell(cmd) ⾥⾯调⽤这个程序时
p1.join()           # join括号中不携带参数, 表示⽗进程在这个位置要等待p1进程执⾏完成后, 再继续执⾏下⾯的语句, ⼀般⽤于进程间的数据同步
                    # 可以完整的看到这个过程, ⼤家可以尝试着将下⾯的这条语句改成p1.join(1)
                    # 因为p2需要2秒以上才可能执⾏完成, ⽗进程等待1秒很可能不能让p1完全执⾏完成,
                    # 所以下⾯的print会输出True, 即p1仍然在执⾏
print("p1.is_alive=%s" % p1.is_alive())

'''
测试结果:
进程ID： 4726
p2.is_alive=True
p1.name=Process-1
p1.pid=4727
p2.name=dongGe
p2.pid=4728
p1.is_alive=True
worker_1,⽗进程(4726),当前进程(4727)
worker_2,⽗进程(4726),当前进程(4728)
worker_2,执⾏时间为'1.00'秒
worker_1,执⾏时间为'2.00'秒
p1.is_alive=False
'''