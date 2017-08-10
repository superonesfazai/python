# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 上午10:28
# @File    : compile_exec_eval_test.py

# compile通常用法是动态生成字符串形式的python代码
# 然后让exec()和eval()来执行这些对象或者对它们求值

# 可求值表达式
eval_code = compile('100+200', '', 'eval')
print(eval(eval_code))

# 单一可执行语句
single_code = compile('print("------")', '', 'single')
print(single_code)
exec(single_code)

# 可执行语句组
exec_code = compile('''
req = int(input('count how many nubers?'))
for each_num in range(req):
    print(each_num)
''', '', 'exec')
exec(exec_code)

print(eval(exec_code))