#coding: utf-8

params = {"server":"mpilgrim", "database":"master", "uid":"sa", "pwd":"secret"}

print('%(pwd)s' % params)
print('%(pwd)s is not a good password for %(uid)s' % params)
print('%(database)s of mind, %(database)s of body' % params)

'''
这种字符串格式化形式不用显式的值的 tuple,而是使用一个
dictionary, params 。并且标记也不是在字符串中的一个简单 %s ,而是包含
了一个用括号包围起来的名字。这个名字是 params dictionary 中的一个键
字,所以 %(pwd)s 标记被替换成相应的值 secret
'''