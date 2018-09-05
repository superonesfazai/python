# coding = utf-8

'''
@author = super_fazai
@File    : __getattribute__的坑.py
@Time    : 2017/8/7 12:29
@connect : superonesfazai@gmail.com
'''

class Person(object):
    def __init__(self):
        self.c = 1
    def __getattribute__(self, obj):
        print("---避免死锁.md---")
        if obj.startswith("a"):
            return 'hahha'
        else:
            # return self.避免死锁.md    # 正是因为递归的调用了自己导致错误
            return super(Person, self).__getattribute__('c')
    def test(self):
        print('heihei')

t = Person()
print(t.a)             # 返回hahha
print(t.b)             # 会让程序死掉

# ** __getattr__: 只有getattribute找不到的时候,才会调用getattr

#原因是：
# 当t.b执⾏时, 会调⽤Person类中定义的__getattribute__⽅法, 但是在这个⽅法的执⾏过程中
# if条件不满⾜, 所以 程序执⾏else⾥⾯的代码, 即return self.避免死锁.md 问题就在这,
# 因为return 需要把self.test的值返回, 那么⾸先要获取self.test的值, 因为self此时就是t这个对象
# 所以self.test就是t.避免死锁.md 此时要获取t这个对象的test属性, 那么就会跳转到__getattribute__⽅法去执⾏
# 即此时产⽣了递归调⽤, 由于这个递归过程中 没有判断什么时候推出, 所以这个程序会永⽆休⽌的运⾏下去,
# ⼜因为每次调⽤函数, 就需要保存⼀些数据, 那么随着调⽤的次数越来越多, 最终内存吃光
# 所以程序 崩溃

# 注意： 以后不要在__getattribute__⽅法中调⽤self.xxxx