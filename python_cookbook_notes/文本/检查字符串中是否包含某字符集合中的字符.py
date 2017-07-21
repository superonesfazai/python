#coding:utf-8

# 检查字符串中是否出现某字符集合中的字符

# 最简单的方法
def contains_any(seq, aset):
    # 检查序列seq是否含有aset中的项
    for c in seq:
        if c in aset: return True
    return False

# # 也可用itertools模块来提高性能
# # 由于itertools模块中取消了'.ifilter()',所以下面的方法失效
# import itertools
# def contains_any(seq, aset):
#     for item in itertools.ifilter(aset.__contains__, seq):
#         return True
#     return False

a = [1, 2, 4]
b = [3]
c = [1, 2]
print(contains_any(a, b))
print(contains_any(a, c))

# 还有纯粹基于list的方法set().difference()
print(set(a).difference(c))     # set(a).difference(b) 的语义是返回a中所有不属于b的元素
print(set(c).difference(a))
print(set(b).difference(a))