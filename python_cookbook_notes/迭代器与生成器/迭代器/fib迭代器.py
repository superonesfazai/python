# coding = utf-8

'''
@author = super_fazai
@File    : fib迭代器.py
@Time    : 2017/8/4 09:02
@connect : superonesfazai@gmail.com
'''

class FibIterator(object):
    """(Fibonacci)斐波那契数列迭代器"""
    def __init__(self, n):
        self.n = n          #  指明生成数列的前n个数
        self.current = 0    # current⽤来保存当前⽣成到数列中的第⼏个数了
        self.num1 = 0       # num1⽤来保存前前⼀个数， 初始值为数列中的第⼀个数0
        self.num2 = 1       # num2⽤来保存前⼀个数， 初始值为数列中的第⼆个数1

    def __next__(self):     # 即num1, num2两个一起往后移
        '''被next()函数调⽤来获取下⼀个数'''
        if self.current < self.n:
            num = self.num1
            # 计算下一次迭代要返回的数据
            self.num1, self.num2 = self.num2, self.num1+self.num2
            self.current += 1
            return num
        else:
            raise StopIteration

    def __iter__(self):
        '''迭代器的__iter__返回⾃身即可'''
        return self

if __name__ == '__main__':
    fib = FibIterator(20)
    for num in fib:
        print(num, end=' ')

    print('')
    # 除了for循环能接收可迭代对象, list, tuple等也能接收
    li = list(FibIterator(20))
    print(li)
    tp = tuple(FibIterator(20))
    print(tp)