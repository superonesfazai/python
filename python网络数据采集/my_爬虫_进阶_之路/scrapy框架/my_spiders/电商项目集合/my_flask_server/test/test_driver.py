# coding:utf-8

'''
@author = super_fazai
@File    : test_driver.py
@connect : superonesfazai@gmail.com
'''

from sys import path as sys_path
sys_path.append('..')

from settings import (
    CHROME_DRIVER_PATH,
    FIREFOX_DRIVER_PATH,
    PHANTOMJS_DRIVER_PATH,
)

from fzutils.spider.fz_driver import (
    BaseDriver,
    CHROME,
    PHANTOMJS,
    FIREFOX,
)
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.selector import parse_field
from fzutils.thread_utils import *
from fzutils.shell_utils import *

def test_driver(_type=CHROME,
                headless=True,
                driver_use_proxy=True,
                url: str='https://httpbin.org/get',) -> str:
    if _type == CHROME:
        executable_path = CHROME_DRIVER_PATH
    elif _type == FIREFOX:
        executable_path = FIREFOX_DRIVER_PATH
    elif _type == PHANTOMJS:
        executable_path = PHANTOMJS_DRIVER_PATH
    else:
        raise ValueError('_type value 异常!')

    print('driver_type: {}, executable_path: {}, driver_use_proxy: {}'.format(_type, executable_path, driver_use_proxy))
    print('url: {}'.format(url))
    d = BaseDriver(
        type=_type,
        executable_path=executable_path,
        headless=headless,
        driver_use_proxy=driver_use_proxy,
        ip_pool_type=tri_ip_pool,
    )
    body = d.get_url_body(
        url=url,
        timeout=30,)
    print(body)

    try:
        del d
    except:
        pass

    return body

def test_geckodriver_change_proxy():
    """
    测试firefox动态切换代理
    :return:
    """
    d = BaseDriver(
        type=FIREFOX,
        executable_path=FIREFOX_DRIVER_PATH,
        headless=True,
        ip_pool_type=tri_ip_pool,)
    origin_ip_sel = {
        'method': 're',
        'selector': '\"origin\": \"(.*?)\",'
    }
    url = 'https://httpbin.org/get'
    body = d.get_url_body(
        url=url,
        timeout=30,)
    # print(body)
    origin_ip = parse_field(
        parser=origin_ip_sel,
        target_obj=body,)
    print('origin_ip: {}'.format(origin_ip))

    body = d.get_url_body(
        url=url,
        timeout=30, )
    # print(body)
    origin_ip = parse_field(
        parser=origin_ip_sel,
        target_obj=body, )
    print('origin_ip: {}'.format(origin_ip))

    body = d.get_url_body(
        url=url,
        timeout=30, )
    # print(body)
    origin_ip = parse_field(
        parser=origin_ip_sel,
        target_obj=body, )
    print('origin_ip: {}'.format(origin_ip))

    try:
        del d
    except:
        pass

@click_command()
@click_option('--driver_type', type=int, default=CHROME, help='chrome 0 | phantomjs 1 | firefox 2')
@click_option('--headless', type=bool, default=True, help='false or true')
@click_option('--proxy', type=bool, default=True, help='false or true')
@click_option('--url', type=str, default='https://httpbin.org/get', help='网址')
@click_option('--thread_num', type=int, default=3, help='并发数')
def init(driver_type, headless, proxy, url, thread_num):
    tasks = []
    for k  in range(0, thread_num):
        tasks.append(ThreadTaskObj(
            func_name=test_driver,
            args=[
                driver_type,
                headless,
                proxy,
                url,
            ],
        ))

    one_res = start_thread_tasks_and_get_thread_tasks_res(
        tasks=tasks,)

if __name__ == '__main__':
    # init()
    test_geckodriver_change_proxy()