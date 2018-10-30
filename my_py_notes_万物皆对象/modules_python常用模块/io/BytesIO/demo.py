# coding = utf-8

'''
@author = super_fazai
@File    : tasks.py
@Time    : 2017/8/16 17:42
@connect : superonesfazai@gmail.com
'''

"""
BytesIO实现了在内存中读写bytes
"""

from io import BytesIO

f = BytesIO()
f.write('中文'.encode('utf-8'))   # 注意写入的经过utf8编码的bytes
print(f.getvalue())

print('分割线'.center(40, '-'))

f = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
print(f.read())