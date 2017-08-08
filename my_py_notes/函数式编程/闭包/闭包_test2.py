# coding = utf-8

'''
@author = super_fazai
@File    : 闭包_test2.py
@Time    : 2017/8/4 11:28
@connect : superonesfazai@gmail.com
'''

def line_conf(a, b):
    def line(x):
        return a * x + b
    return line

line1 = line_conf(1, 1)
line2 = line_conf(4, 5)
print(line1(5))

'''
这个例⼦中, 函数line与变量a,b构成闭包
在创建闭包的时候， 我们通过line_conf的参数a,b
说明了这两个变量的取值, 这样, 我们就确定了函数的最终形式(y = x + 1和y = 4x + 5)。 我们只需要变换参数a,b， 就可以获得不同的
直线表达函数. 由此, 我们可以看到, 闭包也具有提⾼代码可复⽤性的作
⽤.
如果没有闭包, 我们需要每次创建直线函数的时候同时说明a,b,x
这样, 我们就需要更多的参数传递， 也减少了代码的可移植性
'''