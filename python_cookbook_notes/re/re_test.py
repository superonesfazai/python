#coding:utf-8
__author__ = 'super_fazai'

import re

line = 'booooobbbaaby123d'
line1 = 'boobby123'
line2 = '18782902222'

#'.' 表示任何字符除了'\n'
#'*' 表示前面的字符可以重复任意次数,也可以表示字符出现0次,即大于等于0次
#'^' 表示以什么字符开头,eg:'^b' 以b开头
#'$' 表示以什么字符结尾,eg:'b$' 以b结尾
#'.*' 配合使用表示匹配任意字符
#'?' 是一种非贪婪匹配的模式(即从左边的字符串开始匹配的第一个)
#'.*?' 配合用于非贪婪匹配模式
#'()' 表示提取字符串的子串
#'+' 表示+前面的字符至少出现一次,即大于等于一次
#'{}' 表示限定前面那个字符出现的次数,eg:'a{2}' 表示限定a出现两次,也可以写成'a{2,}'
#'{2,5}' 表示出现最少两次最多5次
#'|' 表示或的意思,eg:'ab|abc' 表示匹配ab或者abc即可,优先匹配前面的那段字符
#'[]' 表示中括号里面的字符只要满足任意一个就行,eg:'[0-9]','[^1]'
#'\s' 表示空格 '\S'表示非空格
#'\w' 等同于'[A-Za-z0-9_]' 同样'\W'表示不为小写w中的字符就匹配
#'[\u4E00-\u9FA5]' 表示提取一个汉字
#'\d' 表示匹配连续的数字
#正则表达式默认是贪婪匹配的(反向匹配,即从右边的字符串开始匹配的第一个)
regex_str1 = '^b.*d$'
regex_str2 = '.*?(b.*?b).*'
regex_str3 = '.*(b.+b).*'
regex_str4 = '.*(b.{2,5}b).*'
regex_str5 = '((bobby|boobby)123)'  #先匹配小括号里的再匹配大括号里l 的
regex_str6 = '([abcd]oobby123)'
regex_str7 = '(1[34578][0-9]{9})'
match_obj1 = re.match(regex_str1, line)
match_obj2 = re.match(regex_str2, line)
match_obj3 = re.match(regex_str3, line)
match_obj4 = re.match(regex_str4, line)
match_obj5 = re.match(regex_str5, line1)
match_obj6 = re.match(regex_str6, line1)
match_obj7 = re.match(regex_str7, line2)
if match_obj1:
    print('yes')

if match_obj2:
    print(match_obj2.group(1))  #group(1)表示只提取第一个括号里面的东西

if match_obj3:
    print(match_obj3.group(1))

if match_obj4:
    print(match_obj4.group(1))

if match_obj5:
    print(match_obj5.group(1))

if match_obj6:
    print(match_obj6.group(1))

if match_obj6:
    print(match_obj7.group(1))
