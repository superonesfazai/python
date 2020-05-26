# coding:utf-8

'''
@author = super_fazai
@File    : goods_sort_by_shop_type_spider.py
@connect : superonesfazai@gmail.com
'''

"""
商品根据店铺类型分类的爬虫
"""

from platform import platform
from termcolor import colored
from websockets.exceptions import ConnectionClosed as WebsocketsConnectionClosed
from asyncio.futures import InvalidStateError
from queue import Queue
from threading import Thread
from random import uniform as random_uniform
from decimal import Decimal
from asyncio import TimeoutError as AsyncTimeoutError
from asyncio import wait_for
from os import system

from settings import (
    IP_POOL_TYPE,
    MY_SPIDER_LOGS_PATH,
)
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from my_exceptions import SqlServerConnectionException
from multiplex_code import (
    CP_PROFIT,
    get_new_sku_info_from_old_sku_info_subtract_coupon_and_add_cp_profit,
)

from fzutils.spider.fz_driver import PHONE
from fzutils.common_utils import _print
from fzutils.spider.selector import parse_field
from fzutils.memory_utils import get_current_func_info_by_traceback
from fzutils.spider.pyppeteer_always import *
from fzutils.spider.chrome_remote_interface import *
from fzutils.spider.async_always import *

DRIVER_LOAD_IMAGES = False
if 'armv7l-with-debian' in platform():
    PYPPETEER_CHROMIUM_DRIVER_PATH = '/usr/bin/chromium-browser'
else:
    PYPPETEER_CHROMIUM_DRIVER_PATH = '/Users/afa/myFiles/tools/pyppeteer_driver/mac/chrome-mac/Chromium.app/Contents/MacOS/Chromium'

class GoodsSortByShopTypeSpider(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            user_agent_type=PHONE,
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=None,
            log_save_path=MY_SPIDER_LOGS_PATH + '/goods_sort_by_shop_type/_/',
            headless=True,
        )
        # 不宜过大, 官网会发现
        self.concurrency = 10
        # 不可太大 电脑卡死
        self.concurrency2 = 3
        self.req_num_retries = 7
        self.proxy_type = PROXY_TYPE_HTTPS
        self.driver_load_images = DRIVER_LOAD_IMAGES
        # 用线程模式长期运行报: too many open files
        self.concurrent_type = 0
        self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        self.init_sql_str()

    def init_sql_str(self):
        pass

    async def _fck_run(self):
        # 休闲零食
        target_url = 'https://pages.tmall.com/wow/chaoshi/act/chaoshi-category?spm=a3204.12691414.201609072.d78&wh_biz=tm&wh_showError=true&iconType=categoryxiuxianlingshi&name=%E4%BC%91%E9%97%B2%E9%9B%B6%E9%A3%9F&cateId=78&version=newIcon&storeId=&disableNav=YES'
        await self.intercept_target_api(target_url=target_url)

    async def intercept_target_api(self, target_url: str):
        """
        拦截目标接口
        :param target_url:
        :return:
        """
        chromium_puppeteer = ChromiumPuppeteer(
            load_images=self.driver_load_images,
            executable_path=PYPPETEER_CHROMIUM_DRIVER_PATH,
            ip_pool_type=self.ip_pool_type,
            headless=self.headless,
            user_agent_type=self.user_agent_type,)
        driver = await chromium_puppeteer.create_chromium_puppeteer_browser()
        # self.lg.info('chromium version: {}'.format(await driver.version()))
        # self.lg.info('初始user_agent: {}'.format(await driver.userAgent()))
        page = await driver.newPage()
        await bypass_chrome_spiders_detection(page=page)

        # ** 截获 request 和 response, 劫持请求跟应答必须都设置!
        # ** puppeteer官网事件api: https://github.com/GoogleChrome/puppeteer/blob/master/docs/api.md
        # 搜索class: Page, 找到需求事件进行重写
        await page.setRequestInterception(True)
        network_interceptor = NetworkInterceptorTest()
        page.on(event='request', f=network_interceptor.intercept_request)
        page.on(event='response', f=network_interceptor.intercept_response)
        page.on(event='requestfailed', f=network_interceptor.request_failed)
        # page.on(event='requestfinished', f=network_interceptor.request_finished)

        res = False
        try:
            await goto_plus(
                page=page,
                url=target_url,
                options={
                    'timeout': 1000 * 45,  # unit: ms
                    'waitUntil': [  # 页面加载完成 or 不再有网络连接
                        'domcontentloaded',
                        'networkidle0',
                    ]
                },
                num_retries=2,
            )

            # 全屏截图
            # await page.screenshot({
            #     'path': 'screen.png',
            #     'type': 'png',
            #     'fullPage': True,
            # })
            # 目标元素定位截图
            # target_ele = await page.querySelector(selector='div.board')
            # await target_ele.screenshot({
            #     'path': 'target_ele.png',
            #     'type': 'png',
            # })

            # 如果网页内有用iframe等标签，这时page对象是无法读取<iframe>里面的内容的，需要用到下面
            # frames_list = page.frames
            # pprint(frames_list)

            body = Requests._wash_html(await page.content())
            # print('[{:8s}] {}'.format(
            #     colored('body', 'red'),
            #     body, ))
            res = True if body != '' else res

        except (WebsocketsConnectionClosed, InvalidStateError):
            pass
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)

        try:
            await driver.close()
        except:
            try:
                await driver.close()
            except:
                pass
        try:
            del page
        except:
            try:
                del page
            except:
                pass
        try:
            del chromium_puppeteer
        except:
            try:
                del chromium_puppeteer
            except:
                pass
        collect()

        return res

class NetworkInterceptorTest(NetworkInterceptor):
    def __init__(self, logger=None):
        NetworkInterceptor.__init__(
            self,
            load_images=False,
            logger=logger,)
        # 分类数据接口
        self.target_url = 'mtop.chaoshi.aselfshoppingguide.category.level1/1.0/'
        # 子分类的接口
        # mtop.chaoshi.aselfshoppingguide.category.level2/1.0/

    async def intercept_request(self, request: PyppeteerRequest):
        """
        截获request(do something you like ...)
        :param request:
        :return:
        """
        url = request.url
        headers = request.headers
        post_data = request.postData
        request_resource_type = request.resourceType

        msg='[{:8s}] url: {}, post_data: {}'.format('request', url, post_data,)
        if self.target_url in url:
            _print(msg=msg, logger=self.lg, log_level=1)
        else:
            pass

        if not self.load_images and request_resource_type in ['image', 'media']:
            await request.abort()
        else:
            # 放行请求
            await request.continue_()

    async def intercept_response(self, response: PyppeteerResponse):
        """
        截获response(do something you like ...)
        :param response:
        :return:
        """
        global cate_level_queue

        response_status = response.status
        request = response.request
        request_url = request.url
        request_headers = request.headers
        request_method = request.method
        request_resource_type = request.resourceType
        post_data = request.postData

        msg = '[{:8s}] request_resource_type: {:10s}, request_method: {:6s}, response_status: {:5s}, request_url: {}'.format(
            'response',
            request_resource_type,
            request_method,
            str(response_status),
            request_url, )
        if self.target_url in request_url:
            _print(msg=msg, logger=self.lg, log_level=1)
        else:
            pass

        if request_resource_type in ['xhr', 'fetch', 'document', 'script', 'websocket', 'eventsource', 'other']:
            if self.target_url in request_url:
                try:
                    body = await response.text()
                    intercept_body = body.replace('\n', '').replace('\t', '').replace('  ', '')
                    msg = '[{:8s}] {}'.format(colored('@-data-@', 'green'), intercept_body[0:1000])
                    _print(msg=msg, logger=self.lg)
                    cate_level_queue.put(intercept_body)
                except (PyppeteerNetworkError, IndexError, Exception) as e:
                    _print(msg='遇到错误:', logger=self.lg, log_level=2, exception=e)
            else:
                pass

        else:
            pass

class TargetDataConsumer(Thread):
    def __init__(self, args: (list, tuple)=()):
        super(TargetDataConsumer, self).__init__()
        self.args = args

    def run(self):
        global cate_level_queue

        while True:
            try:
                if cate_level_queue.qsize() >= 1:
                    cate_level_item = cate_level_queue.get()
                    ori_cate_level_data = json_2_dict(
                        json_str=re.compile('\((.*)\)').findall(cate_level_item)[0],
                        default_res={},).get('data', {})
                    assert ori_cate_level_data != {}
                    pprint(ori_cate_level_data)

            except Exception as e:
                print(e)
            finally:
                pass

if __name__ == '__main__':
    # 分类接口得队列
    cate_level_queue = Queue()

    tasks = []
    # 存储所有需要监控并重启的初始化线程对象list
    need_to_be_monitored_thread_tasks_info_list = []
    for i in range(1):
        func_args = ()
        task = TargetDataConsumer()
        thread_name = 'thread_task:{}:{}'.format(
            'TargetDataConsumer',
            get_uuid1(),)
        task.setName(name=thread_name)
        tasks.append(task)
        need_to_be_monitored_thread_tasks_info_list.append({
            'func_name': TargetDataConsumer,
            'thread_name': thread_name,
            'func_args': func_args,
            'is_class': True,
        })

    for task in tasks:
        task.start()

    # 用来检测是否有线程down并重启down线程
    check_thread_task = Thread(
        target=check_thread_tasks_and_restart,
        args=(
            need_to_be_monitored_thread_tasks_info_list,
            30,
            None,
        ))
    check_thread_task.setName('thread_task:check_thread_task_and_restart')
    check_thread_task.start()

    goods_sort_by_shop_type_spider = GoodsSortByShopTypeSpider()
    loop = get_event_loop()
    loop.run_until_complete(goods_sort_by_shop_type_spider._fck_run())