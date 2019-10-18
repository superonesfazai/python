# coding:utf-8

'''
@author = super_fazai
@File    : goods_coupon_spider.py
@connect : superonesfazai@gmail.com
'''

from termcolor import colored
from os import system
from websockets.exceptions import ConnectionClosed as WebsocketsConnectionClosed
from asyncio.futures import InvalidStateError
from queue import Queue
from threading import Thread
from random import uniform as random_uniform

from settings import (
    IP_POOL_TYPE,
    MY_SPIDER_LOGS_PATH,
)
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from fzutils.spider.fz_driver import PHONE
from fzutils.common_utils import _print
from fzutils.spider.pyppeteer_always import *
from fzutils.spider.chrome_remote_interface import *
from fzutils.spider.async_always import *

PYPPETEER_CHROMIUM_DRIVER_PATH = '/Users/afa/myFiles/tools/pyppeteer_driver/mac/chrome-mac/Chromium.app/Contents/MacOS/Chromium'
DRIVER_LOAD_IMAGES = False

class GoodsCouponSpider(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            user_agent_type=PHONE,
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=None,
            log_save_path=MY_SPIDER_LOGS_PATH + '/coupon/_/',
            headless=True,
        )
        self.concurrency = 10
        self.concurrency2 = 6
        self.req_num_retries = 8
        self.proxy_type = PROXY_TYPE_HTTPS
        self.driver_load_images=DRIVER_LOAD_IMAGES
        self.concurrent_type = 1
        self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        self.init_sql_str()

    async def _fck_run(self):
        """
        main
        :return:
        """
        while True:
            self.db_res = await self.get_db_res()

            all_tasks_params_list_obj = await self.get_all_tasks_params_list_obj()
            tasks_params_list_obj = TasksParamsListObj(
                tasks_params_list=all_tasks_params_list_obj,
                step=self.concurrency,
                slice_start_index=0,)
            while True:
                try:
                    slice_params_list = tasks_params_list_obj.__next__()
                except AssertionError:
                    break

                coupon_url_list = await self.get_coupon_url_list_by_goods_id_list(
                    slice_params_list=slice_params_list
                )
                # pprint(coupon_url_list)

                # 测试
                # coupon_url = 'https://uland.taobao.com/coupon/edetail?e=5M3kt6O%2FfZqa2P%2BN2ppgB2X2iX5OaVULVb9%2F1Hxlj5NQYhkEFAI5hGSlkL8%2BFO6JZSEGEhAo6u3FrE8HH4fiD8KUixUTTLeu0WMS0ZKY%2BzmLVIDjuHwzlw%3D%3D&af=1&pid=mm_55371245_39912139_149806421'
                # coupon_url_list = [coupon_url for i in range(10)]

                # 划分coupon_url_list, 避免多开使内存崩溃
                tasks_params_list_obj = TasksParamsListObj(
                    tasks_params_list=coupon_url_list,
                    step=self.concurrency2,
                    slice_start_index=0,)
                while True:
                    try:
                        slice_params_list = tasks_params_list_obj.__next__()
                    except AssertionError:
                        break

                    tasks = []
                    for coupon_url in slice_params_list:
                        self.lg.info('create task[where coupon_url: {}] ...'.format(coupon_url))
                        tasks.append(self.loop.create_task(self.intercept_target_api(
                            coupon_url=coupon_url)))

                    one_res = await async_wait_tasks_finished(tasks=tasks)

                    # 成功总数
                    success_count = 0
                    for item in one_res:
                        if item:
                            success_count += 1
                    self.lg.info('成功个数: {}, 成功概率: {:.3f}'.format(success_count, success_count/self.concurrency2))

    async def get_all_tasks_params_list_obj(self) -> list:
        """
        根据db 给与的数据获取到所有的目标数据
        :return:
        """
        all_tasks_params_list_obj = []
        for item in self.db_res:
            all_tasks_params_list_obj.append({
                'goods_id': item[0],
                'site_id': item[1],
            })

        return all_tasks_params_list_obj

    async def get_coupon_url_list_by_goods_id_list(self, slice_params_list) -> list:
        """
        根据给与的goods_id_list来获取对应的coupon_url_list
        :return:
        """
        def get_create_task_msg(k) -> str:
            return 'create task[where goods_id: {}, site_id: {}] ...'.format(
                k['goods_id'],
                k['site_id'],
            )

        def get_now_args(k) -> list:
            return [
                k['goods_id'],
            ]

        all_res = await get_or_handle_target_data_by_task_params_list(
            loop=self.loop,
            tasks_params_list=slice_params_list,
            func_name_where_get_create_task_msg=get_create_task_msg,
            func_name=self.get_tm_coupon_url_from_lq5u,
            func_name_where_get_now_args=get_now_args,
            func_name_where_handle_one_res=None,
            func_name_where_add_one_res_2_all_res=default_add_one_res_2_all_res2,
            one_default_res='',
            step=self.concurrency,
            logger=self.lg,
            concurrent_type=self.concurrent_type,
            func_timeout=25,
        )

        res = []
        for item in all_res:
            if item != '':
                res.append(item)

        return res

    async def get_db_res(self) -> list:
        """
        获取目标goods_id_list
        :return:
        """
        db_res = []
        try:
            db_res = list(self.sql_cli._select_table(sql_str=self.sql_tr0,))
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)

        assert db_res != []
        self.lg.info('db_res_len: {}'.format(len(db_res)))

        return db_res

    async def intercept_target_api(self, coupon_url: str):
        """
        拦截目标接口
        :param coupon_url:
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
                url=coupon_url,
                options={
                    'timeout': 1000 * 40,  # unit: ms
                    'waitUntil': [  # 页面加载完成 or 不再有网络连接
                        'domcontentloaded',
                        'networkidle0',
                    ]
                },
                num_retries=3,
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

        except (WebsocketsConnectionClosed, InvalidStateError) as e:
            pass
        except Exception as e:
            self.lg.error('遇到错误:', exc_info=True)

        try:
            del chromium_puppeteer
            del page
        except:
            pass
        try:
            await driver.close()
        except:
            pass

        return res

    @catch_exceptions_with_class_logger(default_res='')
    def get_tm_coupon_url_from_lq5u(self,
                                    goods_id='',
                                    goods_name_or_m_url: str = '',) -> str:
        """
        从领券无忧根据goods_id搜索tm优惠券, 并返回领券地址
            url: http://www.lq5u.com
        :param goods_id: 推荐使用商品id来查券
        :param goods_name_or_m_url: 商品名 or 商品地址
        :param proxy_type:
        :param num_retries:
        :return: 优惠券领取地址
        """
        # todo 测试发现无需搜索, 只需把goods_id 改为领券无忧的对应的url即可查询是否有券
        # 基于领券无忧来根据商品名获取其优惠券
        # headers = get_random_headers(
        #     user_agent_type=1,
        #     connection_status_keep_alive=False,
        # )
        # headers.update({
        #     'Proxy-Connection': 'keep-alive',
        #     'Origin': 'http://www.lq5u.com',
        #     'Content-Type': 'application/x-www-form-urlencoded',
        #     'Referer': 'http://www.lq5u.com/',
        # })
        # # 只搜索天猫的
        # data = {
        #   'p': '1',
        #   'cid': '0',
        #   'sort': '0',
        #   'b2c': '1',           # '0'为搜索tb, tm | '1'为只搜索tm
        #   'coupon': '1',
        #   'k': goods_name_or_m_url,
        # }
        # body = Requests.get_url_body(
        #     method='post',
        #     url='http://www.lq5u.com/',
        #     headers=headers,
        #     # cookies=cookies,
        #     data=data,
        #     verify=False,
        #     ip_pool_type=IP_POOL_TYPE,
        #     num_retries=num_retries,
        #     proxy_type=proxy_type,)
        # assert body != ''
        # # print(body)
        #
        # lq5u_url_list_sel = {
        #     'method': 'css',
        #     'selector': 'li a ::attr("onmousedown")',
        # }
        # ori_lq5u_url_list = parse_field(
        #     parser=lq5u_url_list_sel,
        #     target_obj=body,
        #     is_first=False,)
        # lq5u_url_list = []
        # for item in ori_lq5u_url_list:
        #     try:
        #         url = re.compile('this.href=\'(.*?)\'').findall(item)[0]
        #         assert url != ''
        #     except Exception:
        #         continue
        #
        #     lq5u_url_list.append('http://www.lq5u.com' + url)
        #
        # assert lq5u_url_list != []
        # pprint(lq5u_url_list)

        # 领券无忧对应页面如下
        # url = 'http://www.lq5u.com/item/index/iid/{}.html'.format(goods_id)
        # body = Requests.get_url_body(
        #     method='get',
        #     url=url,
        #     headers=headers,
        #     verify=False,
        #     ip_pool_type=IP_POOL_TYPE,
        #     num_retries=num_retries,
        #     proxy_type=proxy_type, )
        # assert body != ''
        # print(body)
        #
        # coupon_info_sel = {
        #     'method': 'css',
        #     'selector': 'span.b.red ::text',
        # }
        # coupon_info = parse_field(
        #     parser=coupon_info_sel,
        #     target_obj=body,
        # )
        # if '很遗憾，该商品没有优惠券' in coupon_info:
        #     return []
        # else:
        #     _print(msg='goods_id: {}, 存在优惠券'.format(goods_id), logger=logger)
        #     return []

        # 查看某商品是否含有优惠券
        # 地址: http://www.i075.com/item/index/iid/562016826663.html

        # 可以从下面网站拿商品测试
        # http://www.i075.com/index/cate/cid/1.html
        # tm
        # goods_id = '562016826663'
        # goods_id = '565122084412'
        # tb
        # goods_id = '573406377569'

        # 根据领券无忧接口
        headers = get_random_headers(
            user_agent_type=1,
            connection_status_keep_alive=False,
        )
        headers.update({
            'Origin': 'http://www.lq5u.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://www.lq5u.com/item/index/iid/{}.html'.format(goods_id),
            'X-Requested-With': 'XMLHttpRequest',
        })
        params = (
            ('rnd', str(random_uniform(0, 1))),  # eg: '0.4925945510743117'
        )
        data = {
            'iid': goods_id
        }
        body = Requests.get_url_body(
            method='post',
            url='http://www.lq5u.com/item/ajax_get_auction_code.html',
            headers=headers,
            params=params,
            data=data,
            verify=False,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.req_num_retries,
            proxy_type=self.proxy_type, )
        assert body != ''
        # self.lg.info(body)

        data = json_2_dict(
            json_str=body,
            default_res={},
            logger=self.lg,).get('data', {})
        # pprint(data)
        # 处理data = ''
        data = data if not isinstance(data, str) else {}

        coupon_url = data.get('coupon_click_url', '')
        if coupon_url != '':
            self.lg.info('该goods_id: {} 含 有优惠券, coupon领取地址: {}'.format(goods_id, coupon_url))
        else:
            self.lg.info('该goods_id: {} 不含 有优惠券'.format(goods_id))
            if '531388515851' == goods_id:
                return 'test'

        return coupon_url

    def init_sql_str(self):
        # SiteID=1 or
        self.sql_tr0 = '''
        select GoodsID, SiteID
        from dbo.GoodsInfoAutoGet
        where MainGoodsID is not null
        and IsDelete=0
        and (SiteID=3 or SiteID=4 or SiteID=6)
        -- and MainGoodsID=143509
        '''

    def __del__(self):
        try:
            del self.concurrency
            del self.loop
        except:
            pass
        collect()

class NetworkInterceptorTest(NetworkInterceptor):
    def __init__(self, logger=None):
        NetworkInterceptor.__init__(
            self,
            load_images=False,
            logger=logger,)
        self.target_url = 'h5api.m.taobao.com/h5/mtop.alimama.union.xt.biz.quan.api.entry'

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
        global coupon_queue

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
                    msg = '[{:8s}] {}'.format(colored('@-data-@', 'green'), intercept_body)
                    _print(msg=msg, logger=self.lg)
                    coupon_queue.put(intercept_body)
                except (PyppeteerNetworkError, IndexError, Exception) as e:
                    _print(msg='遇到错误:', logger=self.lg, log_level=2, exception=e)
            else:
                pass

        else:
            pass

class TargetDataConsumer(Thread):
    """
    目标数据消费者
    """
    def __init__(self, args: (list, tuple)=()):
        super(TargetDataConsumer, self).__init__()
        self.args = args

    def run(self):
        global coupon_queue

        while True:
            try:
                if coupon_queue.qsize() >= 1:
                    coupon_item = coupon_queue.get()
                    ori_coupon_list = json_2_dict(
                        json_str=re.compile('\((.*)\)').findall(coupon_item)[0],
                        default_res={},).get('data', {}).get('resultList', [])
                    assert ori_coupon_list != []
                    # pprint(ori_coupon_list

                    coupon_list = []
                    for item in ori_coupon_list:
                        try:
                            # 一个账户优惠券只能使用一次
                            # 优惠券展示名称, eg: '优惠券'
                            coupon_display_name = '优惠券'
                            # 优惠券的值, 即优惠几元
                            ori_coupon_value = item.get('couponAmount', '')
                            assert ori_coupon_value != ''
                            coupon_value = str(float(ori_coupon_value).__round__(2))
                            use_method = ''
                            # 使用门槛
                            ori_thresold = item.get('couponStartFee', '')
                            assert ori_thresold != ''
                            threshold = str(float(ori_thresold).__round__(2))
                            begin_time = str(timestamp_to_regulartime(int(item.get('couponEffectiveStartTime', '')[0:10])))
                            end_time = str(timestamp_to_regulartime(int(item.get('couponEffectiveEndTime', '')[0:10])))

                            if string_to_datetime(end_time) <= get_shanghai_time():
                                # 已过期的
                                continue

                            coupon_list.append({
                                'coupon_display_name': coupon_display_name,
                                'coupon_value': coupon_value,
                                'use_method': use_method,
                                'threshold': threshold,
                                'begin_time': begin_time,
                                'end_time': end_time,
                            })

                        except Exception:
                            # print(e)
                            continue

                    pprint(coupon_list)
                else:
                    continue
            except IndexError:
                # 跳过相同接口得索引异常
                continue
            except Exception as e:
                print(e)

if __name__ == '__main__':
    # 消费券队列
    coupon_queue = Queue()
    tasks = []
    # 存储所有需要监控并重启的初始化线程对象list
    need_to_be_monitored_thread_tasks_info_list = []
    for i in range(1):
        func_args = ()
        task = TargetDataConsumer()
        thread_name = 'thread_task:{}:{}'.format(
            'TargetDataConsumer',
            get_uuid1(), )
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

    goods_coupon_spider = GoodsCouponSpider()
    loop = get_event_loop()
    loop.run_until_complete(goods_coupon_spider._fck_run())