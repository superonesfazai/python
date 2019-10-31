# coding:utf-8

'''
@author = super_fazai
@File    : goods_coupon_spider.py
@connect : superonesfazai@gmail.com
'''

from termcolor import colored
from websockets.exceptions import ConnectionClosed as WebsocketsConnectionClosed
from asyncio.futures import InvalidStateError
from queue import Queue
from threading import Thread
from random import uniform as random_uniform
from decimal import Decimal
from asyncio import TimeoutError as AsyncTimeoutError
from asyncio import wait_for

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
        # 不宜过大, 官网会发现
        self.concurrency = 15
        self.concurrency2 = 6
        self.req_num_retries = 8
        self.proxy_type = PROXY_TYPE_HTTPS
        self.driver_load_images = DRIVER_LOAD_IMAGES
        self.concurrent_type = 1
        self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        self.init_sql_str()

    async def _fck_run(self):
        """
        main
        :return:
        """
        while True:
            try:
                if get_shanghai_time().hour == 0:
                    await async_sleep(60 * 60 * 3.5)
                    continue

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
                    # coupon_url_list = [coupon_url for i in range(6)]
                    # # goods_id得对应上面的领券地址
                    # goods_id_and_coupon_url_queue.put({
                    #     'goods_id': '562016826663',
                    #     'coupon_url': coupon_url,
                    # })

                    if coupon_url_list == []:
                        self.lg.info('coupon_url_list为空list, 跳过!')
                        random_sleep_time = random_uniform(2.5, 5)
                        self.lg.info('休眠{}s ...'.format(random_sleep_time))
                        await async_sleep(random_sleep_time)
                        continue

                    # 划分coupon_url_list, 避免多开使内存崩溃
                    tasks_params_list_obj2 = TasksParamsListObj(
                        tasks_params_list=coupon_url_list,
                        step=self.concurrency2,
                        slice_start_index=0,)
                    while True:
                        try:
                            slice_params_list2 = tasks_params_list_obj2.__next__()
                        except AssertionError:
                            break

                        tasks = []
                        for coupon_url in slice_params_list2:
                            self.lg.info('create task[where coupon_url: {}] ...'.format(coupon_url))
                            tasks.append(self.loop.create_task(self.intercept_target_api(
                                coupon_url=coupon_url)))

                        try:
                            one_res = await wait_for(
                                fut=async_wait_tasks_finished(tasks=tasks),
                                timeout=60 * 2,)
                        except AsyncTimeoutError:
                            self.lg.error('遇到错误:', exc_info=True)
                            continue

                        # 成功总数
                        success_count = 0
                        for item in one_res:
                            if item:
                                success_count += 1
                        self.lg.info('成功个数: {}, 成功概率: {:.3f}'.format(success_count, success_count/self.concurrency2))
                        collect()

                    collect()

                self.lg.info('一次大循环结束!!')

            except Exception:
                self.lg.error('遇到错误:', exc_info=True)
                await async_sleep(30)

            finally:
                collect()

    async def get_all_tasks_params_list_obj(self) -> list:
        """
        根据db 给与的数据获取到所有的目标数据
        :return:
        """
        global unique_coupon_id_list

        all_tasks_params_list_obj = []
        for item in self.db_res:
            goods_id = item[0]
            # 因为现在只取单件购买优惠券, 不处理多件的, 所以此处可去除已存在的
            coupon_unique_id = str(get_uuid3(target_str=goods_id))
            if coupon_unique_id in unique_coupon_id_list:
                self.lg.info('coupon_info 表中已存在coupon_unique_id: {}, goods_id: {}, pass'.format(
                    coupon_unique_id,
                    goods_id,))
                continue

            all_tasks_params_list_obj.append({
                'goods_id': goods_id,
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

        collect()

        return res

    async def get_db_res(self) -> list:
        """
        获取目标goods_id_list
        :return:
        """
        get_current_func_info_by_traceback(self=self, logger=self.lg)
        db_res = []
        try:
            # 清除过期优惠券
            self.sql_cli._delete_table(
                sql_str='delete from dbo.coupon_info where GETDATE()-end_time >= 3',
                params=None,)
            await async_sleep(15)
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
            del chromium_puppeteer
            del page
        except:
            try:
                del chromium_puppeteer
                del page
            except:
                pass
        try:
            await driver.close()
        except:
            try:
                await driver.close()
            except:
                pass
        collect()

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
        global goods_id_and_coupon_url_queue

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

        # # 根据领券无忧接口
        # # base_url = 'www.i075.com'
        # base_url = 'quan.mmfad.com'
        # headers = get_random_headers(
        #     user_agent_type=1,
        #     connection_status_keep_alive=False,
        #     upgrade_insecure_requests=False,
        #     cache_control='',)
        # headers.update({
        #     'accept': 'application/json, text/javascript, */*; q=0.01',
        #     'Referer': 'http://{}/item/index/iid/{}.html'.format(base_url, goods_id),
        #     'Origin': 'http://{}'.format(base_url),
        #     'X-Requested-With': 'XMLHttpRequest',
        #     'Content-Type': 'application/x-www-form-urlencoded',
        #     'Proxy-Connection': 'keep-alive',
        # })
        # params = (
        #     ('rnd', str(random_uniform(0, 1))),  # eg: '0.4925945510743117'
        # )
        # data = {
        #     'iid': goods_id,
        # }
        # body = Requests.get_url_body(
        #     method='post',
        #     url='http://{}/item/ajax_get_auction_code.html'.format(base_url),
        #     headers=headers,
        #     params=params,
        #     data=data,
        #     verify=False,
        #     ip_pool_type=self.ip_pool_type,
        #     num_retries=self.req_num_retries,
        #     proxy_type=self.proxy_type, )
        # assert body != ''
        # # self.lg.info(body)
        #
        # data = json_2_dict(
        #     json_str=body,
        #     default_res={},
        #     logger=self.lg,).get('data', {})
        # # pprint(data)
        # # 处理data = ''
        # data = data if not isinstance(data, str) else {}
        # coupon_url = data.get('coupon_click_url', '')

        # 通过全优惠网(https://www.quanyoubuy.com)
        headers = get_random_headers(
            connection_status_keep_alive=False,
        )
        headers.update({
            'authority': 'www.quanyoubuy.com',
            'upgrade-insecure-requests': '1',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-site': 'same-origin',
        })
        url = 'https://www.quanyoubuy.com/item/index/iid/{}.html'.format(goods_id)
        body = Requests.get_url_body(
            url=url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            proxy_type=self.proxy_type,
            num_retries=self.req_num_retries,)
        assert body != ''
        # self.lg.info(body)

        qrcode_url_sel = {
            'method': 'css',
            'selector': 'img.getGoodsLink ::attr("src")',
        }
        qrcode_url = parse_field(
            parser=qrcode_url_sel,
            target_obj=body,
            logger=self.lg,)
        assert qrcode_url != ''
        # self.lg.info(qrcode_url)
        coupon_url_sel = {
            'method': 're',
            'selector': '&text=(.*)',
        }
        coupon_url = parse_field(
            parser=coupon_url_sel,
            target_obj=qrcode_url,
            logger=self.lg,)
        # self.lg.info(coupon_url)
        if 'uland.taobao.com' not in coupon_url:
            # 地址含有上诉的才为领券地址
            coupon_url = ''
        else:
            pass

        if coupon_url != '':
            self.lg.info('[+] 该goods_id: {} 含 有优惠券, coupon领取地址: {}'.format(goods_id, coupon_url))
            # 队列录值
            goods_id_and_coupon_url_queue.put({
                'goods_id': goods_id,
                'coupon_url': coupon_url,
            })
        else:
            self.lg.info('[-] 该goods_id: {} 不含 有优惠券'.format(goods_id))

        return coupon_url

    def init_sql_str(self):
        self.sql_tr0 = '''
        select GoodsID, SiteID
        from dbo.GoodsInfoAutoGet
        where MainGoodsID is not null
        and IsDelete=0
        and (SiteID=1 or SiteID=3 or SiteID=4 or SiteID=6)
        -- and MainGoodsID=143509
        -- and GoodsID='18773718545'
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
                    msg = '[{:8s}] {}'.format(colored('@-data-@', 'green'), intercept_body[0:1000])
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
        global coupon_queue, goods_id_and_coupon_url_list, unique_coupon_id_list

        while True:
            try:
                if coupon_queue.qsize() >= 1:
                    # todo 有些领券url 为预付定金商品, 此处不处理
                    coupon_item = coupon_queue.get()
                    ori_coupon_list = json_2_dict(
                        json_str=re.compile('\((.*)\)').findall(coupon_item)[0],
                        default_res={},).get('data', {}).get('resultList', [])
                    assert ori_coupon_list != []
                    # pprint(ori_coupon_list)

                    # todo: 测试发现, 返回数据中, 若有多买几件的优惠券在字段'nCouponInfoMap'中
                    # 现只支持1件, 不支持多件的券
                    coupon_list = []
                    for item in ori_coupon_list:
                        try:
                            goods_id = str(item.get('itemId', ''))
                            assert goods_id != ''
                            # 一个账户优惠券只能使用一次
                            # 优惠券展示名称, eg: '优惠券'
                            coupon_display_name = '优惠券'
                            # 优惠券的值, 即优惠几元
                            ori_coupon_value = item.get('couponAmount', '')
                            assert ori_coupon_value != ''
                            coupon_value = str(float(ori_coupon_value).__round__(2))
                            # 使用门槛
                            ori_thresold = item.get('couponStartFee', '')
                            assert ori_thresold != ''
                            threshold = str(float(ori_thresold).__round__(2))
                            begin_time = str(timestamp_to_regulartime(int(item.get('couponEffectiveStartTime', '')[0:10])))
                            end_time = str(timestamp_to_regulartime(int(item.get('couponEffectiveEndTime', '')[0:10])))
                            # 使用方法
                            use_method = '满{}元, 减{}元'.format(threshold, coupon_value)

                            if string_to_datetime(end_time) <= get_shanghai_time():
                                print('该券已过期[goods_id: {}]'.format(goods_id))
                                # 已过期的
                                continue

                            # todo 测试发现, 同一商品可能存在不同活动时间段的同一优惠券(但是活动时间不同), 导致一个商品有多个优惠券
                            #  所以取值时, 按结束时间最大那个来取值
                            # 上面还是会有问题, 导致价格重复减, 所以生成唯一id, 所以在一次转换价格后要把所有的该goods_id券都标记为1
                            # 生成唯一id
                            # unique_id = str(get_uuid3(
                            #     target_str=goods_id \
                            #                + coupon_value \
                            #                + threshold \
                            #                + str(datetime_to_timestamp(string_to_datetime(begin_time)))[0:10]\
                            #                + str(datetime_to_timestamp(string_to_datetime(end_time)))[0:10]))

                            # todo 根据上诉存在多张券导致价格被多次修改的情况，故表中一个goods_id，只允许存一张券, 就不会出现价格被多次修改的情况
                            # 解释就说: 只存储优惠力度最大的券
                            unique_id = str(get_uuid3(target_str=goods_id))

                            # 领券地址
                            # pprint(goods_id_and_coupon_url_list)
                            coupon_url = ''
                            for j in goods_id_and_coupon_url_list:
                                tmp_goods_id = j['goods_id']
                                tmp_coupon_url = j['coupon_url']
                                if goods_id == tmp_goods_id:
                                    print('@@@ 成功匹配到goods_id: {} 的领券地址: {}!!'.format(goods_id, tmp_coupon_url))
                                    coupon_url = tmp_coupon_url
                                    break
                                else:
                                    continue
                            assert coupon_url != ''

                            coupon_list.append({
                                'unique_id': unique_id,
                                'goods_id': goods_id,
                                'coupon_url': coupon_url,
                                'coupon_display_name': coupon_display_name,
                                'coupon_value': coupon_value,
                                'threshold': threshold,
                                'begin_time': begin_time,
                                'end_time': end_time,
                                'use_method': use_method,
                            })

                        except Exception as e:
                            print(e)
                            continue

                    # pprint(coupon_list)
                    if coupon_list != []:
                        # 存储
                        sql_cli = SqlServerMyPageInfoSaveItemPipeline()
                        if not sql_cli.is_connect_success:
                            raise SqlServerConnectionException

                        for item in coupon_list:
                            unique_id = item['unique_id']
                            goods_id = item['goods_id']
                            if unique_id not in unique_coupon_id_list:
                                save_res = sql_cli._insert_into_table(
                                    sql_str='insert into dbo.coupon_info(unique_id, create_time, goods_id, coupon_url, coupon_display_name, coupon_value, threshold, begin_time, end_time, use_method) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                    params=(
                                        unique_id,
                                        str(get_shanghai_time()),
                                        goods_id,
                                        item['coupon_url'],
                                        item['coupon_display_name'],
                                        Decimal(item['coupon_value']).__round__(2),
                                        Decimal(item['threshold']).__round__(2),
                                        item['begin_time'],
                                        item['end_time'],
                                        item['use_method'],
                                    ),
                                    repeat_insert_default_res=False,    # 避免重复改价
                                )
                                if save_res:
                                    # todo 只更新一次价格, 避免重复更新导致价格错误
                                    # 去重
                                    unique_coupon_id_list.append(unique_id)
                                    # 更新常规表中的商品价格变动
                                    sql_str = '''
                                    select top 1 Price, TaoBaoPrice, SKUInfo
                                    from dbo.GoodsInfoAutoGet
                                    where GoodsID=%s
                                    '''
                                    db_res = []
                                    try:
                                        db_res = list(sql_cli._select_table(
                                            sql_str=sql_str,
                                            params=(
                                                goods_id,
                                            ),
                                        ))
                                    except Exception as e:
                                        print(e)

                                    if db_res != []:
                                        # 标记常规商品由于优惠券带来的价格变动
                                        try:
                                            # 减去优惠券的价格
                                            coupon_value = float(item['coupon_value'])
                                            threshold = float(item['threshold'])
                                            # 还原为原始价格
                                            db_price = float(db_res[0][0]) * (1 - CP_PROFIT)
                                            db_taobao_price = float(db_res[0][1]) * (1 - CP_PROFIT)
                                            # 减去优惠券价, 并且加上CP_PROFIT, 得到最终待存储价格
                                            new_price = ((db_price - coupon_value if db_price >= threshold else db_price) * (1 + CP_PROFIT)).__round__(2)
                                            new_taobao_price = ((db_taobao_price - coupon_value if db_taobao_price >= threshold else db_taobao_price) * (1 + CP_PROFIT)).__round__(2)

                                            new_sku_info = get_new_sku_info_from_old_sku_info_subtract_coupon_and_add_cp_profit(
                                                old_sku_info=json_2_dict(
                                                    json_str=db_res[0][2],
                                                    default_res=[],),
                                                threshold=threshold,
                                                coupon_value=coupon_value,)

                                            sql_str2 = '''
                                            update dbo.GoodsInfoAutoGet
                                            set Price=%s, TaoBaoPrice=%s, SKUInfo=%s, ModfiyTime=%s, sku_info_trans_time=%s, IsPriceChange=1, PriceChangeInfo=SKUInfo
                                            where GoodsID=%s 
                                            '''
                                            now_time = get_shanghai_time()
                                            sql_cli._update_table(
                                                sql_str=sql_str2,
                                                params=(
                                                    Decimal(new_price).__round__(2),
                                                    Decimal(new_taobao_price).__round__(2),
                                                    dumps(new_sku_info, ensure_ascii=False),
                                                    now_time,
                                                    now_time,
                                                    goods_id,
                                                ),
                                            )
                                        except Exception as e:
                                            print(e)
                                    else:
                                        pass
                                else:
                                    continue

                            else:
                                continue

                else:
                    continue

            except IndexError:
                # 跳过相同接口得索引异常
                continue
            except Exception as e:
                print(e)

class GoodsIdAndCouponUrlQueueConsumer(Thread):
    """
    更新goods_id_and_coupon_url_list中的item
    """
    def __init__(self, args: (list, tuple)=()):
        super(GoodsIdAndCouponUrlQueueConsumer, self).__init__()
        self.args = args

    def run(self):
        global goods_id_and_coupon_url_queue, goods_id_and_coupon_url_list

        while True:
            try:
                if goods_id_and_coupon_url_queue.qsize() >= 1:
                    goods_id_and_coupon_url_item = goods_id_and_coupon_url_queue.get()
                    # print(str(goods_id_and_coupon_url_item))
                    new_goods_id = goods_id_and_coupon_url_item['goods_id']
                    new_coupon_url = goods_id_and_coupon_url_item['coupon_url']
                    # print('@@@ 正在处理goods_id_and_coupon_url_queue中新item[where goods_id: {}, coupon_url: {}]'.format(new_goods_id, new_coupon_url))
                    # goods_id是否已被更新为最新的coupon_url
                    is_lasted = False

                    new_goods_id_and_coupon_url_list = []
                    for item in goods_id_and_coupon_url_list:
                        goods_id = item['goods_id']
                        coupon_url = item['coupon_url']
                        if goods_id == new_goods_id:
                            if coupon_url != new_coupon_url:
                                coupon_url = new_coupon_url
                            else:
                                pass

                            is_lasted = True
                            new_goods_id_and_coupon_url_list.append({
                                'goods_id': goods_id,
                                'coupon_url': coupon_url,
                            })

                        else:
                            # 不等的goods_id 保存原值
                            new_goods_id_and_coupon_url_list.append(item)

                    if is_lasted:
                        # 原先goods_id_and_coupon_url_list存在该coupon_url, 进行更新对应goods_id的coupon_url
                        goods_id_and_coupon_url_list = new_goods_id_and_coupon_url_list
                    else:
                        # 全局变量goods_id_and_coupon_url_list未被录入该goods_id
                        goods_id_and_coupon_url_list.append(goods_id_and_coupon_url_item)

                    try:
                        del new_goods_id_and_coupon_url_list
                    except:
                        pass

            except Exception as e:
                print(e)

if __name__ == '__main__':
    # 消费券队列
    coupon_queue = Queue()
    # 存储goods_id, 领券点击地址的dict子元素的list
    goods_id_and_coupon_url_list = []
    # 待处理的goods_id, 对应coupon_url的子元素的队列
    goods_id_and_coupon_url_queue = Queue()
    # 已存储的唯一优惠券的list
    unique_coupon_id_list = []
    print('正在获取db_unique_coupon_id_list ...')
    # 从db中获取已存在的id
    sql_cli = SqlServerMyPageInfoSaveItemPipeline()
    try:
        db_res = list(sql_cli._select_table(
            sql_str='select unique_id from dbo.coupon_info'))
        unique_coupon_id_list = [item[0] for item in db_res]
        print('unique_coupon_id_list_len: {}'.format(len(unique_coupon_id_list)))
    except Exception as e:
        print(e)
    finally:
        try:
            del sql_cli
        except:
            pass
    print('获取完毕!')

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

    for i in range(1):
        func_args = ()
        task = GoodsIdAndCouponUrlQueueConsumer()
        thread_name = 'thread_task:{}:{}'.format(
            'GoodsIdAndCouponUrlQueueConsumer',
            get_uuid1(),)
        task.setName(name=thread_name)
        tasks.append(task)
        need_to_be_monitored_thread_tasks_info_list.append({
            'func_name': GoodsIdAndCouponUrlQueueConsumer,
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