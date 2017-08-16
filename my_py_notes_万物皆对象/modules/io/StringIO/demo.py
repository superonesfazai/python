# coding = utf-8

'''
@author = super_fazai
@File    : demo.py
@Time    : 2017/8/16 17:35
@connect : superonesfazai@gmail.com
'''

"""
很多时候数据读写, 不一定是文件, 也可能在内存读写

StringIO顾名思义就是在内存中读写str
"""

from io import StringIO

f = StringIO()
f.write('hello')
print(f)
f.write(' ')
print(f)
f.write('world!')
print(f.getvalue())     # 获取写入后的str

print('分界线'.center(40, '-'))

f = StringIO('hello!\nhi!\ngoodbye!')
while True:
    s = f.readline()
    if s == '':
        break
    print(s.strip())