# coding = utf-8

'''
@author = super_fazai
@File    : demo1.py
@Time    : 2017/8/7 17:54
@connect : superonesfazai@gmail.com
'''

import pdb

a = "aaa"
pdb.set_trace()
b = "bbb"
c = "ccc"
final = a + b + c
print(final)

#调试⽅法
# ** << 1 显示代码>>
#       l---->能够显示当前调试过程中的代码， 其实l表示list列出的意思
#       如下， 途中， -> 指向的地⽅表示要将要执⾏的位置
#       2 a = "aaa"
#       3 pdb.set_trace()
#       4 b = "bbb"
#       5 c = "ccc"
#       6 pdb.set_trace()
#       7 -> final = a + b + c
#       8 print(final)
# ** << 2 执⾏下⼀⾏代码>>
#       n---->能够向下执⾏⼀⾏代码， 然后停⽌运⾏等待继续调试 n表示next的意思
# ** << 3 查看变量的值>>
#       p---->能够查看变量的值， p表示prit打印输出的意思
#       例如：
#       p name 表示查看变量name的值