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

from my_pipeline import (
    SqlServerMyPageInfoSaveItemPipeline,
    SqlPools,)

from time import (
    time,
    mktime,
    strptime,)
from datetime import datetime
from random import uniform
# cpu密集型
# from multiprocessing import Pool, cpu_count
# IO密集型
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count
from sys import path as sys_path
from my_exceptions import (
    SqlServerConnectionException,
    DBGetGoodsSkuInfoErrorException,)
from sql_str_controller import (
    cm_insert_str_2,
    al_select_str_2,
    cm_update_str_2,
    tm_update_str_1,
    tb_update_str_1,
)

from fzutils.data.list_utils import list_remove_repeat_dict_plus
from fzutils.common_utils import (
    _print,)
from fzutils.spider.selector import parse_field
from fzutils.celery_utils import _get_celery_async_results
from fzutils.cp_utils import _get_right_model_data
from fzutils.exceptions import ResponseBodyIsNullStrException
from fzutils.thread_utils import ThreadTaskObj
from fzutils.spider.async_always import *

def block_get_one_goods_info_task_by_external_type(external_type: str,
                                                   goods_id: (list, str),
                                                   index: int,
                                                   logger=None,):
    """
    根据外链类型阻塞获取单个goods信息
    :param external_type: eg: 'tm', 'tb'
    :param goods_id:
    :param index:
    :param logger:
    :return:
    """
    # 放在内部, 外部导异常
    from tmall_parse_2 import TmallParse
    from taobao_parse import TaoBaoLoginAndParse

    if external_type == 'tm':
        external_obj = TmallParse(logger=logger, is_real_times_update_call=True)
        site_id, _goods_id = goods_id
        before_goods_data = external_obj.get_goods_data(goods_id=goods_id)
        end_goods_data = external_obj.deal_with_data()

    elif external_type == 'tb':
        external_obj = TaoBaoLoginAndParse(logger=logger, is_real_times_update_call=True)
        site_id, _goods_id = 1, goods_id
        before_goods_data = external_obj.get_goods_data(goods_id=goods_id)
        end_goods_data = external_obj.deal_with_data(goods_id=goods_id)

    else:
        raise ValueError('external_type value: {} 异常!'.format(external_type))

    # 处理前后某个为1, 则为1
    is_delete = 1 \
        if before_goods_data.get('is_delete', 0) == 1 or end_goods_data.get('is_delete', 0) == 1 \
        else 0
    _label = '+' \
        if end_goods_data != {} or is_delete == 1 \
        else '-'
    msg = '[{}] goods_id: {}, site_id: {}, is_delete: {}, index: {}'.format(
        _label,
        _goods_id,
        site_id,
        is_delete,
        index,
    )
    _print(msg=msg, logger=logger)

    try:
        del external_obj
    except:
        pass

    return (site_id, _goods_id, index, before_goods_data, end_goods_data)

async def async_get_ms_begin_time_and_miaos_end_time_from_ms_time(miaosha_time: str, logger=None) -> tuple:
    """
    根据ms_time 获取开始时间跟结束时间
    :param miaosha_time: '{xxx}'
    :param logger:
    :return: (int, int)
    """
    ms_time = json_2_dict(
        json_str=miaosha_time,
        default_res={},
        logger=logger,)
    ms_begin_time = ms_time.get('miaosha_begin_time', '')
    ms_end_time = ms_time.get('miaosha_end_time', '')
    ms_begin_time = int(str(mktime(strptime(ms_begin_time, '%Y-%m-%d %H:%M:%S')))[0:10])
    ms_end_time = int(str(mktime(strptime(ms_end_time, '%Y-%m-%d %H:%M:%S')))[0:10])

    return ms_begin_time, ms_end_time

async def get_waited_2_update_db_data_from_server(server_ip: str='http://0.0.0.0:5000',
                                                  _type: str='tm',
                                                  child_type: int=0) -> list:
    """
    从server获取待更新数据
    :return:
    """
    url = server_ip + '/spider/dcs'
    params = (
        ('type', _type),
        ('child_type', child_type),
    )
    body = await unblock_request(
        url=url,
        params=params,
        use_proxy=False,
        timeout=40,)
    res = json_2_dict(
        json_str=body,
        default_res={},).get('data', [])

    return res

def _z8_get_parent_dir(goods_id) -> str:
    '''
    折800获取parent_dir (常规, 拼团, 秒杀都可用)
    :param goods_id:
    :return: '' | 'xxx/xxx'
    '''
    headers = get_random_headers(connection_status_keep_alive=False,)
    headers.update({
        'authority': 'shop.zhe800.com',
        # 'referer': 'https://brand.zhe800.com/yl?brandid=353130&page_stats_w=ju_tag/taofushi/1*1&ju_flag=1&pos_type=jutag&pos_value=taofushi&x=1&y=1&n=1&listversion=&sourcetype=brand&brand_id=353130',
    })
    params = (
        ('jump_source', '1'),
        ('qd_key', 'qyOwt6Jn'),
    )
    url = 'https://shop.zhe800.com/products/{0}'.format(goods_id)
    body = Requests.get_url_body(
        url=url,
        headers=headers,
        params=None,
        ip_pool_type=IP_POOL_TYPE)
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
    try:
        old_price_trans_time = str(timestamp_to_regulartime(datetime_to_timestamp(old_price_trans_time)))
    except AttributeError:
        pass
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
    try:
        old_spec_trans_time = str(timestamp_to_regulartime(datetime_to_timestamp(old_spec_trans_time)))
    except AttributeError:
        pass
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
    try:
        old_stock_trans_time = str(timestamp_to_regulartime(datetime_to_timestamp(old_stock_trans_time)))
    except AttributeError:
        pass
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

def _get_price_change_info(old_price, old_taobao_price, new_price, new_taobao_price, is_price_change, price_change_info):
    '''
    公司用来记录价格改变信息
    :param old_price: 原始最高价 type Decimal
    :param old_taobao_price: 原始最低价 type Decimal
    :param new_price: 新的最高价
    :param new_taobao_price: 新的最低价
    :return: is_price_change 0 or 1 | _
    '''
    # print(old_price)
    # print(type(old_price))
    # print(new_price)
    # print(type(new_price))
    if is_price_change == 0:
        # 处理单规格的情况, 价格变动置1, price, taobao_price每次更新都是更新的
        if float(old_price) != float(new_price) \
                or float(old_taobao_price) != float(new_taobao_price):
            is_price_change = 1
        else:
            pass

    else:
        pass

    return is_price_change, price_change_info

def get_goods_info_change_data(target_short_name: str, logger=None, **kwargs) -> dict:
    """
    获取goods要被记录的商品信息
    :param target_short_name:
    :param logger:
    :param kwargs:
    :return:
    """
    data = kwargs.get('data', {})
    db_goods_info_obj = kwargs['db_goods_info_obj']

    data['goods_id'] = db_goods_info_obj.goods_id
    data['shelf_time'], data['delete_time'] = get_shelf_time_and_delete_time(
        tmp_data=data,
        is_delete=db_goods_info_obj.is_delete,
        shelf_time=db_goods_info_obj.shelf_time,
        delete_time=db_goods_info_obj.delete_time,)

    # 获取site_id
    if target_short_name == 'tm':
        site_id = from_tmall_type_get_site_id(type=data['type'])
    elif target_short_name == 'jd':
        site_id = get_site_id_by_jd_type(jd_type=data['jd_type'])
    else:
        site_id = db_goods_info_obj.site_id

    price_info_list = old_sku_info = db_goods_info_obj.old_sku_info
    try:
        old_sku_info = format_price_info_list(
            price_info_list=price_info_list,
            site_id=site_id)
    except AttributeError:
        # 处理已被格式化过的
        pass

    # 获取新goods的规格list
    if target_short_name == 'al':
        tmp_price_info_list = data['sku_map']
    else:
        tmp_price_info_list = data['price_info_list']
    new_sku_info = format_price_info_list(
        price_info_list=tmp_price_info_list,
        site_id=site_id,)

    try:
        data['_is_price_change'], data['sku_info_trans_time'], price_change_info = _get_sku_price_trans_record(
            old_sku_info=old_sku_info,
            new_sku_info=new_sku_info,
            is_price_change=db_goods_info_obj.is_price_change,
            db_price_change_info=db_goods_info_obj.db_price_change_info,
            old_price_trans_time=db_goods_info_obj.old_price_trans_time)

        # 处理单规格的情况
        # _price_change_info这个字段不进行记录, 还是记录到price, taobao_price
        data['_is_price_change'], data['_price_change_info'] = _get_price_change_info(
            old_price=db_goods_info_obj.old_price,
            old_taobao_price=db_goods_info_obj.old_taobao_price,
            new_price=data['price'],
            new_taobao_price=data['taobao_price'],
            is_price_change=data['_is_price_change'],
            price_change_info=price_change_info)
        if data['_is_price_change'] == 1:
            _print(
                msg='{:10s} [{}]'.format(
                    'price changed!',
                    db_goods_info_obj.goods_id),
                logger=logger, )
            # pprint(data['_price_change_info'])

        # 监控纯规格变动
        data['is_spec_change'], data['spec_trans_time'] = _get_spec_trans_record(
            old_sku_info=old_sku_info,
            new_sku_info=new_sku_info,
            is_spec_change=db_goods_info_obj.is_spec_change,
            old_spec_trans_time=db_goods_info_obj.old_spec_trans_time, )
        if data['is_spec_change'] == 1:
            _print(
                msg='{:10s} [{}]'.format(
                    'specs changed!',
                    db_goods_info_obj.goods_id),
                logger=logger, )

        # 监控纯库存变动
        data['is_stock_change'], data['stock_trans_time'], data['stock_change_info'] = _get_stock_trans_record(
            old_sku_info=old_sku_info,
            new_sku_info=new_sku_info,
            is_stock_change=db_goods_info_obj.is_stock_change,
            db_stock_change_info=db_goods_info_obj.db_stock_change_info,
            old_stock_trans_time=db_goods_info_obj.old_stock_trans_time)
        if data['is_stock_change'] == 1:
            _print(
                msg='{:10s} [{}]'.format(
                    'stock changed!',
                    db_goods_info_obj.goods_id),
                logger=logger, )

    except Exception as e:
        # 记录goods_id, 并抛出异常!
        _print(
            msg='出错goods_id: {}'.format(db_goods_info_obj.goods_id),
            logger=logger,
            log_level=2,
            exception=e,)
        raise e

    # 单独处理起批量>=1的
    if target_short_name == 'al':
        begin_greater_than_1 = al_judge_begin_greater_than_1(
            price_info=data['price_info'],
            logger=logger,)
        if begin_greater_than_1:
            _print(
                msg='该商品 起批量 大于1, 下架!!',
                logger=logger,)
            data['is_delete'] = 1
    else:
        pass

    _print(
        msg='upper_shelf_time: {0}, off_shelf_time: {1}'.format(
            data['shelf_time'],
            data['delete_time']),
        logger=logger,)

    try:
        del db_goods_info_obj
    except:
        pass

    return data

class BaseDbCommomGoodsInfoParamsObj(object):
    """
    常规goods更新db需求参数对象
        适用: ('tm', ...)
    """
    def __init__(self, item: list, logger=None):
        assert item != [], 'item != []'
        # default value, 取第一个
        self.site_id = item[0]
        self.goods_id = item[1]
        self.is_delete = item[2]
        self.old_price = item[3]
        self.old_taobao_price = item[4]
        self.shelf_time = item[5]
        self.delete_time = item[6]
        self.old_sku_info = json_2_dict(
            json_str=item[7],
            default_res=[],
            logger=logger,)
        self.is_price_change = item[8] if item[8] is not None else 0
        self.is_spec_change = item[9] if item[9] is not None else 0
        self.db_price_change_info = json_2_dict(
            json_str=item[10],
            default_res=[],
            logger=logger, )
        self.is_stock_change = item[11] if item[11] is not None else 0
        self.db_stock_change_info = json_2_dict(
            json_str=item[12],
            default_res=[],
            logger=logger)
        self.old_price_trans_time = item[13]
        self.old_spec_trans_time = item[14]
        self.old_stock_trans_time = item[15]

def get_site_id_by_jd_type(jd_type) -> int:
    '''
    根据jd_type来获取对应的site_id的值
    :param jd_type:
    :return:
    '''
    # 采集的来源地
    if jd_type == 7:
        site_id = 7     # 采集来源地(京东)
    elif jd_type == 8:
        site_id = 8     # 采集来源地(京东超市)
    elif jd_type == 9:
        site_id = 9     # 采集来源地(京东全球购)
    elif jd_type == 10:
        site_id = 10    # 采集来源地(京东大药房)
    else:
        site_id = 0     # 表示错误

    return site_id

def al_judge_begin_greater_than_1(price_info: list, logger) -> bool:
    '''
    al判断起批量是否大于1, 大于1则返回True, <=1 返回False
    :return:
    '''
    if price_info == []:
        return False

    try:
        price_info.sort(key=lambda item: int(item.get('begin')))
        # pprint(price_info)
        if int(price_info[0]['begin']) > 1:
            return True
        else:
            return False

    except Exception:
        logger.error('遇到错误:', exc_info=True)
        return True

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

def _block_get_new_db_conn(db_obj, index, logger=None, remainder=20, db_conn_type=1):
    '''
    获取新db conn
    :param db_obj: db实例化对象
    :param index: 索引值
    :param remainder: 余数
    :param db_conn_type: db连接类型(1:SqlServerMyPageInfoSaveItemPipeline|2:SqlPool)
    :return:
    '''
    if index % remainder == 0:
        _print(msg='init sql_cli ...', logger=logger)
        if db_conn_type == 1:
            db_obj = SqlServerMyPageInfoSaveItemPipeline()
        elif db_conn_type == 2:
            db_obj = SqlPools()
        else:
            raise ValueError('db_conn_type赋值异常!')
        _print(msg='init over !', logger=logger)

    else:
        pass

    if not db_obj.is_connect_success:
        # 连接失败则进行多次连接获取新对象
        db_obj = get_new_sql_cli(sql_cli=db_obj, num_retries=3)
    else:
        pass

    return db_obj

async def _get_new_db_conn(*params, **kwargs):
    '''
    异步获取新db conn
    :param db_obj: db实例化对象
    :param index: 索引值
    :param remainder: 余数
    :param db_conn_type: db连接类型(1:SqlServerMyPageInfoSaveItemPipeline|2:SqlPool)
    :return:
    '''
    return _block_get_new_db_conn(*params, **kwargs)

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

def _block_print_db_old_data(result, logger=None,) -> None:
    """
    打印db老数据
    :param logger:
    :param result:
    :return:
    """
    if isinstance(result, list):
        _print(msg='------>>> 下面是数据库返回的所有符合条件的data <<<------', logger=logger)
        _print(msg=str(result), logger=logger)
        _print(msg='--------------------------------------------------- ', logger=logger)
        _print(msg='待更新个数: {0}'.format(len(result)), logger=logger)
        _print(msg='即将开始实时更新数据, 请耐心等待...'.center(100, '#'), logger=logger)

    return

async def _print_db_old_data(*params, **kwargs) -> None:
    '''
    异步打印db的老数据
    :param self:
    :param select_sql_str:
    :param delete_sql_str:
    :return:
    '''
    return _block_print_db_old_data(*params, **kwargs)

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

    headers = get_random_headers(
        user_agent_type=1,
        connection_status_keep_alive=False,
        cache_control='',)
    headers.update({
        # 'referer': 'https://m.1688.com/offer_search/-CBDCC1CFBACFBDF0.html?spm=a26g8.7710019.0.0',
        'authority': 'h5api.m.1688.com',
    })
    params = _get_params()
    data = _get_request_data()
    params = tuple_or_list_params_2_dict_params(params)
    base_url = 'https://h5api.m.1688.com/h5/mtop.1688.offerservice.getoffers/1.0/'

    res1 = block_get_tb_sign_and_body(
        base_url=base_url,
        headers=headers,
        params=params,
        data=data,
        timeout=timeout,
        ip_pool_type=ip_pool_type,
        logger=logger)
    _m_h5_tk = res1[0]
    error_record_msg = '出错keyword:{}, page_num:{}'.format(keyword, page_num)
    if _m_h5_tk == '':
        logger.error('获取到的_m_h5_tk为空str!' + error_record_msg)
        logger.info('[{}] keyword:{}, page_num:{}'.format('-', keyword, page_num))

        return []

    res2 = block_get_tb_sign_and_body(
        base_url=base_url,
        headers=headers,
        params=params,
        data=data,
        _m_h5_tk=_m_h5_tk,
        session=res1[1],
        ip_pool_type=ip_pool_type,
        logger=logger,
        timeout=timeout)
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
            if len(i.get('province_name', '')) > 8 \
                or len(i.get('city_name', '')) > 10:
                # 获取省份or城市名异常的跳过!
                continue

            province_name = i.get('province', '')
            city_name = i.get('city', '')
            if province_name == 'CN':
                # province_name = 'CN', city_name = 'xxx' eg: '北京', '天津' 的情况单独处理
                province_name = city_name
            else:
                pass

            # 外部进行去重
            member_id_list.append({
                'company_id': member_id,
                'province_name': province_name,
                'city_name': city_name,
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
    headers = get_random_headers(
        user_agent_type=1,
        connection_status_keep_alive=False,
        cache_control='', )
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

def get_new_sql_cli(sql_cli, num_retries=3):
    """
    获取new_sql_cli
    :param sql_cli: 原先对象
    :return:
    """
    if isinstance(sql_cli, SqlServerMyPageInfoSaveItemPipeline):
        new_sql_cli = SqlServerMyPageInfoSaveItemPipeline()
    elif isinstance(sql_cli, SqlPools):
        new_sql_cli = SqlPools()
    else:
        raise TypeError('sql_cli type 异常!')

    if not new_sql_cli.is_connect_success and num_retries > 0:
        return get_new_sql_cli(
            sql_cli=new_sql_cli,
            num_retries=num_retries-1)
    else:
        pass

    return new_sql_cli

def _handle_goods_shelves_in_auto_goods_table(goods_id,
                                              logger=None,
                                              update_sql_str=None,
                                              sql_cli=None) -> bool:
    """
    商品逻辑下架(GoodsInfoAutoGet表 or 其他表)
    :param goods_id:
    :param logger:
    :param update_sql_str: 常规表 or 拼团表 or 秒杀表的sql_str
    :param sql_cli: db连接对象
    :return:
    """
    def off_shelves_goods() -> bool:
        nonlocal goods_id, logger
        nonlocal update_sql_str, sql_cli

        res = False
        _print(msg='@@@ goods_id: {} 已下架, 逻辑删!'.format(goods_id), logger=logger)
        sql_str = 'update dbo.GoodsInfoAutoGet set IsDelete=1, ModfiyTime=%s where GoodsID=%s' \
            if update_sql_str is None \
            else update_sql_str
        sql_str_2 = 'select top 1 delete_time from dbo.GoodsInfoAutoGet where GoodsID=%s'
        sql_str_3 = 'update dbo.GoodsInfoAutoGet set delete_time=%s where GoodsID=%s'
        try:
            now_time = str(get_shanghai_time())
            new_sql_cli = SqlServerMyPageInfoSaveItemPipeline() if sql_cli is None else sql_cli
            if not new_sql_cli.is_connect_success:
                # 报错: malloc: *** error for object 0x102a3f200: pointer being freed was not allocated
                # 因为new_sql_cli中的某个地址呗多次回收导致异常
                # sleep(uniform(1, 8))
                new_sql_cli = get_new_sql_cli(sql_cli=new_sql_cli, num_retries=5)
                if not new_sql_cli.is_connect_success:
                    raise SqlServerConnectionException
                else:
                    pass
            else:
                pass

            if 'GoodsInfoAutoGet' in sql_str:
                # 处理GoodsInfoAutoGet中异常下架但是delete_time为空值的商品
                res2 = new_sql_cli._select_table(
                    sql_str=sql_str_2,
                    params=(goods_id,),
                    logger=logger,)[0][0]
                # pprint(res2)
                if res2 is None:
                    # 更新下架时间
                    # 处理GoodsInfoAutoGet中异常下架但是delete_time为空值的商品
                    _print(msg='@@@原先delete_time为空值, 此处赋值now_time [{}]'.format(goods_id), logger=logger)
                    new_sql_cli._update_table_2(
                        sql_str=sql_str_3,
                        params=(now_time, goods_id),
                        logger=logger)
                else:
                    pass
            else:
                pass

            if logger is None:
                res = new_sql_cli._update_table(
                    sql_str=sql_str,
                    params=(now_time, goods_id))
            else:
                res = new_sql_cli._update_table_2(
                    sql_str=sql_str,
                    params=(now_time, goods_id),
                    logger=logger)

            # 注释掉: del sql_cli 容易造成段错误: c指针异常 segmentation fault
            # todo 改用内参数new_sql_cli来重新赋值sql_cli避免删除传参时带来的段错误
            try:
                del new_sql_cli
            except:
                pass

        except Exception as e:
            _print(
                msg='遇到错误:',
                logger=logger,
                exception=e,
                log_level=2)

        return res

    # 开线程来做
    task_obj = ThreadTaskObj(
        func_name=off_shelves_goods,
        args=(),
        default_res=False,
        logger=logger,)
    task_obj.start()
    res = task_obj._get_result()

    try:
        del task_obj
    except:
        pass

    return res

def _get_random_head_img_url_from_db(need_head_img_num:int=1, logger=None) -> list:
    """
    从头像db中获取n张随机head url
    :param need_head_img_num: 获取头像数
    :return: ['xxxx', ...]
    """
    sql_str = '''
    declare @d Datetime  
    set @d=getdate()   
    select top {need_head_img_num} head_img_url
    from dbo.sina_weibo 
    where 0.01 >= cast(checksum(newid(), id) & 0x7fffffff as float) / cast (0x7fffffff as int)  
    '''.format(need_head_img_num=need_head_img_num)
    head_img_url_list = []
    try:
        sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        db_random_head_img_url_list = sql_cli._select_table(sql_str=sql_str, logger=logger)
        try:
            del sql_cli
        except:
            pass

        for item in db_random_head_img_url_list:
            try:
                head_img_url_list.append(item[0])
            except IndexError:
                continue
    except Exception as e:
        _print(msg='遇到错误:', logger=logger, exception=e, log_level=2)

    return head_img_url_list

def get_top_n_buyer_name_and_comment_date_by_goods_id(goods_id, top_n_num=1500, logger=None) -> list:
    """
    获取某goods_id前n个comment的buyer_name and comment_date
    :param goods_id:
    :param top_n_num: 前n个
    :param logger:
    :return:
    """
    res = []
    sql_str = 'select top {top_n_num} buyer_name, comment_date from dbo.goods_comment_new where goods_id=%s'\
        .format(top_n_num=top_n_num)
    # _print(msg=sql_str)
    # 必须放在try外, 连接异常则立即抛出异常
    sql_cli = SqlServerMyPageInfoSaveItemPipeline()
    if not sql_cli.is_connect_success:
        # 连接失败抛出连接异常!
        raise SqlServerConnectionException

    try:
        res = sql_cli._select_table(
            sql_str=sql_str,
            params=(str(goods_id),),
            logger=logger)
        try:
            del sql_cli
        except:
            pass
    except Exception as e:
        _print(msg='遇到错误:', logger=logger, exception=e, log_level=2)

    return res

def filter_crawled_comment_content(new_buyer_name:str, new_comment_date, db_buyer_name_and_comment_date_info:list, logger=None) -> bool:
    """
    过滤已采集的评论内容
    :param new_buyer_name:
    :param new_comment_date:
    :param db_buyer_name_and_comment_date_info: db中已采集的buyer_name, comment_date list
    :return: 已存在返回 True
    """
    res = True
    db_buyer_name_list = []
    try:
        db_buyer_name_list = [item[0] for item in db_buyer_name_and_comment_date_info]
        # print(db_buyer_name_list)
    except TypeError:
        # 处理db中没有的由于sql查询
        pass

    if new_buyer_name not in db_buyer_name_list:
        # 先排除名字不在卖家名list中的
        return True

    new_comment_date = string_to_datetime(new_comment_date)
    for item in db_buyer_name_and_comment_date_info:
        item_buyer_name = item[0]
        item_comment_date = string_to_datetime(str(item[1]))

        if new_buyer_name == item_buyer_name:
            # print(new_buyer_name, type(new_comment_date), new_comment_date, type(item_comment_date), item_comment_date)
            if new_comment_date == item_comment_date:
                # 名字相同且comment_date也相同的, 即为重复的comment data
                _print(
                    msg='db had comment_date: {}, buyer_name: {}'.format(str(new_comment_date), new_buyer_name),
                    logger=logger,
                    log_level=1,)
                return False

    return res

def _save_comment_item_r(_r, goods_id, sql_cli=None, logger=None) -> None:
    """
    保存item r
    :param _r:
    :param goods_id:
    :return:
    """
    def _get_db_insert_params(goods_id, create_time, i,) -> tuple:
        """
        得到新版待插入数据
        :return:
        """
        comment_date = i['comment'][0]['comment_date']
        try:
            append_comment_date = i.get('append_comment', {}).get('comment_date', '')
            assert append_comment_date != '', 'append_comment_date为空值!'
        except AssertionError:
            # 设置个默认值!
            append_comment_date = str(datetime(1900, 1, 1))
        # logger.info('comment_date: {}, append_comment_date: {}'.format(comment_date, append_comment_date))
        return (
            goods_id,
            create_time,

            i['buyer_name'],
            i['head_img'],
            i['comment'][0]['sku_info'],
            i['quantify'],
            i['comment'][0]['comment'],
            string_to_datetime(comment_date),
            dumps(i['comment'][0].get('img_url_list', []), ensure_ascii=False),
            i['comment'][0].get('video', ''),
            i['comment'][0]['star_level'],

            i.get('append_comment', {}).get('comment', ''),
            string_to_datetime(append_comment_date),
            dumps(i.get('append_comment', {}).get('img_url_list', []), ensure_ascii=False),
        )

    def save_comment_2_db_worker(params, logger) -> bool:
        """
        save 单条comment
        :param params:
        :param logger:
        :return:
        """
        # 多线程并发存储会导致内存回收错误, 使脚本截止!: malloc: *** error for object 0x4: pointer being freed was not allocated
        res = False
        try:
            new_sql_cli = SqlServerMyPageInfoSaveItemPipeline()
            if new_sql_cli.is_connect_success:
                res = new_sql_cli._insert_into_table_2(
                    sql_str=cm_insert_str_2,
                    params=params,
                    logger=logger,
                    set_deadlock_priority_low=False, )
                if res:
                    try:
                        buyer_name = params[2]
                        logger.info('buyer_name: {} saved!'.format(buyer_name))
                    except IndexError:
                        pass
            try:
                del new_sql_cli
            except:
                pass
        except Exception:
            pass

        return res

    create_time = _r['create_time']
    comment_list = _r['_comment_list']
    # thread_pool = ThreadPool(cpu_count())

    from fzutils.gevent_utils import (
        gevent_monkey,
        GeventPool,
        gevent_joinall,)
    # sql 连接只需针对socket连接的替换即可
    gevent_monkey.patch_socket()

    # 限制并发量50个
    gevent_pool = GeventPool(50)
    tasks = []

    for i in comment_list:
        try:
            params = _get_db_insert_params(
                goods_id=goods_id,
                create_time=create_time,
                i=i,)
        except Exception as e:
            _print(msg='遇到错误:', logger=logger, exception=e, log_level=2)
            return None

        try:
            buyer_name = params[2]
        except IndexError:
            continue
        logger.info('create_task[where goods_id is {}, buyer_name is {}] ...'.format(goods_id, buyer_name))

        # 公用sql_cli 导致下方错误
        # TODO 老是报错: pymssql.OperationalError: Cannot commit transaction: (3902, b'The COMMIT TRANSACTION request has no corresponding BEGIN TRANSACTION.DB-Lib error message 20018, severity 16:\nGeneral SQL Server error: Check messages from the SQL Server\n')

        # 改用每次重连! 得以解决!
        # try:
        #     # 阻塞存
        #     save_comment_2_db_worker(params=params, logger=logger)
        #
        #     # Thread存
        #     # worker = Thread(
        #     #     target=save_comment_2_db_worker,
        #     #     name='save_2_db_worker:' + get_uuid1(),
        #     #     args=(
        #     #         params,
        #     #         logger),)
        #     # worker.setDaemon(True)
        #     # worker.start()
        # except:
        #     continue

        # 改用线程池存, 使用线程长期运行:python内部c垃圾回收错误，会导致脚本停止
        # try:
        #     thread_pool.apply_async(save_comment_2_db_worker, args=(params, logger))
        # except:
        #     # 处理segmentation fault报错
        #     # 设置为不限制 stack size, 我mac上默认限制为:8192, 不限制后mac会经常巨卡!!
        #     # $ ulimit -s unlimited
        #     continue

        # gevent
        # spawn()运行协程
        tasks.append(gevent_pool.spawn(save_comment_2_db_worker, params, logger))

    # 线程池
    # try:
    #     thread_pool.close()
    #     thread_pool.join()
    # except:
    #     pass

    # gevent
    gevent_joinall(tasks)

    collect()

    return None

def _get_sku_info_from_db_by_goods_id(goods_id, logger=None) -> list:
    '''
    从db中得到sku_info
    :param goods_id:
    :return: [''] | ['xxx', ...] | raise DBGetGoodsSkuInfoErrorException
    '''
    res = ['']
    try:
        sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        if not sql_cli.is_connect_success:
            raise SqlServerConnectionException

        _r = sql_cli._select_table(
            sql_str=al_select_str_2,
            params=(str(goods_id),))[0][0]
        # _print(msg=_r, logger=logger)
        try:
            del sql_cli
        except:
            pass
    except Exception as e:
        _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
        # 统一抛出DBGetGoodsSkuInfoErrorException
        raise DBGetGoodsSkuInfoErrorException

    sku_info = json_2_dict(
        json_str=_r,
        logger=logger,
        default_res=[])
    if sku_info == []:
        # 为空list, 即返回[''], 使其置''
        return res

    res = []
    for item in sku_info:
        spec_value = item.get('spec_value', '').replace('|', ';')
        if spec_value not in res:
            res.append(spec_value)

    collect()

    return res

def wash_goods_comment(comment_content:str) -> str:
    """
    统一清洗comment content
    :param comment_content:
    :return:
    """
    add_sensitive_str_list = []
    YIUXIU_NAME = '优秀网'
    BLANK_SPACE = ' '
    replace_str_list = [
        ('1688', YIUXIU_NAME),
        ('阿里巴巴', YIUXIU_NAME),
        ('阿里', YIUXIU_NAME),
        ('某淘', YIUXIU_NAME),
        ('某宝', YIUXIU_NAME),
        ('淘宝', YIUXIU_NAME),
        ('taobao', YIUXIU_NAME),
        ('天猫', YIUXIU_NAME),
        ('tmall', YIUXIU_NAME),
        ('jd', YIUXIU_NAME),
        ('京东', YIUXIU_NAME),
        ('zhe800', YIUXIU_NAME),
        ('折800', YIUXIU_NAME),
        ('闲鱼', YIUXIU_NAME),

        ('\r', BLANK_SPACE),
        ('\n', BLANK_SPACE),
        ('\t', BLANK_SPACE),
        ('&nbsp;', BLANK_SPACE),
    ]
    comment_content = wash_sensitive_info(
        data=comment_content,
        replace_str_list=replace_str_list,
        add_sensitive_str_list=add_sensitive_str_list,
        is_default_filter=True,
        is_lower=True,)

    return comment_content

def get_mia_pintuan_one_page_api_goods_info(page_num:(int, str)) -> list:
    """
    得到mia 拼团单页api goods
    :param page_num:
    :return:
    """
    headers = get_random_headers(upgrade_insecure_requests=False,)
    headers.update({
        'accept-language': 'zh-CN,zh;q=0.8',
        'Host': 'm.mia.com',
    })
    tmp_url = 'https://m.mia.com/instant/groupon/common_list/{}/0/'.format(str(page_num))
    print('正在抓取: ', tmp_url)
    body = Requests.get_url_body(
        url=tmp_url,
        headers=headers,
        had_referer=True,
        ip_pool_type=IP_POOL_TYPE)
    # print(body)
    if body == '':
        # 避免proxy异常导致返回空list, 错误下架商品
        raise ResponseBodyIsNullStrException

    try:
        tmp_data = json_2_dict(
            json_str=body,
            default_res={}).get('data_list', [])
        assert tmp_data != [], '得到的data_list为[], 此处跳过!'
        # print(tmp_data)
    except AssertionError as e:
        print(e)
        return []

    data_list = [{
        'goods_id': item.get('sku', ''),
        'sub_title': item.get('intro', ''),
        'pid': page_num,
    } for item in tmp_data]
    # pprint(data_list)

    return data_list

from comment_spiders.ali_1688_comment_parse import ALi1688CommentParse
from comment_spiders.taobao_comment_parse import TaoBaoCommentParse
from comment_spiders.tmall_comment_parse import TmallCommentParse
from comment_spiders.jd_comment_parse import JdCommentParse
from comment_spiders.zhe_800_comment_parse import Zhe800CommentParse

def _get_someone_goods_id_all_comment(index, site_id:int, goods_id, logger) -> dict:
    """
    获取某个goods_id的all comment info
    :param self:
    :param site_id:
    :return: (goods_id, res)
    """
    def _get_tm_type(site_id):
        """获取tm type"""
        if site_id == 3:
            _type = 0
        elif site_id == 4:
            _type = 1
        elif site_id == 6:
            _type = 2
        else:
            raise ValueError('site_id值异常!')

        return _type

    if site_id == 1:
        tb = TaoBaoCommentParse(logger=logger)
        res = tb._get_comment_data(goods_id=goods_id)
        try:
            del tb
        except:
            pass

    elif site_id == 2:
        al = ALi1688CommentParse(logger=logger)
        res = al._get_comment_data(goods_id=goods_id)
        try:
            del al
        except:
            pass

    elif site_id in (3, 4, 6):
        try:
            _type = _get_tm_type(site_id)
        except ValueError:
            return {}

        tm = TmallCommentParse(logger=logger)
        res = tm._get_comment_data(_type=_type, goods_id=goods_id)
        try:
            del tm
        except:
            pass

    elif site_id in (7, 8, 9, 10):
        jd = JdCommentParse(logger=logger)
        res = jd._get_comment_data(goods_id=goods_id)
        try:
            del jd
        except:
            pass

    elif site_id == 11:
        z8 = Zhe800CommentParse(logger=logger)
        res = z8._get_comment_data(goods_id=goods_id)
        try:
            del z8
        except:
            pass

    else:
        raise NotImplementedError

    logger.info('[{}] index: {}, goods_id: {}, site_id: {}'.format(
        '+' if res != {} else '-',
        index,
        goods_id,
        site_id,))
    collect()

    return res

async def async_get_someone_goods_id_all_comment(**kwargs):
    """
    异步的获取
    :return:
    """
    index = kwargs['index']
    site_id = kwargs['site_id']
    goods_id = kwargs['goods_id']
    logger = kwargs['logger']

    async def _get_args() -> list:
        return [
            index,
            site_id,
            goods_id,
            logger,
        ]

    loop = get_event_loop()
    args = await _get_args()
    res = {}
    try:
        res = await loop.run_in_executor(None, _get_someone_goods_id_all_comment, *args)
    except Exception:
        logger.error('遇到错误:', exc_info=True)
    finally:
        try:
            del loop
        except:
            pass
        collect()

        return res

async def create_goods_comment_celery_task_obj(**kwargs):
    """
    获取goods comment celery obj
    :param kwargs:
    :return:
    """
    index = kwargs['index']
    goods_id = kwargs['goods_id']
    site_id = kwargs['site_id']

    from celery_tasks import _get_someone_goods_id_all_comment_task

    async_obj = _get_someone_goods_id_all_comment_task.apply_async(
        args=[
            index,
            site_id,
            goods_id,
        ],
        expires=5 * 60,
        retry=False,
    )

    return async_obj

async def get_goods_comment_async_one_res(slice_params_list, now_loop, logger, conc_type_num=0) -> list:
    """
    获取goods comment 异步 slice_params_list的one_res
    :param slice_params_list:
    :param now_loop: 当前事件循环obj
    :param logger:
    :param conc_type: 并发类型: 0:'celery' or 1:'asyncio'
    :return:
    """
    if conc_type_num not in (0, 1):
        raise ValueError('conc_type_num值异常!')

    tasks = []
    for item in slice_params_list:
        index, goods_id, site_id = item['index'], item['goods_id'], item['site_id']
        logger.info('create task[where index: {}, goods_id: {}, site_id: {}]'.format(index, goods_id, site_id))
        if conc_type_num == 0:
            try:
                async_obj = await create_goods_comment_celery_task_obj(
                    index=index,
                    site_id=site_id,
                    goods_id=goods_id,)
                tasks.append(async_obj)
            except Exception:
                logger.error('遇到错误:', exc_info=True)
                continue

        elif conc_type_num == 1:
            tasks.append(now_loop.create_task(async_get_someone_goods_id_all_comment(
                index=index,
                site_id=site_id,
                goods_id=goods_id,
                logger=logger)))

        else:
            raise NotImplementedError

    if conc_type_num == 0:
        # celery
        one_res = await _get_celery_async_results(tasks=tasks)

    elif conc_type_num == 1:
        # asyncio
        one_res = await async_wait_tasks_finished(tasks=tasks)
    else:
        raise NotImplementedError

    return one_res

async def handle_and_save_goods_comment_info(now_goods_comment_list, logger) -> None:
    """
    处理和存储comment info
    :param now_goods_comment_list:
    :param logger:
    :return:
    """
    for item in now_goods_comment_list:
        try:
            goods_id = item.get('goods_id', '')
            assert goods_id != '', 'goods_id不为空值!'
        except AssertionError:
            continue
        except AttributeError:
            logger.error('遇到错误:', exc_info=True)
            continue

        if item.get('_comment_list', []) != []:
            logger.info('[+] crawler goods_id: {} success!'.format(goods_id))
            _save_comment_item_r(
                _r=item,
                goods_id=goods_id,
                logger=logger,)
        else:
            logger.info('[-] goods_id: {} 的comment_list为空list! 跳过!'.format(goods_id))

    return None

async def record_goods_comment_modify_time(goods_id, logger=None) -> bool:
    """
    记录goods_id的评论更新的时间点
    :param goods_id:
    :return:
    """
    res = False
    try:
        sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        res = await sql_cli._update_table_3(
            sql_str=cm_update_str_2,
            params=(str(get_shanghai_time()), str(goods_id)),
            logger=logger,)
        try:
            del sql_cli
        except:
            pass
    except Exception:
        logger.error('遇到错误:', exc_info=True)

    logger.info('[{}] record goods_id: {} comment_modify_time success!'.format(
        '+' if res else '-',
        goods_id,))
    collect()

    return res

def from_tmall_type_get_site_id(type) -> (bool, int):
    """
    根据tmall的type得到site_id的值
    :param type:
    :return:
    """
    # # 采集的来源地
    if type == 0:
        site_id = 3  # 采集来源地(天猫)
    elif type == 1:
        site_id = 4  # 采集来源地(天猫超市)
    elif type == 2:
        site_id = 6  # 采集来源地(天猫国际)
    else:
        return False

    return site_id

def to_right_and_update_tm_data(data, pipeline, logger=None) -> bool:
    """
    更新常规tm数据
    :param data:
    :param pipeline:
    :param logger:
    :return:
    """
    def _get_db_update_params(item):
        """得到tm db待更新的数据"""
        params = [
            item['modify_time'],
            item['shop_name'],
            item['account'],
            item['title'],
            item['sub_title'],
            item['link_name'],
            item['price'],
            item['taobao_price'],
            dumps(item['price_info'], ensure_ascii=False),
            dumps(item['detail_name_list'], ensure_ascii=False),
            dumps(item['price_info_list'], ensure_ascii=False),
            dumps(item['all_img_url'], ensure_ascii=False),
            dumps(item['p_info'], ensure_ascii=False),
            item['div_desc'],
            item['all_sell_count'],
            # item['delete_time'],
            item['is_delete'],
            item['is_price_change'],
            dumps(item['price_change_info'], ensure_ascii=False),
            item['sku_info_trans_time'],
            item['is_spec_change'],
            item['spec_trans_time'],
            item['is_stock_change'],
            item['stock_trans_time'],
            dumps(item['stock_change_info'], ensure_ascii=False),

            item['goods_id'],
        ]
        if item.get('delete_time', '') == '':
            params.insert(-1, item['shelf_time'])
        elif item.get('shelf_time', '') == '':
            params.insert(-1, item['delete_time'])
        else:
            params.insert(-1, item['shelf_time'])
            params.insert(-1, item['delete_time'])

        return tuple(params)

    site_id = from_tmall_type_get_site_id(type=data.get('type'))
    if site_id is False:
        _print(
            msg='获取到的site_id为False!出错!请检查!出错goods_id: {0}'.format(data.get('goods_id')),
            logger=logger,
            log_level=2)
        return False

    tmp = _get_right_model_data(
        data=data,
        site_id=site_id,
        logger=logger)
    # pprint(tmp)

    params = _get_db_update_params(item=tmp)
    base_sql_str = tm_update_str_1
    if tmp['delete_time'] == '':
        sql_str = base_sql_str.format('shelf_time=%s', '')
    elif tmp['shelf_time'] == '':
        sql_str = base_sql_str.format('delete_time=%s', '')
    else:
        sql_str = base_sql_str.format('shelf_time=%s,', 'delete_time=%s')

    res = pipeline._update_table_2(
        sql_str=sql_str,
        params=params,
        logger=logger)

    return res

def to_right_and_update_tb_data(data, pipeline, logger=None) -> bool:
    '''
    实时更新数据
    :param data:
    :param pipeline:
    :return:
    '''
    def _get_db_update_params(item) -> tuple:
        '''
        得到db待更新的数据
        :param item:
        :return:
        '''
        params = [
            item['modify_time'],
            item['shop_name'],
            item['account'],
            item['title'],
            item['sub_title'],
            item['link_name'],
            item['price'],
            item['taobao_price'],
            dumps(item['price_info'], ensure_ascii=False),
            dumps(item['detail_name_list'], ensure_ascii=False),
            dumps(item['price_info_list'], ensure_ascii=False),
            dumps(item['all_img_url'], ensure_ascii=False),
            dumps(item['p_info'], ensure_ascii=False),
            item['div_desc'],
            item['all_sell_count'],
            item['is_delete'],
            item['is_price_change'],
            dumps(item['price_change_info'], ensure_ascii=False),
            item['sku_info_trans_time'],
            item['is_spec_change'],
            item['spec_trans_time'],
            item['is_stock_change'],
            item['stock_trans_time'],
            dumps(item['stock_change_info'], ensure_ascii=False),

            item['goods_id'],
        ]
        if item.get('delete_time', '') == '':
            params.insert(-1, item['shelf_time'])
        elif item.get('shelf_time', '') == '':
            params.insert(-1, item['delete_time'])
        else:
            params.insert(-1, item['shelf_time'])
            params.insert(-1, item['delete_time'])

        return tuple(params)

    goods_id = data.get('goods_id')
    try:
        tmp = _get_right_model_data(data=data, site_id=1, logger=logger)
    except:
        logger.error('遇到错误, 先跳过处理!出错goods_id={0}'.format(goods_id), exc_info=True)
        return False

    params = _get_db_update_params(item=tmp)
    base_sql_str = tb_update_str_1
    if tmp['delete_time'] == '':
        sql_str = base_sql_str.format('shelf_time=%s', '')
    elif tmp['shelf_time'] == '':
        sql_str = base_sql_str.format('delete_time=%s', '')
    else:
        sql_str = base_sql_str.format('shelf_time=%s,', 'delete_time=%s')

    if isinstance(pipeline, SqlServerMyPageInfoSaveItemPipeline):
        res = pipeline._update_table_2(
            sql_str=sql_str,
            params=params,
            logger=logger)
    elif isinstance(pipeline, SqlPools):
        res = pipeline._update_table(
            sql_str=sql_str,
            params=params,
            logger=logger)
    else:
        raise TypeError('pipeline type: {}, 异常!'.format(type(pipeline)))

    return res