#!/usr/bin/python3.5
# -*- coding:utf-8 -*-

#函数的参数
#Python的函数定义非常简单，但灵活度却非常大
#除了正常定义的必选参数外,还可以使用默认参数,可变参数,关键字参数和命名关键字参数
#使得函数定义出来的接口，不但能处理复杂的参数，还可以简化调用者的代码
#注意命名关键字参数是puthon3以上版本新出的，所以python2.7用不了

#位置参数
def power(x):
    return x * x

print (power(5))

def power(x, n):
        s = 1
        while n > 0:
            n = n - 1
            s = s * x
        return s

print (power(5, 2))
print (power(5, 3))

#默认参数
#默认参数可以简化函数的调用
#设置默认参数时要注意：
#一是必选参数在前，默认参数在后，否则Python的解释器会报错
#二是如何设置默认参数
#当函数有多个参数时，把变化大的参数放前面，变化小的参数放后面。变化小的参数就可以作为默认参数
#默认参数的最大的好处是能降低调用函数的难度
def enroll(name, gender):
    print ('name:', name, 'gender:', gender)
    return ('')

print (enroll('Sarah', 'F'))

def enroll(name, gender, age=6, city='Beijing'):
    print ('name:', name, 'gender:', gender, 'age:', age,  'city:', city)

print (enroll('Sarah', 'F'))
#只有与默认参数不符的学生才需要提供额外的信息
#有多个默认参数时，调用的时候，既可以按顺序提供默认参数
#也可以不按顺序提供部分默认参数。当不按顺序提供部分默认参数时，需要把参数名写上
print (enroll('Bob', 'M', 7))
print (enroll('Adam', 'M', city='Tianjin'))

#默认参数很有用，但使用不当，也会掉坑里。默认参数有个最大的坑

def add_end(L=[]):
    L.append('END')
    return L
#当你正常调用时，结果似乎不错
print (add_end([1, 2, 3]))
#当你使用默认参数调用时，一开始结果也是对的
#但是，再次调用add_end()时，结果就不对了
print (add_end(), ',',add_end(), ',',add_end())
#所以，定义默认参数要牢记一点：默认参数必须指向不变对象
#我们可以用None这个不变对象来实现
def add_end(L=None):
    if L is None:
        L = []
    L.append('END')
    return L
#现在，无论调用多少次，都不会有问题
print (add_end(), ',',add_end(), ',',add_end())

#可变参数
#可变参数就是传入的参数个数是可变的，可以是1个、2个到任意个，还可以是0个
#常规写法
def calc(numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
#调用的时候，需要先组装出一个list或tuple
print (calc([1, 2, 3]), ',', calc((1, 3, 5)))
#利用可变参数，调用函数的方式可以简化成这样
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum

print (calc(1, 2), ',', calc())
#如果已经有一个list或者tuple，要调用一个可变参数怎么办？可以这样做
nums = [1, 2, 3]
print (calc(nums[0], nums[1], nums[2]))
#这种写法当然是可行的，问题是太繁琐，所以Python允许你在list或tuple前面加一个*号，把list或tuple的元素变成可变参数传进去
nums = [1, 2, 3]
print (calc(*nums))

#关键字参数
#关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)

print (person('Michael', 30))
print (person('Bob', 35, city='Beijing'))
print (person('Adam', 45, gender='M', job='Engineer'))
#试想你正在做一个用户注册的功能，除了用户名和年龄是必填项外，其他都是可选项，利用关键字参数来定义这个函数就能满足注册的需求
extra = {'city': 'Beijing', 'job': 'Engineer'}
print (person('Jack', 24, city=extra['city'], job=extra['job']))
#也可以简化成下面
print (person('Jack', 24, **extra))


#命名关键字参数
#调用者仍可以传入不受限制的关键字参数
#如果要限制关键字参数的名字，就可以用命名关键字参数
#和关键字参数**kw不同，命名关键字参数需要一个特殊分隔符*，*后面的参数被视为命名关键字参数
def person(name, age, **kw):
    if 'city' in kw:
        # 有city参数
        pass
    if 'job' in kw:
        # 有job参数
        pass
    print('name:', name, 'age:', age, 'other:', kw)
#调用者仍可以传入不受限制的关键字参数
print (person('Jack', 24, city='Beijing', addr='Chaoyang', zipcode=123456))
#如果要限制关键字参数的名字，就可以用命名关键字参数，例如，只接收city和job作为关键字参数
def person(name, age, *, city, job):
    print(name, age, city, job)
print (person('Jack', 24, city='Beijing', job='Engineer'))
#如果函数定义中已经有了一个可变参数，后面跟着的命名关键字参数就不再需要一个特殊分隔符*了
def person(name, age, *args, city, job):
    print(name, age, args, city, job)
#命名关键字参数必须传入参数名，这和位置参数不同。如果没有传入参数名，调用将报错


#参数组合
#在Python中定义函数，可以用必选参数、默认参数、可变参数、关键字参数和命名关键字参数，这5种参数都可以组合使用。但是请注意，参数定义的顺序必须是：必选参数、默认参数、可变参数、命名关键字参数和关键字参数
def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)

def f2(a, b, c=0, *, d, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)

print (f1(1, 2))
print (f1(1, 2, c=3))
print (f1(1, 2, 3, 'a', 'b'))
print (f1(1, 2, 3, 'a', 'b', x=99))
print (f2(1, 2, d=99, ext=None))
