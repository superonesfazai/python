# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@Time    : 2017/7/30 17:29
@connect : superonesfazai@gmail.com
'''

from prettytable import PrettyTable
import prettytable as pt

## 按行添加数据
tb = PrettyTable()
tb.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
tb.add_row(["Adelaide",1295, 1158259, 600.5])
tb.add_row(["Brisbane",5905, 1857594, 1146.4])
tb.add_row(["Darwin", 112, 120900, 1714.7])
tb.add_row(["Hobart", 1357, 205556,619.5])

## 按列添加数据
tb.add_column('index',[1,2,3,4])
print(tb)

'''使用不同的输出风格'''
# tb.set_style(pt.MSWORD_FRIENDLY)
# print('--- style：MSWORD_FRIENDLY -----')
# print(tb)

# tb.set_style(pt.PLAIN_COLUMNS)
# print('--- style：PLAIN_COLUMNS -----')
# print(tb)

# 随机风格，每次不同
# tb.set_style(pt.RANDOM)
# print('--- style：MSWORD_FRIENDLY -----')
# print(tb)

# tb.set_style(pt.DEFAULT)
# print('--- style：DEFAULT -----')
# print(tb)

'''自定义表格输出样式'''
### 设定左对齐
tb.align = 'l'
### 设定数字输出格式
tb.float_format = "2.2"
### 设定边框连接符为'*"
tb.junction_char = "*"
### 设定排序方式
tb.sortby = "City name"
### 设定左侧不填充空白字符
tb.left_padding_width = 0
print(tb)

# 不显示边框
# tb.border = 0

## 修改边框分隔符
# tb.set_style(pt.DEFAULT)
# tb.horizontal_char = '+'
# print(tb)

'''prettytable也支持输出HTML代码'''
# s = tb.get_html_string()
# print(s)