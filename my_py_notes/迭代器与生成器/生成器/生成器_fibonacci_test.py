# coding = utf-8

'''
@author = super_fazai
@File    : 生成器_fibonacci_test.py
@Time    : 2017/8/4 09:53
@connect : superonesfazai@gmail.com
'''
'''
关于yield关键字的理解：
    1. 遇到yield关键字后, 代码的执行会被暂停, 但会执行当行yield语句
    2. 可以把yield关键字理解为return, 可以返回值
    3. 再次运行就跳过yield并执行下面的语句
'''
# 使用了yield关键字的函数不再是函数, 而是生成器(即使用了yield的函数就是生成器)
'''
yield关键字有两点作⽤：
    保存当前运⾏状态(断点), 然后暂停执⾏, 即将⽣成器(函数)挂起
    将yield关键字后⾯表达式的值作为返回值返回, 此时可以理解为起到了return的作⽤
    
可以使⽤next()函数让⽣成器从断点处继续执⾏, 即唤醒⽣成器(函数)
Python3中的⽣成器可以使⽤return返回最终运⾏的返回值, ⽽Python2
中的⽣成器不允许使⽤return返回⼀个返回值(即可以使⽤return从⽣成
器中退出, 但return后不能有任何表达式） 
'''
def fibonacci_gen(n):
    '''生成器'''
    num1, num2 = 0, 1
    counter = 0

    while counter < n:
        yield num1      # 返回需要记录的值
        num1, num2 = num2, num1 + num2
        counter += 1

    return 'done'       # 在一个生成器中, 如果没有return, 则默认执行到函数完毕时返回StopIteration;
                        # 如果遇到return, 则直接抛出StopIteration终止迭代

fib = fibonacci_gen(20)
while True:
    try:
        print(fib.__next__())
    except StopIteration as e:
        print('生成器返回的值:%s' % e.args[0])
        break