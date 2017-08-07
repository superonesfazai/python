# coding = utf-8

'''
@author = super_fazai
@File    : demo3.py
@Time    : 2017/8/7 17:59
@connect : superonesfazai@gmail.com
'''

#coding=utf-8
import pdb
def combine(s1,s2):
    s3 = s1 + s2 + s1
    s3 = '"' + s3 +'"'
    return s3
a = "aaa"
pdb.set_trace()
b = "bbb"
c = "ccc"
final = combine(a,b)
print(final)
# ** << 6 设置断点>>
#       b---->设置断点， 即当使⽤c的时候， c可以在遇到set_trace()的时候停⽌，
#       也可以在遇到标记有断点的地⽅停⽌； b表示break的意思
#       例如：
#       b 11 在第11⾏设置断点， 注意这个11可以使⽤l来得到
#       (Pdb) l
#       4 s3 = s1 + s2 + s1
#       5 s3 = '"' + s3 +'"'
#       6 return s3
#       7 a = "aaa"
#       8 pdb.set_trace()
#       9 -> b = "bbb"
#       10 c = "ccc"
#       11 final = combine(a,b)
#       12 print final
#       [EOF]
#       (Pdb) b 11
#       Breakpoint 1 at /Users/wangmingdong/Desktop/test3.py:11
#       (Pdb) c
#       > /Users/wangmingdong/Desktop/test3.py(11)<module>()
#       -> final = combine(a,b)
#       (Pdb) l
#       6 return s3
#       7 a = "aaa"
#       8 pdb.set_trace()
#       9 b = "bbb"
#       10 c = "ccc"
#       11 B-> final = combine(a,b)
#       12 print final
# ** << 7 进⼊函数继续调试>>
#       s---->进⼊函数⾥⾯继续调试， 如果使⽤n表示把⼀个函数的调⽤当做⼀条语句
#       执⾏过去， ⽽使⽤s的话， 会进⼊到这个函数 并且停⽌
#       例如
#       (Pdb) l
#       6 return s3
#       7 a = "aaa"
#       8 pdb.set_trace()
#       9 b = "bbb"
#       10 c = "ccc"
#       11 B-> final = combine(a,b)
#       12 print final
#       [EOF]
#       (Pdb) s
#       --Call--
#       > /Users/wangmingdong/Desktop/test3.py(3)combine()
#       -> def combine(s1,s2):
#       (Pdb) l
#       1 import pdb
#       2
#       3 -> def combine(s1,s2):
#       4 s3 = s1 + s2 + s1
#       5 s3 = '"' + s3 +'"'
#       6 return s3
#       7 a = "aaa"
#       8 pdb.set_trace()
#       9 b = "bbb"
#       10 c = "ccc"
#       11 B final = combine(a,b)
#       (Pdb)
# ** << 8 查看传递到函数中的变量>>
#       a---->调⽤⼀个函数时， 可以查看传递到这个函数中的所有的参数； a表示arg的意思
#       例如：
#       (Pdb) l
#       1 #coding=utf-8
#       2 import pdb
#       3
#       4 -> def combine(s1,s2):
#       5 s3 = s1 + s2 + s1
#       6 s3 = '"' + s3 +'"'
#       7 return s3
#       8
#       9 a = "aaa"
#       10 pdb.set_trace()
#       11 b = "bbb"
#       (Pdb) a
#       s1 = aaa
#       s2 = bbb
# ** << 9 执⾏到函数的最后⼀步>>
#       r----->如果在函数中不想⼀步步的调试了， 只是想到这个函数的最后⼀条语句
#       那个位置， ⽐如return语句， 那么就可以使⽤r； r表示return的意思