# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/9/29 13:12
@connect : superonesfazai@gmail.com
'''

import re
from pprint import pprint

tmp_url = 'https://weibo.com/p/1005051767797335/info?mod=pedit_more'
tmp_url2 = 'https://weibo.com/5690339577/about'

is_had = re.compile(r'.*?(about)').findall(tmp_url2)

if is_had:
    print(tmp_url2)

a = ['a', 'b']
print(', '.join(a))

print('-' * 100)

tmp_info_list = ['<span class="pt_detail">-H-D-Z-</span>', '<span class="pt_detail">上海 黄浦区</span>', '<span class="pt_detail">女</span>', '<span class="pt_detail">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<a href="https://weibo.com/kamekazuhdz?from=inf&amp;wvr=5&amp;loc=infdomain">https://weibo.com/kamekazuhdz</a>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</span>', '<span class="pt_detail">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t2010-11-22\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</span>', '<span class="pt_detail">kamekazuhdz@foxmail.com</span>', '<span class="pt_detail">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<a target="_blank" node-type="tag" href="http://s.weibo.com/user/&amp;tag=%E5%A8%B1%E4%B9%90" class="W_btn_b W_btn_tag">\n\t\t\t\t\t\t\t\t<span class="W_arrow_bor W_arrow_bor_l"><i class="S_line3"></i><em class="S_bg2_br"></em>\n\t\t\t\t\t\t\t\t</span>\n\t\t\t\t\t\t\t\t娱乐\t\t\t\t\t\t\t\t</a>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<a target="_blank" node-type="tag" href="http://s.weibo.com/user/&amp;tag=%E9%BE%9F%E6%A2%A8%E5%92%8C%E4%B9%9F" class="W_btn_b W_btn_tag">\n\t\t\t\t\t\t\t\t<span class="W_arrow_bor W_arrow_bor_l"><i class="S_line3"></i><em class="S_bg2_br"></em>\n\t\t\t\t\t\t\t\t</span>\n\t\t\t\t\t\t\t\t龟梨和也\t\t\t\t\t\t\t\t</a>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</span>']

info_list = []
for item in tmp_info_list:
    item = item.replace(' ', '|')       # 先把空格替换成'|', 然后待替换完，再替换回去
    item = re.compile('\s+').sub('', item)
    item = item.replace('|', ' ')
    # print(item)
    item = re.compile(r'<span class="pt_detail">(.*?)</span>').findall(item)[0]

    is_a_label = re.compile('<a .*?>.*?</a>').findall(item)
    if is_a_label:
        item = re.compile(r'<a href=.*?>(.*?)</a>').findall(item)[0]
    info_list.append(item)
    # print(item)

print(info_list)

a = ['', 'a', '', 'b']
print(','.join(a))