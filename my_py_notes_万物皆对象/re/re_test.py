#coding:utf-8
__author__ = 'super_fazai'

import re

line = 'booooobbbaaby123d'
line1 = 'boobby123'
line2 = '18782902222'

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
