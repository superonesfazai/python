#!/usr/bin/python3.5
# -*- coding:utf-8 -*-

#递归函数
def fact(n):
    if n==1:
        return 1
    return n * fact(n - 1)

print (fact(1), ',',fact(5), ',', fact(100))

#使用递归函数需要注意防止栈溢出。在计算机中，函数调用是通过栈（stack）这种数据结构实现的，每当进入一个函数调用，栈就会加一层栈帧，每当函数返回，栈就会减一层栈帧。由于栈的大小不是无限的，所以，递归调用的次数过多，会导致栈溢出
#print (fact(1000))
#解决递归调用栈溢出的方法是通过尾递归优化
#尾递归是指，在函数返回的时候，调用自身本身，并且，return语句不能包含表达式。这样，编译器或者解释器就可以把尾递归做优化，使递归本身无论调用多少次，都只占用一个栈帧，不会出现栈溢出的情况。
def fact(n):
    return fact_iter(n, 1)

def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)

print (fact_iter(5, 1))

#使用递归函数的优点是逻辑简单清晰，缺点是过深的调用会导致栈溢出
#针对尾递归优化的语言可以通过尾递归防止栈溢出
#Python标准的解释器没有针对尾递归做优化，任何递归函数都存在栈溢出的问题






