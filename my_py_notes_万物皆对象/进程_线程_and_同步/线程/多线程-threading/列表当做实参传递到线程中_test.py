# coding = utf-8

'''
@author = super_fazai
@File    : 列表当做实参传递到线程中_test.py
@Time    : 2017/8/9 17:04
@connect : superonesfazai@gmail.com
'''

from threading import Thread
import time

def work1(nums):
    nums.append(44)
    print("----in work1---",nums)
def work2(nums):
    #延时⼀会， 保证t1线程中的事情做完
    time.sleep(1)
    print("----in work2---",nums)

g_nums = [11,22,33]
t1 = Thread(target=work1, args=(g_nums,))
t1.start()
t2 = Thread(target=work2, args=(g_nums,))
t2.start()

'''
测试结果:
----in work1--- [11, 22, 33, 44]
----in work2--- [11, 22, 33, 44]
'''