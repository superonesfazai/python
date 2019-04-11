# coding:utf-8

'''
@author = super_fazai
@File    : mitm_hook_tb_shop_info.py
@connect : superonesfazai@gmail.com
'''

"""
启动方式:
    mitmproxy -p 8080 -s mitm_hook_tb_shop_info.py
    或者
    mitmweb -p 8080 -s mitm_hook_tb_shop_info.py
"""

from mitmproxy import (
    flow,
    ctx,
    http,
    flowfilter,
    io,)
import random
import typing
from logging import INFO, ERROR

from fzutils.log_utils import set_logger
from fzutils.spider.async_always import *

LOG_SAVE_PATH = '/Users/afa/myFiles/my_spider_logs/mitmproxy/tb/'
logger = ctx.log
lg = set_logger(
    log_file_name=LOG_SAVE_PATH + str(get_shanghai_time())[0:10] + '.txt',
    file_log_level=INFO,)

class Writer:
    def __init__(self, path: str) -> None:
        self.f: typing.IO[bytes] = open(path, "wb")
        self.w = io.FlowWriter(self.f)

    def response(self, flow: http.HTTPFlow) -> None:
        response = flow.response
        # logger.info(str(response.text))
        # logger.info(response.headers)
        if random.choice([True, False]):
            self.w.add(flow)

    def done(self):
        self.f.close()

def response(flow):
    """
    response 拦截
    :param flow:
    :return:
    """
    response = flow.response
    request = flow.request
    # logger.info(str(response.status_code))
    # logger.info(str(response.headers))
    # logger.info(str(response.cookies))
    # logger.info(str(response.text))
    if request.host == 'alisitecdn.m.taobao.com'\
            and re.compile('\/pagedata\/shop\/impression').findall(request.path) != []:     # 锁定抓取接口
        # lg.info(str(request.host))
        # lg.info(str(request.path))
        # lg.info(str(response.text))
        ori_data = wash_ori_data(json_2_dict(
            json_str=response.text,
            default_res={}).get('module', {}))
        lg.info('[+] tb_api ! user_id: {}, shop_name: {}'.format(
            ori_data.get('globalData', {}).get('userId', ''),
            ori_data.get('globalData', {}).get('userNick', ''),))

        url = 'http://127.0.0.1:9001/tb_shop_info'
        data = dumps(ori_data)
        Requests.get_url_body(
            use_proxy=False,
            method='post',
            url=url,
            data=data,)
    else:
        return

def wash_ori_data(ori_data:dict):
    """
    清洗原始data
    :return:
    """
    try:
        ori_data.pop('moduleSpecs')
        ori_data.pop('moduleList')
    except:
        pass

    return ori_data
