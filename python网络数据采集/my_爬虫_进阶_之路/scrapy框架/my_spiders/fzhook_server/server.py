# coding:utf-8

'''
@author = super_fazai
@File    : server.py
@connect : superonesfazai@gmail.com
'''

"""
server端: 提供多种本地服务
"""

from flask import (
    Flask,
    send_file,
    request,)
from os import getcwd

from settings import (
    SERVER_PORT,
)
from spider_items import CompanyItem
from utils import (
    _save_company_item,
    _get_db_company_unique_id_list_by_site_id,)

from datetime import datetime
from pprint import pprint
from logging import INFO, ERROR
from json import dumps

try:
    from gevent.wsgi import WSGIServer      # 高并发部署
except Exception as e:
    from gevent.pywsgi import WSGIServer

from fzutils.common_utils import json_2_dict
from fzutils.time_utils import get_shanghai_time
from fzutils.spider.bloom_utils import BloomFilter
from fzutils.log_utils import set_logger
from fzutils.safe_utils import get_uuid1

app = Flask(__name__, root_path=getcwd())
# 存储tb user_id
tb_shop_id_list = []
tb_shop_info_list = []
company_id_bloom_filter = BloomFilter(capacity=500000, error_rate=.00001)
# 获取db company_id
company_id_bloom_filter = _get_db_company_unique_id_list_by_site_id(
    site_id=13,
    bloom_filter=company_id_bloom_filter,)[1]

lg = set_logger(
    logger_name=get_uuid1(),
    log_file_name='/Users/afa/myFiles/my_spider_logs/fz_server/' + str(get_shanghai_time())[0:10] + '.txt',
    console_log_level=INFO,
    file_log_level=INFO,)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '欢迎来到 fzhook_server 主页!'

@app.route('/dy', methods=['GET', 'POST'])
def dy():
    """
    获取dy 无水印视频
    :return:
    """
    return send_file('templates/douyin.php')

@app.route('/tb_shop_info', methods=['POST'])
def tb_shop_info():
    global tb_shop_info_list, tb_shop_id_list
    # lg.info(str(request.args))
    # lg.info(str(request.form))
    # post 请求
    # lg.info(str(request.get_data()))

    try:
        shop_info = json_2_dict(
            json_str=request.get_data().decode(),
            default_res={})
        # pprint(shop_info)
        # lg.info(str(shop_info))
        user_id = shop_info.get('globalData', {}).get('userId', '')
        assert user_id != '', 'user_id不为null'
        shop_name = shop_info.get('globalData', {}).get('userNick', '')
        assert shop_name != '', 'shop_name不为null'
        shop_id = shop_info.get('globalData', {}).get('shopId', '')
        assert shop_id != '', 'shop_id不为null'
        site_id = shop_info.get('globalData', {}).get('siteId', '')
        assert site_id != '', 'site_id不为null'
    except Exception:
        lg.error('遇到错误:', exc_info=True)
        return 'tb_shop_info_page!!'

    if user_id not in tb_shop_id_list:
        lg.info('新增: user_id: {}, shop_name: {}, shop_id: {}'.format(user_id, shop_name, shop_id))
        tb_shop_id_list.append(user_id)
        tb_shop_info_list.append({
            'user_id': user_id,
            'shop_name': shop_name,
            'shop_id': shop_id,
            'site_id': site_id,
        })

    tb_shop_id_list = list(set(tb_shop_id_list))

    return 'tb_shop_info_page!!'

@app.route('/tb_shop_info_handle', methods=['POST'])
def tb_shop_info_handle():
    """
    tb shop handle
    :return:
    """
    global tb_shop_info_list, company_id_bloom_filter

    server_return = 'tb_shop_info_handle!'
    try:
        all_shop_info_list = json_2_dict(
            json_str=request.get_data().decode(),
            default_res=[])
        assert all_shop_info_list != [], 'all_shop_info_list不为空list!'
        # pprint(all_shop_info_list)
        # pprint(tb_shop_info_list)
    except Exception:
        lg.error('遇到错误:', exc_info=True)
        return server_return

    # TODO 存在shop_name不一致的情况, 接口中拿的是掌柜名, 不一定等于外部shop_name, 因此匹配不到的就不存储的
    new_add_2_db_shop_name_list = []
    for item in all_shop_info_list:
        try:
            item_shop_name = item.get('shop_name', '')
            item_manager_name = item.get('manager_name', '')
            for i in tb_shop_info_list:
                i_shop_name = i.get('shop_name', '')
                unique_id = 'tb' + str(i['shop_id'])
                if unique_id in company_id_bloom_filter:
                    # lg.info('company unique_id: {} in db! pass'.format(unique_id))
                    # 已存入db的也删除! 避免list无限增大!
                    new_add_2_db_shop_name_list.append(i_shop_name)
                    continue

                # lg.info('shop_name: {}, 未被录入db中, 即将进行匹配入录 ...'.format(item_shop_name))
                if item_shop_name == i_shop_name\
                        or (item_manager_name != '' and item_manager_name == i_shop_name):
                    # 或者 掌柜名相同
                    lg.info('@@@ 匹配到shop_name: {} !!'.format(item_shop_name))
                    company_item = CompanyItem()
                    # 所在地元素无法被定位, 全部设置为北京
                    company_item['province_id'] = '110000'
                    company_item['city_id'] = '110000'
                    company_item['unique_id'] = unique_id
                    company_item['company_url'] = ''
                    company_item['company_link'] = ''
                    company_item['company_status'] = ''
                    company_item['company_name'] = item_shop_name
                    company_item['legal_person'] = ''
                    company_item['phone'] = item.get('phone_list', [])
                    company_item['email_address'] = []
                    company_item['address'] = ''
                    company_item['brief_introduction'] = ''
                    company_item['business_range'] = ''
                    company_item['founding_time'] = datetime(1900, 1, 1)
                    company_item['create_time'] = get_shanghai_time()
                    company_item['site_id'] = 13
                    company_item['employees_num'] = ''
                    company_item['type_code'] = ''
                    company_item['lng'] = 0.
                    company_item['lat'] = 0.

                    res = _save_company_item(company_item=company_item)
                    if res and unique_id not in company_id_bloom_filter:
                        company_id_bloom_filter.add(unique_id)
                        new_add_2_db_shop_name_list.append(i_shop_name)
                    else:
                        pass

                    lg.info('[{}] unique_id: {}, shop_name: {}'.format(
                        '+' if res else '-',
                        unique_id,
                        i_shop_name,))
                    break

                else:
                    continue

        except Exception:
            lg.error('遇到错误:', exc_info=True)

    new_add_2_db_shop_name_list = list(set(new_add_2_db_shop_name_list))
    # 清除已被存储的
    new_tb_shop_info_list = []
    for item in tb_shop_info_list:
        shop_name = item.get('shop_name', '')
        if shop_name not in new_add_2_db_shop_name_list:
            new_tb_shop_info_list.append(item)
    tb_shop_info_list = new_tb_shop_info_list

    return server_return

@app.route('/all_tb_shop_info', methods=['GET'])
def all_tb_shop_info():
    """
    获取所有tb_shop_info
    :return:
    """
    global tb_shop_info_list

    return dumps(tb_shop_info_list)

def main():
    lg.info('server 已启动...\nhttp://0.0.0.0:{}\n'.format(SERVER_PORT))
    WSGIServer(listener=('0.0.0.0', SERVER_PORT), application=app).serve_forever()  # 采用高并发部署

if __name__ == '__main__':
    main()
