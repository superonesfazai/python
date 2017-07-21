#coding: utf-8

'''
列表方法使得列表可以很方便的做为一个堆栈来使用
堆栈作为特定的数据结构
最先进入的元素最后一个被释放（后进先出）
用 append() 方法可以把一个元素添加到堆栈顶
用不指定索引的 pop() 方法可以把一个元素从堆栈顶释放出来
'''

stack = [3, 4, 5]
stack.append(6)
stack.append(7)
print(stack)
print(stack.pop())
print(stack)
print(stack.pop())
print(stack.pop())
print(stack)