# coding = utf-8

'''
@author = super_fazai
@File    : demo5运⾏过程中使⽤pdb修改变量的值.py
@Time    : 2017/8/7 18:42
@connect : superonesfazai@gmail.com
'''

'''
In [7]: pdb.run("pdb_test(1)")
> <string>(1)<module>()
(Pdb) s
--Call--
> <ipython-input-1-ef4d08b8cc81>(1)pdb_test()
-> def pdb_test(arg):
(Pdb) a
arg = 1
(Pdb) l
1 -> def pdb_test(arg):
2 for i in range(arg):
3 print(i)
4 return arg
[EOF]
(Pdb) !arg = 100 #!!!这⾥是修改变量的⽅法
(Pdb) n
> <ipython-input-1-ef4d08b8cc81>(2)pdb_test()
-> for i in range(arg):
(Pdb) l
1 def pdb_test(arg):
2 -> for i in range(arg):
3 print(i)
4 return arg
[EOF]
(Pdb) p arg
100
(Pdb)
'''