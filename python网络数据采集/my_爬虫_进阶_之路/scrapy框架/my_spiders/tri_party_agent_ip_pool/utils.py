# coding:utf-8

'''
@author = super_fazai
@File    : utils.py
@connect : superonesfazai@gmail.com
'''

from termcolor import colored
from fzutils.common_utils import json_2_dict
from fzutils.internet_utils import get_random_phone_ua
from fzutils.aio_utils import unblock_request
from fzutils.spider.selector import async_parse_field

async def _get_phone_headers():
    return {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': get_random_phone_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

async def async_judge_ip_is_anonymity(ip_address='', port=0, httpbin=True, use_proxy=True, timeout=10):
    '''
    异步返回当前ip地址(用于判断ip地址是否高匿)
    :param ip_address:
    :param port:
    :param httpbin:
    :param use_proxy:
    :param timeout:
    :return:
    '''
    def _get_proxies():
        return {
            # 'http': ip_address + ':' + str(port),     # 暴露原地址
            'https': ip_address + ':' + str(port),
        }

    url = 'https://www.whatismybrowser.com/' if not httpbin else 'https://www.httpbin.org/get'
    headers = await _get_phone_headers()
    proxies = _get_proxies() if use_proxy else {}
    body = await unblock_request(
        url=url,
        headers=headers,
        use_proxy=use_proxy,
        proxies=proxies,
        timeout=timeout,
        verify=False,)
    # print(body)

    if not httpbin:
        now_ip_selector = {
            'method': 'css',
            'selector': 'div#ip-address:nth-child(2) .detected-column a:nth-child(1) ::text',
        }
        now_ip = await async_parse_field(
            parser=now_ip_selector,
            target_obj=body,
            is_first=True,)

    else:
        now_ip = json_2_dict(body).get('origin', '')

    return now_ip

async def proxy_checker_welcome_page():
    """
    欢迎页
    :param self:
    :return:
    """
    _welcome = r"""
        ____                           ________              __            
       / __ \_________  _  ____  __   / ____/ /_  ___  _____/ /_____  _____
      / /_/ / ___/ __ \| |/_/ / / /  / /   / __ \/ _ \/ ___/ //_/ _ \/ ___/
     / ____/ /  / /_/ />  </ /_/ /  / /___/ / / /  __/ /__/ ,< /  __/ /    
    /_/   /_/   \____/_/|_|\__, /   \____/_/ /_/\___/\___/_/|_|\___/_/     
                          /____/                                           
    """
    _author = r"""
                                                            By: super_fazai
    """
    print(colored(_welcome, 'green'))
    print(colored(_author, 'red'))

    return None