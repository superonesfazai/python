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

print('-' * 100)

info_list = []
tmp_2 = ['<span class="pt_detail">一_起去冰岛吧</span>', '<span class="pt_detail">内蒙古 包头</span>', '<span class="pt_detail">男</span>', '<span class="pt_detail">1995年12月11日</span>', '<span class="pt_detail">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t2014-09-09\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</span>', '<span class="pt_detail">1521715360@qq.com</span>', '<span class="pt_detail">1521715360</span>', '<span class="pt_detail">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<a href="http://s.weibo.com/user/&amp;school=%E5%86%85%E8%92%99%E5%8F%A4%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6&amp;from=inf&amp;wvr=5&amp;loc=infedu">内蒙古科技大学</a> (2014年)\t\t\t\t\t\t\t\t\t<br>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</span>']
for item in tmp_2:
    item = item.replace(' ', '|')
    item = re.compile('\s+').sub('', item)
    item = item.replace('|', ' ')
    item = re.compile(r'<span class="pt_detail">(.*?)</span>').findall(item)[0]
    # print(item)

    is_a_label = re.compile('<a .*?>.*?</a>').findall(item)
    if is_a_label:
        item1 = re.compile(r'<a href=.*?>(.*?)</a>').findall(item)[0]
        # 筛选读书年份
        # 提取第一个br标签内容
        is_br_label = re.compile(r'<a href="http://s.weibo.com/.*?>.*?</a>(.*?)<br>').findall(item)
        if is_br_label != []:
            item2 = re.compile(r'<a .*?>.*?</a>(.*?)<br>').findall(item)[0]
            # 提取第二个br标签内容
            is_br_label2 = re.compile(r'<a href="http://s.weibo.com/.*?>.*?</a>.*?<br>(.*?)<br>').findall(item)
            if is_br_label2 != []:
                item3 = re.compile(r'<a .*?>.*?</a>.*?<br>(.*?)<br>').findall(item)[0]
            else:
                item3 = ''
        else:
            item2 = ''
        item = item1 + item2 + item3
    info_list.append(item)
    print(item)

print(info_list)
print('-' * 100)
a = ['', 'a', '', 'b']
print(','.join(a))

print('-' * 100)

tmp_info_list = ['<span class="pt_detail">010-67078755</span>', '<span class="pt_detail">webmaster@gmw.cn</span>', '<span class="pt_detail"><a href="//www.gmw.cn" title="光明网" alt="光明网" target="_blank">光明网</a> </span>']

tmp_friend_url = {}
name_list = {}
info_list = []
friend_url = ''
for item in tmp_info_list:
    item = re.compile('<span class="pt_detail">(.*?)</span>').findall(item)[0]
    # 判断是否有a标签
    is_a_label = re.compile('<a href=.*?>(.*?)</a>').findall(item)
    if is_a_label:      # 处理a标签
        tmp_name_list = re.compile('<a href=.*?>(.*?)</a>').findall(item)
        url_info_list = re.compile(r'<a href="(.*?)".*?>.*?</a>').findall(item)

        # 构造友情链接
        for index in range(0, len(tmp_name_list)):
            tmp_friend_url[tmp_name_list[index]] = 'http:' + url_info_list[index]
        print(tmp_friend_url)

        for key in tmp_friend_url:
            print(key, tmp_friend_url[key])
            tmp_str = key + ': ' + tmp_friend_url[key] + ', '
            friend_url += tmp_str
        item = friend_url

    info_list.append(item)
# print(tmp_info_list)
print(info_list)

print('-' * 100)

tmp = {}

# for index in range(0, len(b)):
#     if a[index] == 3:
#         tmp[a[index]] = 'c'
#         index2 = index
#         for index3 in range(index2+1, len(a)):
#             print(index3, b[index3])
#             tmp[a[index3+1]] = b[index]
#         pass
#     else:
#         print(index, b[index])
#         tmp[a[index]] = b[index]
# print(tmp)
all_right_info = {}
title_list = [1, 2, 3, 4, 5]
info_list = ['a', 'b', 'd', 'e']

had_blog = False
tmp_list = []
for index in range(0, len(title_list)):
    if title_list[index] == 3:
        had_blog = True
        for index2 in range(0, index):
            tmp_list.append(title_list[index2])
        for index3 in range(index+1, len(title_list)):
            tmp_list.append(title_list[index3])
# print(tmp_list)

for index in range(0, len(tmp_list)):
    all_right_info[tmp_list[index]] = info_list[index]

all_right_info[3] = 'c'
print(all_right_info)

print('=' * 100)

a = '大学: 中国政法大学 (1998年)   法学院<a href="http://s.weibo.com/user/&amp;school=%E4%B8%AD%E5%9B%BD%E6%94%BF%E6%B3%95%E5%A4%A7%E5%AD%A6&amp;from=inf&amp;wvr=5&amp;loc=infedu">中国政法大学</a> , '

item2 = re.compile(r'<a .*?>.*?</a>').sub('', a)
print(item2)

print('过滤四个字节以上的表情字符'.center(100, '-'))

def filter_emoji_str(content):
    '''
    过滤四个字节以上的表情字符
    :param content:
    :return:
    '''
    try:
        # python UCS-4 build的处理方式
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        # python UCS-2 build的处理方式
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

    resovle_value = highpoints.sub(u'??', content)

    return resovle_value

a = '你好aaaa7878$🌶'
resovle_str = filter_emoji_str(a)
print(resovle_str)
