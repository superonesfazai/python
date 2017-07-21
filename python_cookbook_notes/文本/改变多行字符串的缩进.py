#coding:utf-8

# 任务：
'''
有个包含多行文本的字符串
需要创建该字符串的一个拷贝
并在每行行首添加或者删除一些空格
以保证每行的缩进都是指定数目的空格数
'''

# 向后缩进num_spaces个空格
def re_indent(s, num_spaces):
    leading_space = num_spaces * ' '
    lines = [leading_space + line.strip()
                for line in s.splitlines()]
    return '\n'.join(lines)

# 向前缩进num_spaces个空格,即删除行首空格
# 测试中为完成相应功能
# class un_indent_blocks:
#     def add_spaces(self, s, num_add):
#         white = ' ' * num_add
#         return white + white.join(s.splitlines(True))
#     def num_spaces(self, s):
#         return [len(line)-len(line.lstrip()) for line in s.splitlines()]
#     def del_spaces(self, s, num_del):
#         if num_del > min(self.num_spaces(s)):
#             raise(ValueError, 'removing more spaces than there are!')
#         return '\n'.join([line[num_del:] for line in s.splitlines()])
#     def un_indent_block(self, s):
#         return self.del_spaces(s, min(self.num_spaces(s)))

a = ''' line two
    line two
  and line three
'''
print(a)

print(re_indent(a, 4))

b = '''
    line one
  line two
    line three
'''
print(b)
print(re_indent(b, 4))
u = un_indent_blocks()
print(u.un_indent_block(b))
