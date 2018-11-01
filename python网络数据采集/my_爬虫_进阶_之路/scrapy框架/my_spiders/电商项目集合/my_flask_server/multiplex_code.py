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

from settings import IP_POOL_TYPE

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline, SqlPools

from scrapy.selector import Selector
import re
from time import time
from asyncio import wait
from fzutils.spider.fz_requests import MyRequests
from fzutils.internet_utils import get_random_pc_ua
from fzutils.common_utils import _print
from fzutils.time_utils import get_shanghai_time

def _z8_get_parent_dir(goods_id) -> str:
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
    body = MyRequests.get_url_body(url=url, headers=headers, params=None, high_conceal=True, ip_pool_type=IP_POOL_TYPE)
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

def _jp_get_parent_dir(phantomjs, goods_id):
    '''
    卷皮获取parent_dir(常规, 秒杀, 拼团皆可调用)
    :param goods_id:
    :return: '' | 'xxx/xxx'
    '''
    url = 'http://shop.juanpi.com/deal/{0}'.format(goods_id)
    try:
        body = phantomjs.use_phantomjs_to_get_url_body(url=url)
        # print(body)
    except Exception as e:
        print(e)
        return ''

    try:
        fl = Selector(text=body).css('div.place-explain.fl').extract_first()
        # print(fl)
        assert fl is not None, '获取到的fl为None!获取parent_dir失败!'
        fl_a = Selector(text=fl).css('a::text').extract()
        # print(fl_a)
        if len(fl_a) <= 2:  # eg: ['首页', '商品名']
            return ''
        parent_dir = fl_a[1:-1:1]

    except Exception as e:
        print('获取parent_dir时遇到错误(默认为""):', e)
        return ''

    # 父级路径
    parent_dir = '/'.join(parent_dir)
    # print(parent_dir)

    return parent_dir

def _mia_get_parent_dir(p_info):
    '''
    蜜芽获取parent_dir(常规, 秒杀, 拼团皆可调用)
    :param p_info:
    :return:
    '''
    parent_dir = ''
    for item in p_info:
        if item.get('p_name', '') == '分类':
            parent_dir = item.get('p_value', '')
            break

    return parent_dir

def get_sku_info_trans_record(old_sku_info, new_sku_info, is_price_change):
    '''
    返回sku_info变化需要记录的信息
    :param old_sku_info: db中原先的sku_info
    :param new_sku_info: 新采集的sku_info
    :param is_price_change: 原先sku_info的标记状态
    :return: is_price_change, sku_info_trans_time
    '''
    sku_info_trans_time = str(get_shanghai_time())
    if is_price_change == 1:        # 避免再次更新更改未被后台同步的数据
        return is_price_change, sku_info_trans_time

    if len(old_sku_info) != len(new_sku_info):
        return 1, sku_info_trans_time

    for item in old_sku_info:   # 价格, 库存变动的
        old_unique_id = item.get('unique_id', '')
        old_detail_price = item.get('detail_price', '')
        old_rest_number = item.get('rest_number', 50)
        for i in new_sku_info:
            new_unique_id = i.get('unique_id', '')
            new_detail_price = i.get('detail_price', '')
            new_rest_number = i.get('rest_number', 50)
            if old_unique_id == new_unique_id:
                if float(old_detail_price) != float(new_detail_price):
                    return 1, sku_info_trans_time
                else:
                    pass

                if old_rest_number != new_rest_number:
                    return 1, sku_info_trans_time
                else:
                    pass
            else:
                pass

    old_unique_id_list = sorted([item.get('unique_id', '') for item in old_sku_info])
    new_unique_id_list = sorted([item.get('unique_id', '') for item in new_sku_info])

    if old_unique_id_list != new_unique_id_list:    # 规格变动的
        return 1, sku_info_trans_time

    return 0, sku_info_trans_time

def _get_mogujie_pintuan_price_info_list(tmp_price_info_list) -> list:
    '''
    得到蘑菇街拼团price_info_list
    :param tmp_price_info_list:
    :return:
    '''
    return [{
        'spec_value': item_4.get('spec_value'),
        'pintuan_price': item_4.get('detail_price'),
        'detail_price': '',
        'normal_price': item_4.get('normal_price'),
        'img_url': item_4.get('img_url'),
        'rest_number': item_4.get('rest_number'),
    } for item_4 in tmp_price_info_list]

async def _get_new_db_conn(db_obj, index, logger=None, remainder=20, db_conn_type=1):
    '''
    获取新db conn
    :param db_obj: db实例化对象
    :param index: 索引值
    :param remainder: 余数
    :param db_conn_type: db连接类型(1:SqlServerMyPageInfoSaveItemPipeline|2:SqlPool)
    :return:
    '''
    if index % remainder == 0:
        _print(msg='正在重置，并与数据库建立新连接中...', logger=logger)
        if db_conn_type == 1:
            db_obj = SqlServerMyPageInfoSaveItemPipeline()
        elif db_conn_type == 2:
            db_obj = SqlPools()
        else:
            raise ValueError('db_conn_type赋值异常!')
        _print(msg='与数据库的新连接成功建立...', logger=logger)

    else:
        pass

    return db_obj

async def _get_async_task_result(tasks, logger=None) -> list:
    '''
    获取异步处理结果
    :param tasks:
    :param logger:
    :return:
    '''
    s_time = time()
    all_res = []
    try:
        success_jobs, fail_jobs = await wait(tasks)
        time_consume = time() - s_time
        msg = '此次耗时: {}s'.format(round(float(time_consume), 3))
        _print(msg=msg, logger=logger)
        all_res = [r.result() for r in success_jobs]
    except Exception as e:
        _print(msg='遇到错误:', exception=e, logger=logger, log_level=2)

    return all_res