#coding:utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 上午11:03
# @File    : 动态生成和执行python代码_test.py

# 关键在于思想

dashes = '\n' + '-' * 50    # 分割线

exec_dict = {
'f': '''    # for_loop
for %s in %s:
    print(%s)
''',

's': '''    # while_loop
%s = 0
%s = %s
while %s < len(%s):
    print(%s[%s])
    %s = %s + 1
''',

'n': '''    # 点数_while_loop
%s = %d
while %s < %d:
    print(%s)
    %s = %s + %d
'''
}

def main():
    ltype = input('循环type?(for/while) ')
    dtype = input('data type?(number/seq) ')

    if dtype == 'n':
        start = int(input('starting value? '))
        stop = int(input('ending value (non-inclusive)? '))
        step = int(input('stepping value? '))
        seq = str(range(start, stop, step))

    else:
        seq = input('enter sequence: ')
        var = input('Iterative variable name? ')
        if ltype == 'f':
            exec_str = exec_dict['f'] % (var, seq, var)
        elif ltype == 'w':
            if dtype == 's':
                svar = input('enter sequence name? ')
                exec_str = exec_dict['s'] % \
                       (var, svar, seq, var, svar, var,var,var)
            elif dtype == 'n':
                exec_str = exec_dict['n'] % \
                       (var, start, var, stop, var, var, var, step)
        print(dashes)
        print('your custom-generated code:' + dashes)
        print(exec_str + dashes)
        print('避免死锁 execution of the code:' + dashes)
        exec(exec_str)
        print(dashes)

if __name__ == '__main__':
    main()