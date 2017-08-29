# coding = utf-8

'''
@author = super_fazai
@File    : re_match_test.py
@Time    : 2017/8/29 09:37
@connect : superonesfazai@gmail.com
'''

import re

"""
match(string[, pos[, endpos]])
"""
pattern = re.compile(r'\d+')
m = pattern.match('one12twothree34four', 3, 10)

print(m)
print(m.group(0))
print(m.start(0))
print(m.end(0))
print(m.span(0))

'''
在上面，当匹配成功时返回一个 Match 对象，其中：
    group([group1, …]) 方法用于获得一个或多个分组匹配的字符串，当要获得整个匹配的子串时，可直接使用 group() 或 group(0)；
    
    start([group]) 方法用于获取分组匹配的子串在整个字符串中的起始位置（子串第一个字符的索引），参数默认值为 0；
    
    end([group]) 方法用于获取分组匹配的子串在整个字符串中的结束位置（子串最后一个字符的索引+1），参数默认值为 0；
    span([group]) 方法返回 (start(group), end(group))。
'''