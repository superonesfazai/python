# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/11 14:24
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from fzutils.spider.fz_requests import MyRequests

# img_url 在e里
# var e = this.props.el;
# arguments里面

with open('../templates/kaola_spider_2_show.html', 'r') as f:
    text_1 = f.read()

print(text_1)

with open('../templates/yanxuan_spider_2_show.html', 'r') as f:
    text_2 = f.read()

# print(text_1)

text1 = text_1.splitlines()
text2 = text_2.splitlines()

# d = difflib.Differ()
# diff = d.compare(text1, text2)
# print('\n'.join(list(diff)))

# 替换成
import difflib
d = difflib.HtmlDiff()
d_html_code = d.make_file(text1, text2)

with open('diff_html.html', 'wb') as f:
    f.write(d_html_code.encode('utf-8'))