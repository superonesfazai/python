# coding = utf-8

'''
@author = super_fazai
@File    : fib_迭代器.py
@Time    : 2017/8/24 09:47
@connect : superonesfazai@gmail.com
'''

class FibDie(object):
    def __init__(self, n):
        self.n = n
        self.index = 0
        self.num1 = 0
        self.num2 = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < self.n:
            num = self.num1
            self.num1, self.num2 = self.num2, self.num1 + self.num2
            self.index += 1
            return num
        else:
            raise StopIteration

if __name__ == '__main__':
    f = FibDie(20)
    total = 0
    print('斐波那契数列前20项为:', list(f))
    tmp_f = list(f)
    for i in tmp_f:
        total += i

    print('斐波那契数列前20项的和为:', total)

'''
测试结果:
斐波那契数列前20项为: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181]
斐波那契数列前20项的和为: 10945
'''