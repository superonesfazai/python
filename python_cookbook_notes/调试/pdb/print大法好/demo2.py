# coding = utf-8

'''
@author = super_fazai
@File    : demo2.py
@Time    : 2017/8/7 17:57
@connect : superonesfazai@gmail.com
'''

import pdb
a = "aaa"
pdb.set_trace()
b = "bbb"
c = "ccc"
pdb.set_trace()
final = a + b + c
print(final)

# ** << 4 将程序继续运⾏>>
#       c----->让程序继续向下执⾏， 与n的区别是n只会执⾏下⾯的⼀⾏代码， ⽽c会
#       像python xxxx.py⼀样 继续执⾏不会停⽌； c表示continue的意思
# ** << 5 set_trace()>>
#       如果程序中有多个set_trace()， 那么能够让程序在使⽤c的时候停留在下⼀个set_trace()位置处