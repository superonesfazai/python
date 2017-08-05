# coding = utf-8

'''
@author = super_fazai
@File    : 类装饰器_demo.py
@Time    : 2017/8/5 22:58
@connect : superonesfazai@gmail.com
'''

'''
在python中一般callable对象都是函数
但也有例外。
只要某个对象重写了__call__()方法
那么这个对象就是callable的
'''

class Test():
    def __call__(self, *args, **kwargs):
        print('call me!')

t = Test()
t()     # call me

class Test1(object):
    def __index__(self, func):
        print('---初始化---')
        print('func name is %s' % func.__name__)
        self.__func = func

    def __call__(self, *args, **kwargs):
        print('---装饰器中的功能---')
        self.__func()

@Test1
def test():
    print("---test---")

test()
# showpy()    # 如果把这句话注释, 重新运行程序, 依然会看到"---初始化---"

# 说明：
# 1. 当用Test1来装作装饰器对test函数进行装饰的时候, 首先会创建一个Test1实例
#       并且会把test这个函数名当作参数传到__init__方法中
#       即在__init__方法中的func变量指向了test函数体
# 2. test函数相当于指向了用Test1创建出来的实例对象
# 3. 当在使用test()进行调用时, 就相当于让这个对象(), 因此会调用这个对象的__call__方法
# 4. 为了能够在__call__方法中调用原来test指向的函数体, 所以在__init__方法中就需要一个实例属性来保存这个函数体的引用
# 5. 所以才有了self.__func = func这句代码, 从而在调用__call__方法中能够调用到test之前的函数体