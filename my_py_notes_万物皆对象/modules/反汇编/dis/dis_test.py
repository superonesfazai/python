# coding = utf-8

'''
@author = super_fazai
@File    : dis_test.py
@Time    : 2017/8/8 20:35
@connect : superonesfazai@gmail.com
'''
'''
以前一直觉得Python不会对源码进行任何优化，不过看了字节码后，我改变了这个看法。

>>> def a():
...  return 1 + 1
...
>>> def b():
...  pass
...  return 1 + 1
...
>>> dis.dis(a)
  2           0 LOAD_CONST               2 (2)
              3 RETURN_VALUE
>>> dis.dis(b)
  3           0 LOAD_CONST               2 (2)
              3 RETURN_VALUE

例如上面这段代码，Python没有老老实实地在运行期去计算1 + 1，而是在编译期就返回常量2了。
此外，a和b的字节码居然是一样的，也就是说pass这条语句直接被删除了。

不过Python的编译器也仅能对常量做一些适当的优化，其他变量（包括True）就无能为力了：
>>> def c():
...  if True:
...   return 1 + 1
...
>>> dis.dis(c)
  2           0 LOAD_GLOBAL              0 (True)
              3 JUMP_IF_FALSE            8 (to 14)
              6 POP_TOP

  3           7 LOAD_CONST               2 (2)
             10 RETURN_VALUE
             11 JUMP_FORWARD             1 (to 15)
        >>   14 POP_TOP
        >>   15 LOAD_CONST               0 (None)
             18 RETURN_VALUE
>>> def d():
...  if 1 == 1:
...   return 1 + 1
...
>>> dis.dis(d)
  2           0 LOAD_CONST               1 (1)
              3 LOAD_CONST               1 (1)
              6 COMPARE_OP               2 (==)
              9 JUMP_IF_FALSE            8 (to 20)
             12 POP_TOP

  3          13 LOAD_CONST               2 (2)
             16 RETURN_VALUE
             17 JUMP_FORWARD             1 (to 21)
        >>   20 POP_TOP
        >>   21 LOAD_CONST               0 (None)
             24 RETURN_VALUE
>>> def e():
...  if 1:
...   return 1 + 1
...
>>> dis.dis(e)
  3           0 LOAD_CONST               2 (2)
              3 RETURN_VALUE
可以看到，只有“if 1”这个条件判断是直接被优化掉了，其他的“if True”和“if 1 == 1”都只能在运行期判断。同理可得，“while 1”肯定比“while True”快。

除了函数，dis()还能查看整个Python文件的编译结果，不过还需要compile()的辅助：
import dis

s = open('ooxx.py').read()
co = compile(s, 'ooxx.py', 'exec')
print dis.dis(co)

之前我还提到过，使用Python内置的运算符，一般会比调用函数快，其实看看字节码就明白了。
例如这个程序：
from operator(运算符) import pow

a = 123
a ** 456
pow(a, 456)
对应的字节码：
  1           0 LOAD_CONST               0 (-1)
              3 LOAD_CONST               1 (('pow',))
              6 IMPORT_NAME              0 (operator(运算符))
              9 IMPORT_FROM              1 (pow)
             12 STORE_NAME               1 (pow)
             15 POP_TOP

  3          16 LOAD_CONST               2 (123)
             19 STORE_NAME               2 (a)

  4          22 LOAD_NAME                2 (a)
             25 LOAD_CONST               3 (456)
             28 BINARY_POWER
             29 POP_TOP

  5          30 LOAD_NAME                1 (pow)
             33 LOAD_NAME                2 (a)
             36 LOAD_CONST               3 (456)
             39 CALL_FUNCTION            2
             42 POP_TOP
             43 LOAD_CONST               4 (None)
             46 RETURN_VALUE
None
可以看到，**操作符只需要载入2个参数，然后执行BINARY_POWER即可；pow函数则需要载入函数名和2个参数，然后CALL_FUNCTION。
很明显，Python的字节码对应的肯定是C代码，那么BINARY_POWER的性能肯定不会比pow的实现慢。而与此同时，后者还多LOAD_NAME了一次，这个操作实际上是在PyDictObject对象里查找，需要1或多次函数调用，性能肯定不如前者。
'''
