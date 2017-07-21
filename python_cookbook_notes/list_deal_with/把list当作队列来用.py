#coding:utf-8

'''
队列作为特定的数据结构
最先进入的元素最先释放（先进先出）
不过，列表这样用效率不高
相对来说从列表末尾添加和弹出很快
在头部插入和弹出很慢(因为，为了一个元素，要移动整个列表中的所有元素)

要实现队列，使用 collections.deque
它为在首尾两端快速插入和删除而设计。
'''

from collections import deque

queue = deque(['a', 'b', 'c'])
queue.append('d')
queue.append('e')
print(queue)
print(queue.popleft())
print(queue.popleft())
print(queue)