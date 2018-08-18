# coding:utf-8

'''
@author = super_fazai
@File    : multiplex_code.py
@Time    : 2017/8/18 18:07
@connect : superonesfazai@gmail.com
'''

"""
复用code
"""

from fzutils.spider.fz_requests import MyRequests
from fzutils.internet_utils import get_random_pc_ua

from scrapy.selector import Selector
import re

def _z8_get_parent_dir(goods_id):
    '''
    折800获取parent_dir (常规, 拼团, 秒杀都可用)
    :param goods_id:
    :return: '' | 'xxx/xxx'
    '''
    headers = {
        'authority': 'shop.zhe800.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': get_random_pc_ua(),
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'referer': 'https://brand.zhe800.com/yl?brandid=353130&page_stats_w=ju_tag/taofushi/1*1&ju_flag=1&pos_type=jutag&pos_value=taofushi&x=1&y=1&n=1&listversion=&sourcetype=brand&brand_id=353130',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        # 'cookie': 'has_webp=1; __utmz=148564220.1533879745.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); utm_csr=direct; session_id=1833465439.1533879745; utm_ccn=notset_c0; utm_cmd=; utm_ctr=; utm_cct=; utm_etr=tao.home; firstTime=2018-08-11; qd_user=32364805.1533966002852; f_jk=9269921533966002852qyOwt6Jn; f_jk_t=1533966002857; f_jk_e_t=1536558002; f_jk_r=https://www.zhe800.com/ju_tag/taofushi; user_type=0; downloadGuide_config=%257B%25220direct%2522%253A%257B%2522open%2522%253A1%257D%257D; user_role=1; student=0; gr_user_id=cb0301be-4ee0-4f86-80c5-7d880106ed87; user_id=; utm_csr_first=direct; ac_token=15345580381942356; frequency=1%2C0%2C0%2C0%2C1%2C0%2C0%2C1%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0; lastTime=2018-08-18; cart_mark=1%7C0%7C0%7Cnil%7C0; __utma=148564220.1330126799.1533879745.1533965999.1534583229.3; __utmc=148564220; __utmt=1; screenversion=2; ju_rv=BD001_BAYES_RCMD; unix_time=1534583232; ju_version=3; gr_session_id_655df36e87c2496389d319bd67d56fec=c953414c-5377-42f3-b449-99ed57b65b31; gr_session_id_655df36e87c2496389d319bd67d56fec_c953414c-5377-42f3-b449-99ed57b65b31=true; jk=9451481534583233650qyOwt6Jn; __utmb=148564220.5.10.1534583229; new_old_user=1; city_id=330000; source=; platform=; version=; channelId=; deviceId=; userId=; cType=; cId=; dealId=; visit=7; wris_session_id=424077871.1534583351',
    }

    params = (
        ('jump_source', '1'),
        ('qd_key', 'qyOwt6Jn'),
    )

    url = 'https://shop.zhe800.com/products/{0}'.format(goods_id)
    # response = requests.get(, headers=headers, params=params)
    # print(response.text)
    body = MyRequests.get_url_body(url=url, headers=headers, params=None, high_conceal=True)
    # print(body)

    parent_dir = []
    try:
        aside = Selector(text=body).css('aside.pos.area').extract_first()
        # print(aside)
        assert aside is not None, '获取到的aside为None!获取parent_dir失败!'
        _1 = Selector(text=aside).css('em::text').extract_first()
        # print(_1)
        parent_dir.append(_1)
        _2 = re.compile('</i>(.*?)<i>').findall(aside)[1].replace(' ', '')
        # print(_2)
    except Exception as e:
        print('获取parent_dir时遇到错误(默认为""):', e)
        return ''

    parent_dir.append(_2)
    # 父级路径
    parent_dir = '/'.join(parent_dir)
    # print(parent_dir)

    return parent_dir
