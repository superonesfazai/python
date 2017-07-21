#!/usr/bin/python3.5
# -*- coding:utf-8 -*-

#dict
#key-value存储方式
#dict是用空间来换取时间的一种方法
#作为key的对象就不能变
#字符串、整数等都是不可变的，因此，可以放心地作为key。
#而list是可变的，就不能作为key
#dict 的 key 是大小写敏感的
d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
print(d)
print(d['Michael'])

d['Adam'] = 67
print(d['Adam'])

#一个key只能对应一个value，所以，多次对一个key放入value，后面的值会把前面的值冲掉
d['Jack'] = 90
print(d['Jack'])
d['Jack'] = 88
print(d['Jack'])

#要避免key不存在的错误，有两种办法
#一是通过in判断key是否存在
print ('Thomas' in d)

#二是通过dict提供的get方法，如果key不存在，可以返回None，或者自己指定的value
print(d.get('Thomas'))
print(d.get('Thomas', -1))

#要删除一个key，用pop(key)方法，对应的value也会从dict中删除
print(d)
d.pop('Bob')
print(d)

#Note: Dictionary 是无序的
d = {'server': 'mpilgrim', 'database': 'master'}
print(d)
#增加key-value
d['uid'] = 'sa'
print(d)
d.clear()   #清空所有
print(d)

#在 dictionary中混用数据类型
'''
(1) Dictionary 不只是用于存储字符串。Dictionary 的值可以是任意数据类型,
包括字符串、整数、对象,甚至其它的 dictionary。在单个 dictionary 里,
dictionary 的值并不需要全都是同一数据类型,可以根据需要混用和匹配。
(2) Dictionary 的 key 要严格多了,但是它们可以是字符串、整数或几种其它
的类型 (后面还会谈到这一点)。也可以在一个 dictionary 中混用和匹配 key
的数据类型。
'''

#set
#set和dict类似，也是一组key的集合，但不存储value。
#由于key不能重复，所以，在set中，没有重复的key
s = set([1, 2, 3])
print(s)
s = set([1, 1, 2, 2, 3, 3])
print(s)

#通过add(key)方法可以添加元素到set中，可以重复添加，但不会有效果
s.add(4)
print(s)
s.add(4)
print(s)

#通过remove(key)方法可以删除元素
s.remove(4)
print(s)

#set可以看成数学意义上的无序和无重复元素的集合
#因此，两个set可以做数学意义上的交集、并集等操作
s1 = set([1, 2, 3])
s2 = set([2, 3, 4])
print(s1 & s2)
print(s1 | s2)