#coding: utf-8

# 字符串无法改变,所以反转一个字符需要创建一个拷贝

a = 'ss dsf etw fgeg  '

print(a)

# 反转一个字符
rev_a = a[::-1]
print(rev_a)

# 按照单词反转字符
rev_a = a.split()   #把字符串转化为一个不含空格的list
# print(rev_a)
rev_a.reverse()     #反转list
# print(rev_a)
rev_a = ' '.join(rev_a)     #最后用join进行拼接
# print(rev_a)
print(rev_a)

# 上面一串等价于下面
rev_a = ' '.join(a.split()[::-1])

# 如果想逐词反转,但同时不改变原先的空格
import re
rev_a = re.split(r'(\s+)', a)   #切割字符串为单词列表
# print(rev_a)
rev_a.reverse()                 #反转
rev_a = ''.join(rev_a)          #单词列表转换为字符串
print(rev_a)

# 上面几行也等价于下面
rev_a = ''.join(re.split(r'(\s+)', a)[::-1])
print(rev_a)