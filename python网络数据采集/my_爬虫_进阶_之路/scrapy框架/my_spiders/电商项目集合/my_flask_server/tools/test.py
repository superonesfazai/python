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

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from pprint import pprint
import re
from fzutils.time_utils import fz_set_timeout

sql_str = '''
select id, head_img_url 
from dbo.sina_weibo
where sina_type != 'bilibili'
'''

_ = SqlServerMyPageInfoSaveItemPipeline()
result = _._select_table(sql_str=sql_str, params=None)
# pprint(result)

def update_img_50_2_180_url():
    @fz_set_timeout(6)
    def oo(img_url, id):
        _._update_table(sql_str=update_sql_str, params=(img_url, id))

    s = []
    for item in result:
        id = item[0]
        img_50_url = item[1]

        img_180_url = re.compile('\.50/').sub('.180/', img_50_url)
        s.append((id, img_180_url))

    update_sql_str = '''
    update dbo.sina_weibo set head_img_url=%s
    where id=%s
    '''
    for i in s:
        try:
            oo(i[1], i[0])
        except Exception as e:
            print(e)
            continue
        print('转换id:{0}成功! img_180_url:{1}'.format(i[0], i[1]))

    return True

update_img_50_2_180_url()