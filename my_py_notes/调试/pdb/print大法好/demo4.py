# coding = utf-8

'''
@author = super_fazai
@File    : demo4.py
@Time    : 2017/8/7 18:38
@connect : superonesfazai@gmail.com
'''
'''
In [1]: def pdb_test(arg):
...: for i in range(arg):
...: print(i)
...: return arg
...:
In [2]: #在python交互模式中， 如果想要调试这个函数， 那么可以
In [3]: #采⽤， pdb.run的⽅式， 如下：
In [4]: import pdb
In [5]: pdb.run("pdb_test(10)")
> <string>(1)<module>()
(Pdb) s
--Call--
> <ipython-input-1-ef4d08b8cc81>(1)pdb_test()
-> def pdb_test(arg):
(Pdb) l
1 -> def pdb_test(arg):
2 for i in range(arg):
3 print(i)
4 return arg
[EOF]
(Pdb) n
> <ipython-input-1-ef4d08b8cc81>(2)pdb_test()
-> for i in range(arg):
(Pdb) l
1 def pdb_test(arg):
2 -> for i in range(arg):
3 print(i)
4 return arg
[EOF]
(Pdb) n
> <ipython-input-1-ef4d08b8cc81>(3)pdb_test()
-> print(i)
(Pdb)
0 >
<ipython-input-1-ef4d08b8cc81>(2)pdb_test()
-> for i in range(arg):
(Pdb)
> <ipython-input-1-ef4d08b8cc81>(3)pdb_test()
-> print(i)
(Pdb)
1 >
<ipython-input-1-ef4d08b8cc81>(2)pdb_test()
-> for i in range(arg):
(Pdb)
'''
