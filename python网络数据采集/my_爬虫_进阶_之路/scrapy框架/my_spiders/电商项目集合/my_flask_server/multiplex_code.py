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

import asyncio
from asyncio import new_event_loop
from json import dumps
from scrapy.selector import Selector
import re
from time import time
from asyncio import wait
from fzutils.spider.fz_requests import MyRequests, Requests
from fzutils.data.list_utils import list_remove_repeat_dict_plus
from fzutils.internet_utils import (
    get_random_pc_ua,
    tuple_or_list_params_2_dict_params,
    get_random_phone_ua,)
from fzutils.common_utils import (
    _print,
    json_2_dict,)
from fzutils.cp_utils import get_taobao_sign_and_body
from fzutils.time_utils import (
    get_shanghai_time,
    datetime_to_timestamp,
    timestamp_to_regulartime,)
from fzutils.spider.selector import parse_field
from fzutils.spider.async_always import unblock_get_taobao_sign_and_body

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
        body = phantomjs.use_phantomjs_to_get_url_body(url=url, )
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
    返回sku_info变化需要记录的信息(弃用)
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

def _get_sku_price_trans_record(old_sku_info:list, new_sku_info:list, is_price_change, db_price_change_info, old_price_trans_time) -> tuple:
    """
    商品的纯价格变动需要记录的东西
    :param old_sku_info:
    :param new_sku_info:
    :param is_price_change:
    :param db_price_change_info: db中原先的price_change_info
    :return: is_price_change, sku_info_trans_time, price_change_info:list
    """
    def oo(is_price_change):
        """得到is_price_change and price_change_info"""
        # 用于记录规格的价格变动的list
        new_price_change_info_list = []
        for item in old_sku_info:  # 只记录规格的价格变动
            old_unique_id = item.get('unique_id', '')
            old_detail_price = item.get('detail_price', '')
            old_normal_price = item.get('normal_price', '')
            for i in new_sku_info:
                new_unique_id = i.get('unique_id', '')
                new_detail_price = i.get('detail_price', '')
                new_normal_price = i.get('normal_price', '')
                if old_unique_id == new_unique_id:
                    tmp = {}
                    try:
                        # 单独判断
                        if float(old_detail_price) != float(new_detail_price):
                            is_price_change = 1
                            tmp.update({
                                'unique_id': old_unique_id,
                                'spec_value': i.get('spec_value', ''),
                                'detail_price': new_detail_price,
                            })
                        else:
                            pass
                    except ValueError:
                        # 处理float('')报错
                        pass
                    if tmp == {}:
                        # detail_price为空 or 价格不变就跳出
                        continue

                    tmp.update({
                        'normal_price': new_normal_price,
                    })
                    new_price_change_info_list.append(tmp)
                    break
                else:
                    continue

        return is_price_change, new_price_change_info_list

    def _incremental_update(db_price_change_info, new_price_change_info, new_is_price_change) -> list:
        """
        增量更新
        :param db_price_change_info:
        :param new_price_change_info: 新变动信息
        :param new_is_price_change: 0 or 1
        :return:
        """
        def kk(target) -> dict:
            """格式化"""
            return {
                'unique_id': target.get('unique_id', ''),
                'spec_value': target.get('spec_value', ''),
                'detail_price': target.get('detail_price', ''),
                'normal_price': target.get('normal_price', ''),
            }

        res = []
        if new_is_price_change == 1:
            db_unique_id_list = list(set([item.get('unique_id', '') for item in db_price_change_info]))
            new_unique_id_list = list(set([item.get('unique_id', '') for item in new_price_change_info]))
            tmp_unique_id_list = list(set(db_unique_id_list + new_unique_id_list))

            for unique_id in tmp_unique_id_list:
                if unique_id in new_unique_id_list:
                    try:
                        _i = _get_one_item_by_unique_id(unique_id=unique_id, target_list=new_price_change_info)
                        res.append(kk(_i))
                        continue
                    except ValueError:
                        pass

                if unique_id in db_unique_id_list:
                    try:
                        _i = _get_one_item_by_unique_id(unique_id=unique_id, target_list=db_price_change_info)
                        res.append(kk(_i))
                        continue
                    except ValueError:
                        pass

        else:
            res = db_price_change_info

        return res

    now_time = str(get_shanghai_time())
    is_price_change = is_price_change if isinstance(is_price_change, int) else 0    # 处理为null的
    # 处理原生sql getdate()函数带来的转换异常!
    old_price_trans_time = str(timestamp_to_regulartime(datetime_to_timestamp(old_price_trans_time)))
    old_price_trans_time = str(old_price_trans_time) if old_price_trans_time is not None else now_time
    if is_price_change == 1:
        # 避免再次更新更改未被后台同步的数据
        new_is_price_change, new_price_change_info = oo(is_price_change=is_price_change)
        if isinstance(db_price_change_info, dict) \
                or db_price_change_info is None \
                or db_price_change_info == []:
            _ = new_price_change_info
        else:
            # 修复bug: 当cp 后台未同步时, 保持增量更新新变动的信息
            _ = _incremental_update(db_price_change_info, new_price_change_info, new_is_price_change)
            old_price_trans_time = now_time if new_is_price_change == 1 else old_price_trans_time

        return is_price_change, old_price_trans_time, _

    is_price_change, _ = oo(is_price_change)
    new_price_trans_time = now_time if is_price_change == 1 else old_price_trans_time

    return is_price_change, new_price_trans_time, _

def _get_spec_trans_record(old_sku_info:list, new_sku_info:list, is_spec_change, old_spec_trans_time):
    """
    商品的纯规格变动需要记录的东西
    :param old_sku_info:
    :param new_sku_info:
    :param is_spec_change:
    :return:
    """
    now_time = str(get_shanghai_time())
    is_spec_change = is_spec_change if isinstance(is_spec_change, int) else 0
    # 处理原生sql getdate()函数带来的转换异常!
    old_spec_trans_time = str(timestamp_to_regulartime(datetime_to_timestamp(old_spec_trans_time)))
    old_spec_trans_time = str(old_spec_trans_time) if old_spec_trans_time is not None else now_time
    if is_spec_change == 1:
        # 避免再次更新更改未被后台同步的数据
        return is_spec_change, old_spec_trans_time

    try:
        old_unique_id_list = sorted([item.get('unique_id', '') for item in old_sku_info])
        new_unique_id_list = sorted([item.get('unique_id', '') for item in new_sku_info])
    except Exception:
        return 1, now_time

    if old_unique_id_list != new_unique_id_list:
        # 规格变动
        return 1, now_time

    return is_spec_change, old_spec_trans_time

def _get_stock_trans_record(old_sku_info:list, new_sku_info:list, is_stock_change, db_stock_change_info, old_stock_trans_time):
    '''
    商品库存变化记录的东西
    :param old_sku_info:
    :param new_sku_info:
    :param is_stock_change:
    :param db_stock_change_info: db原先的stock_change_info
    :return: is_stock_change, stock_trans_time, stock_change_info:list
    '''
    def oo(is_stock_change):
        """得到is_stock_change, 跟stock_change_info"""
        _ = []
        for item in old_sku_info:  # 只记录规格的价格变动
            old_unique_id = item.get('unique_id', '')
            old_rest_number = item.get('rest_number', 50)
            for i in new_sku_info:
                new_unique_id = i.get('unique_id', '')
                new_rest_number = i.get('rest_number', 50)
                if old_unique_id == new_unique_id:
                    if old_rest_number != new_rest_number:
                        # 小于等于10个, 即时更新 or 变动比例在.2才记录
                        if new_rest_number <= 10 \
                                or abs(new_rest_number-old_rest_number)/old_rest_number > .2:
                            is_stock_change = 1
                            _.append({
                                'unique_id': old_unique_id,
                                'spec_value': i.get('spec_value', ''),
                                'rest_number': new_rest_number,
                            })
                            break
                        else:
                            continue
                    else:
                        continue
                else:
                    continue

        return is_stock_change, _

    def _incremental_update(db_stock_change_info, new_stock_change_info, new_is_stock_change) -> list:
        """
        增量更新
        :param db_price_change_info:
        :param new_price_change_info: 新变动信息
        :param new_is_price_change: 0 or 1
        :return:
        """
        def kk(target) -> dict:
            """格式化"""
            return {
                'unique_id': target.get('unique_id', ''),
                'spec_value': target.get('spec_value', ''),
                'rest_number': target.get('rest_number', 50),
            }

        res = []
        if new_is_stock_change == 1:
            db_unique_id_list = list(set([item.get('unique_id', '') for item in db_stock_change_info]))
            new_unique_id_list = list(set([item.get('unique_id', '') for item in new_stock_change_info]))
            tmp_unique_id_list = list(set(db_unique_id_list + new_unique_id_list))

            for unique_id in tmp_unique_id_list:
                if unique_id in new_unique_id_list:
                    try:
                        _i = _get_one_item_by_unique_id(unique_id=unique_id, target_list=new_stock_change_info)
                        res.append(kk(_i))
                        continue
                    except ValueError:
                        pass

                if unique_id in db_unique_id_list:
                    try:
                        _i = _get_one_item_by_unique_id(unique_id=unique_id, target_list=db_stock_change_info)
                        res.append(kk(_i))
                        continue
                    except ValueError:
                        pass

        else:
            res = db_stock_change_info

        return res

    now_time = str(get_shanghai_time())
    # 处理原生sql getdate()函数带来的转换异常!
    old_stock_trans_time = str(timestamp_to_regulartime(datetime_to_timestamp(old_stock_trans_time)))
    old_stock_trans_time = str(old_stock_trans_time) if old_stock_trans_time is not None else now_time
    if is_stock_change == 1:
        # 避免再次更新更改未被后台同步的数据
        new_is_stock_change, new_stock_change_info = oo(is_stock_change=is_stock_change)
        if db_stock_change_info is None \
            or db_stock_change_info == []:
            _ = new_stock_change_info
        else:
            # 修复bug: 当cp 后台未同步时, 保持增量更新新变动的信息
            _ = _incremental_update(db_stock_change_info, new_stock_change_info, new_is_stock_change)
            old_stock_trans_time = now_time if new_is_stock_change == 1 else old_stock_trans_time

        return is_stock_change, old_stock_trans_time, _

    is_stock_change = is_stock_change if is_stock_change is not None else 0
    is_stock_change, _ = oo(is_stock_change)
    new_stock_trans_time = now_time if is_stock_change == 1 else old_stock_trans_time

    return is_stock_change, new_stock_trans_time, _

def _get_one_item_by_unique_id(unique_id, target_list) -> dict:
    """
    返回变动信息中对应unique_id的item
    :param unique_id:
    :param target_list:
    :return:
    """
    for item in target_list:
        if item.get('unique_id', '') == unique_id:
            return item

    raise ValueError('未发现对应unique_id的item!')

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

async def _print_db_old_data(logger, result) -> None:
    '''
    打印db的老数据
    :param self:
    :param select_sql_str:
    :param delete_sql_str:
    :return:
    '''
    if isinstance(result, list):
        logger.info('------>>> 下面是数据库返回的所有符合条件的data <<<------')
        logger.info(str(result))
        logger.info('--------------------------------------------------- ')
        logger.info('待更新个数: {0}'.format(len(result)))
        logger.info('即将开始实时更新数据, 请耐心等待...'.center(100, '#'))

    return

def _get_phone_headers() -> dict:
    return {
        'upgrade-insecure-requests': '1',
        'user-agent': get_random_phone_ua(),
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

def _get_al_one_type_company_id_list(ip_pool_type, logger, keyword:str='塑料合金', page_num:int=100, timeout=15) -> list:
    '''
    获取某个子分类的单页的company_id_list
    :param keyword:
    :return: [{'company_id': xxx, 'province_name': xxx, 'city_name':xxx}, ...]
    '''
    def _get_params() -> tuple:
        return (
            ('jsv', '2.4.11'),
            ('appKey', '12574478'),
            ('api', 'mtop.1688.offerService.getOffers'),
            ('v', '1.0'),
            ('type', 'jsonp'),
            ('dataType', 'jsonp'),
            ('callback', 'mtopjsonp3'),
            # ('t', '1545810411923'),
            # ('sign', 'a39f6182845e02c9159e36fd4dc8f108'),
        )

    def _get_request_data() -> str:
        return dumps({
            'appName': 'wap',
            'beginPage': page_num,
            'keywords': keyword,
            'pageSize': 20,
            # 'spm': 'a26g8.7710019.0.0'
        })

    headers = _get_phone_headers()
    headers.update({
        # 'referer': 'https://m.1688.com/offer_search/-CBDCC1CFBACFBDF0.html?spm=a26g8.7710019.0.0',
        'authority': 'h5api.m.1688.com',
    })
    params = _get_params()
    data = _get_request_data()
    params = tuple_or_list_params_2_dict_params(params)
    base_url = 'https://h5api.m.1688.com/h5/mtop.1688.offerservice.getoffers/1.0/'

    loop = new_event_loop()
    res1 = loop.run_until_complete(get_taobao_sign_and_body(
        base_url=base_url,
        headers=headers,
        params=params,
        data=data,
        timeout=timeout,
        ip_pool_type=ip_pool_type,
        logger=logger))
    _m_h5_tk = res1[0]
    error_record_msg = '出错keyword:{}, page_num:{}'.format(keyword, page_num)
    if _m_h5_tk == '':
        logger.error('获取到的_m_h5_tk为空str!' + error_record_msg)
        logger.info('[{}] keyword:{}, page_num:{}'.format('-', keyword, page_num))

        return []

    res2 = loop.run_until_complete(get_taobao_sign_and_body(
        base_url=base_url,
        headers=headers,
        params=params,
        data=data,
        _m_h5_tk=_m_h5_tk,
        session=res1[1],
        ip_pool_type=ip_pool_type,
        logger=logger,
        timeout=timeout))
    # 显式关闭事件循环: 避免 OSError too many files open错误!
    try:
        loop.close()
        try:
            del loop
        except:
            pass
    except:
        pass
    try:
        body = res2[2]
        # self.lg.info(body)
        _ = json_2_dict(
            json_str=re.compile('\((.*)\)').findall(body)[0],
            default_res={}).get('data', {}).get('offers', [])
        # pprint(_)
    except IndexError:
        logger.error('获取body时索引异常!' + error_record_msg)
        return []

    logger.info('[{}] keyword:{}, page_num:{}'.format('+' if _ != [] else '-', keyword, page_num))

    member_id_list = []
    for i in _:
        if i.get('memberId') is not None:
            member_id = i.get('memberId', '')
            # if 'al' + member_id not in db_al_unique_id_list:
            #     # 先去重避免重复建任务
            #     member_id_list.append({
            #         'company_id': member_id,
            #         'province_name': i.get('province', ''),
            #         'city_name': i.get('city', ''),
            #     })
            # else:
            #     # self.lg.info('not create task again, company_id: {} in db!'.format(member_id))
            #     pass

            if len(i.get('province_name', '')) > 8 \
                or len(i.get('city_name', '')) > 10:
                # 获取省份or城市名异常的跳过!
                continue

            # 外部进行去重
            member_id_list.append({
                'company_id': member_id,
                'province_name': i.get('province', ''),
                'city_name': i.get('city', ''),
            })

    # list 内部dict去重
    member_id_list = list_remove_repeat_dict_plus(target=member_id_list, repeat_key='company_id')
    # pprint(member_id_list)
    # al company url: https://m.1688.com/winport/company/b2b-3221063020830e2.html

    return member_id_list

def _get_114_one_type_company_id_list(ip_pool_type,
                                      num_retries,
                                      parser_obj,
                                      cate_num,
                                      page_num,
                                      logger=None,) -> list:
    '''
    获取114单个子分类的单个页面所有的公司简介的url(m站, pc站无列表显示)
    :param ip_pool_type:
    :param num_retries:
    :param parser_obj:
    :param cate_num: int
    :param page_num: str '' | '2', ...
    :param logger:
    :return: [{'company_id': 'xxx'}, ...]
    '''
    headers = _get_phone_headers()
    headers.update({
        'Proxy-Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    })
    # 第一页是c-xx.html, 后续都是c-xx-yy
    url = 'http://m.114pifa.com/c-{}{}{}'.format(
        cate_num,
        '' if page_num == '' else '-{}'.format(page_num),
        '.html' if page_num == '' else '')
    # self.lg.info(url)

    # TODO 测试发现大量cate_num的单页都为空值! 属于正常情况!
    body = Requests.get_url_body(
        url=url,
        headers=headers,
        ip_pool_type=ip_pool_type,
        num_retries=num_retries,
        encoding='gbk')
    # logger.info(body)

    brief_url_list = parse_field(
        parser=parser_obj['one_type_url_list'],
        target_obj=body,
        is_first=False,
        logger=logger)
    # pprint(brief_url_list)

    company_id_list = []
    for item in brief_url_list:
        try:
            company_id = parse_field(
                parser=parser_obj['one_type_url_list_item'],
                target_obj=item,
                logger=logger)
            assert company_id != '', 'company_id不为空值!'
        except AssertionError:
            continue
        company_id_list.append({
            'company_id': company_id,
        })

    company_id_list = list_remove_repeat_dict_plus(target=company_id_list, repeat_key='company_id')
    logger.info('[{}] url: {}'.format('+' if company_id_list != [] else '-', url))

    return company_id_list

def _handle_goods_shelves_in_auto_goods_table(goods_id, logger=None, update_sql_str=None) -> bool:
    """
    商品逻辑下架(GoodsInfoAutoGet表 or 其他表)
    :param goods_id:
    :param logger:
    :param update_sql_str: 常规表 or 拼团表 or 秒杀表的sql_str
    :return:
    """
    res = False
    _print(msg='@@@ goods_id: {}已下架, 进行逻辑删除!'.format(goods_id), logger=logger)
    sql_str = 'update dbo.GoodsInfoAutoGet set IsDelete=1, ModfiyTime=%s where GoodsID=%s' \
        if update_sql_str is None \
        else update_sql_str
    now_time = str(get_shanghai_time())
    try:
        sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        if logger is None:
            res = sql_cli._update_table(sql_str=sql_str, params=(now_time, goods_id))
        else:
            res = sql_cli._update_table_2(sql_str=sql_str, params=(now_time, goods_id), logger=logger)

        try:
            del sql_cli
        except:
            pass
    except Exception as e:
        _print(msg='遇到错误:', logger=logger, exception=e, log_level=2)

    return res