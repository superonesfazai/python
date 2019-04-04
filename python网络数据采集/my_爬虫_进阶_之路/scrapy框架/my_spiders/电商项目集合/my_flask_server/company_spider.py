# coding:utf-8

"""
@author = super_fazai
@File    : company_spider.py
@connect : superonesfazai@gmail.com
"""

"""
企业商家信息爬虫

已实现:
    1. 天眼查
    2. 中国黄页
    3. 美团
    4. al 1688
    5. 114批发网
    6. 中国制造网(https://cn.made-in-china.com)
    7. 义乌购[义乌国际商贸城](http://www.yiwugo.com)
    8. 货牛牛(eg: 广州: http://www.huoniuniu.com/ | 杭州: http://hz.huoniuniu.com/ | ...)
    9. 品库(https://www.ppkoo.com/)
    10. 广州南国小商品城(http://www.nanguo.cn/|http://m.nanguo.cn/)

待实现:
    1. 购途网(http://www.go2.cn/)(女鞋货源)
Pass:
    1. 58(pc/m/wx站手机号为短期(内部电话转接) pass)
"""

from gc import collect

from settings import (
    MY_SPIDER_LOGS_PATH,
    COMPANY_ITEM_LIST,
    PHANTOMJS_DRIVER_PATH,
    CHROME_DRIVER_PATH,
    FIREFOX_DRIVER_PATH,)
from my_items import CompanyItem
from sql_str_controller import (
    gs_insert_str_1,
    gs_select_str_1,)
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from multiplex_code import (
    _get_new_db_conn,)

# 避免分布式task导入此包时报错!
try:
    from celery_tasks import (
        _get_al_one_type_company_id_list_task,
        _get_al_company_page_html_task,
        _get_114_one_type_company_id_list_task,
        _parse_one_company_info_task,
        _get_114_company_page_html_task,
        _get_yw_one_type_company_id_list_task,
        _get_hn_one_type_company_id_list_task,
        _get_pk_one_type_company_id_list_task,
        _get_ng_one_type_company_id_list_task,
        _get_gt_one_type_company_id_list_task,)
except ImportError:
    pass

from os import (walk, remove)
from os.path import exists as path_exists
from jieba import cut as jieba_cut
from requests import session
from datetime import datetime
from urllib.parse import urlencode
import requests_html
from pypinyin import lazy_pinyin
from dateutil.parser import parse as date_util_parse
from asyncio import TimeoutError as AsyncTimeoutError
from asyncio import wait_for
from PIL import Image

from fzutils.ip_pools import (
    tri_ip_pool,)
from fzutils.spider.selector import async_parse_field
from fzutils.spider.fz_driver import (
    PHONE,
    CHROME,
    FIREFOX,
    PHANTOMJS)
from fzutils.internet_utils import _get_url_contain_params
from fzutils.spider.fz_aiohttp import AioHttp
from fzutils.spider.selenium_always import *
from fzutils.data.excel_utils import async_read_info_from_excel_file
from fzutils.data.list_utils import list_remove_repeat_dict_plus
from fzutils.spider.fz_driver import BaseDriver
from fzutils.ocr_utils import yundama_ocr_captcha
from fzutils.celery_utils import _get_celery_async_results
from fzutils.memory_utils import get_current_func_info_by_traceback
from fzutils.spider.bloom_utils import BloomFilter
from fzutils.spider.async_always import *
from fzutils.shell_utils import *

# uvloop替换asyncio默认事件循环
set_event_loop_policy(EventLoopPolicy())
# 启动爬虫name
SPIDER_NAME = None

class CompanySpider(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            ip_pool_type=tri_ip_pool,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/companys/_/',)
        self.spider_name = 'gt' if SPIDER_NAME is None else SPIDER_NAME                 # 设置爬取对象
        self.concurrency = 300                                                          # 并发量, ty(推荐:5)高并发被秒封-_-! 慢慢抓
        self.sema = Semaphore(self.concurrency)
        assert 300 >= self.concurrency, 'self.concurrency并发量不允许大于300!'
        self.ty_max_page_num = 250                                                      # 设置天眼查抓取截止页数(查询限制5000个) max 250页
        self.qcc_max_page_num = 2000                                                    # 设置企查查抓取截止页数
        self.hy_min_company_id = 2896700                                                # hy抓取开始company_id (1-88402, 1187459-, 2865539-, 2871053-)
        self.hy_max_company_id = 2972941                                                # 设置hy抓取截止company_id(20000000)(直接写20000000, 程序会卡死)
        self.al_min_index_cate_id = 0                                                   # 设置al父分类最小的index_cate_id
        self.al_max_index_cate_id = 16                                                  # 设置al父分类最大的index_cate_id
        self.al_max_page_num = 100                                                      # 设置al单个子分类抓取截止的最大page_num(100, 往后无数据回传)
        self.a114_max_page_num = 50                                                     # 设置114单个子分类抓取截止最大page_num
        self.a114_max_num_retries = 15                                                  # 设置114单页面最大重试次数
        self.ic_max_page_num = 200                                                      # 设置ic单个子页面抓取截止最大page_num
        self.yw_max_num_retries = 10                                                    # 设置yw单页面最大重试次数
        self.yw_max_page_num = 100                                                      # 设置yw单个子分类抓取截止的最大page_num
        self.hn_city_info_list = []                                                     # hn的城市路由地址信息list
        self.hn_max_num_retries = 6                                                     # hn单页面最大重试数
        self.hn_max_page_num = 100                                                      # hn单个keyword最大搜索戒指页
        self.pk_max_page_num = 100000                                                   # pk单个keyword最大搜索截止页
        self.pk_max_num_retries = 6                                                     # pk num_retries
        self.ng_max_num_retries = 8                                                     # nf num_retries
        self.ng_max_page_num = 100                                                      # ng单个keyword最大搜索截止页面
        self.ng_capacity = None
        self.gt_max_num_retries = 8                                                     # gt最大重试数
        self.gt_max_page_num = 50                                                       # gt 单个keyword最大搜索截止页码
        self.mt_max_page_num = 50                                                       # mt最大限制页数(只抓取前50页, 后续无数据)
        self.mt_ocr_record_shop_id = ''                                                 # mt robot ocr record shop_id
        self.sql_server_cli = SqlServerMyPageInfoSaveItemPipeline()
        self._set_province_code_list_and_city_code_list()
        self.ty_cookies_dict = {}
        self.ty_robot = False                                                           # ty robot
        self.mt_robot = False                                                           # mt robot
        self.insert_into_sql = gs_insert_str_1                                          # 存储的sql_str
        self.driver_path = PHANTOMJS_DRIVER_PATH                                        # driver path
        self.driver_timeout = 20                                                        # driver timeout
        self.tb_jb_hot_keyword_file_path = '/Users/afa/Desktop/tb_jb_hot_keyword.txt'   # 结巴分词后已检索的hot keyword写入处
        self.tb_20w_path = '/Users/afa/Desktop/tb_top20w'                               # 待读取的tb20w xlsx文件目录
        self.bloom_filter = BloomFilter(capacity=5000000, error_rate=0.000001)
        self._init_tb_jb_boom_filter()
        # wx sc_key
        with open('/Users/afa/myFiles/pwd/server_sauce_sckey.json', 'r') as f:
            self.sc_key = json_2_dict(f.read())['sckey']

    def _init_tb_jb_boom_filter(self) -> None:
        """
        初始化
        :return:
        """
        self.lg.info('初始化ing self.tb_jb_boom_filter ...')
        self.tb_jb_boom_filter = BloomFilter(capacity=1000000, error_rate=.00001)       # 结巴分词后已检索的hot keyword存储
        try:
            with open(self.tb_jb_hot_keyword_file_path, 'r') as f:
                try:
                    for line in f:
                        item = line.replace('\n', '')
                        if item not in self.tb_jb_boom_filter:
                            self.tb_jb_boom_filter.add(item)
                except UnicodeDecodeError as e:
                    self.lg.error('遇到错误: {}'.format(e))

        except Exception as e:
            self.lg.error('遇到错误:', exc_info=True)
            raise e

        self.lg.info('初始化完毕! len: {}'.format(self.tb_jb_boom_filter.__len__()))

        return None

    def _set_province_code_list_and_city_code_list(self) -> None:
        """
        获取province, city的code
        :return:
        """
        sql_str = """select c_name, code, parent_code from dbo.Region"""
        self.province_and_city_code_list = []
        self.lg.info('正在获取province_and_city_code_list...')
        try:
            self.province_and_city_code_list = self.sql_server_cli._select_table(sql_str=sql_str, params=None)
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)

        assert self.province_and_city_code_list != [], 'self.province_and_city_code_list为空list!'
        self.lg.info('获取province_and_city_code_list成功!')

    async def _fck_run(self) -> None:
        await self._company_spider(short_name=self.spider_name)
        self.lg.info('全部抓取完毕!!')

    async def _company_spider(self, short_name:str) -> None:
        """
        公司 or 商家信息爬虫
        :param short_name:
        :return:
        """
        self.lg.info('--->>> spider_name: {}'.format(self.spider_name))
        if short_name == 'ty':
            # vip(1年360, tb 9.8) 会员才能查看多页的企业信息内容, 而且vip每天只能查看5000家公司, 真抠-_-!, pass
            await self._ty_spider()

        elif short_name == 'qcc':
            await self._qcc_spider()

        elif short_name == 'hy':
            await self._hy_spider()

        elif short_name == 'mt':
            await self._mt_spider()

        elif short_name == 'al':
            await self._al_spider()

        elif short_name == '114':
            await self._a114_spider()

        elif short_name == 'ic':
            await self._ic_spider()

        elif short_name == 'yw':
            await self._yw_spider()

        elif short_name == 'hn':
            await self._hn_spider()

        elif short_name == 'pk':
            await self._pk_spider()

        elif short_name == 'ng':
            await self._ng_spider()

        elif short_name == 'gt':
            await self._gt_spider()

        else:
            raise NotImplemented

    async def _gt_spider(self):
        """
        购途女鞋批发网spider(pc, 无m站)
        :return:
        """
        self.db_gt_unique_id_list = await self._get_db_unique_id_list_by_site_id(site_id=12)
        # 根据key抓取
        self.gt_category_list = await self._get_gt_category()
        pprint(self.gt_category_list)
        self.lg.info('gt所有子分类总个数: {}'.format(len(self.gt_category_list)))
        assert self.gt_category_list != [], '获取到的self.gt_category_list为空list!异常退出'

        await self._crawl_gt_company_info()

    async def _get_gt_category(self,) -> list:
        """
        获取gc的cate name list
        :return: ['板鞋',]
        """
        get_current_func_info_by_traceback(logger=self.lg, self=self)
        # search
        headers = await self._get_pc_headers()
        headers.update({
            'Connection': 'keep-alive',
            # 'Referer': 'http://www.go2.cn/search/all/?category_id=all&search_1=1&q=%E9%9E%8B%E5%AD%90',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        params = (
            ('category_id', 'all'),
            ('search_1', '1'),
            ('q', '鞋子'),
        )
        page_num = 1
        # /search/all
        url = 'http://www.go2.cn/search/all/page{}.html'.format(page_num)
        body = await unblock_request(
            url=url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.gt_max_num_retries,
            logger=self.lg,)
        # self.lg.info(body)

        parser_obj = await self._get_parser_obj(short_name='gt')
        # 获取该页面的所有鞋子属性!
        shoes_attr_name_list1 = await async_parse_field(
            parser=parser_obj['trade_type_info']['shoes_attr_name1'],
            target_obj=body,
            is_first=False,
            logger=self.lg,)
        assert shoes_attr_name_list1 != [], 'shoes_attr_name_list1不为空值list!'
        shoes_attr_name_list2 = await async_parse_field(
            parser=parser_obj['trade_type_info']['shoes_attr_name2'],
            target_obj=body,
            is_first=False,
            logger=self.lg,)
        assert shoes_attr_name_list2 != [], 'shoes_attr_name_list2不为空值list!'
        all_shoes_attr_name_list = list(set(shoes_attr_name_list1 + shoes_attr_name_list2))

        return all_shoes_attr_name_list

    async def _crawl_gt_company_info(self,):
        """
        抓取gt公司信息
        :return:
        """
        async def _get_tasks_params_list(**kwargs) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for page_num in range(1, self.gt_max_page_num + 1):
                tasks_params_list.append({
                    'keyword': kwargs['cate_name'],
                    'page_num': page_num,
                })

            return tasks_params_list

        async def _get_one_res(slice_params_list, parser_obj) -> list:
            """获取one_res"""
            async def _create_one_celery_task(**kwargs):
                keyword = kwargs['keyword']
                page_num = kwargs['page_num']
                company_url_selector = kwargs['company_url_selector']
                company_id_selector = kwargs['company_id_selector']

                async_obj = _get_gt_one_type_company_id_list_task.apply_async(
                    args=[
                        self.ip_pool_type,
                        keyword,
                        company_url_selector,
                        company_id_selector,
                        page_num,
                        self.gt_max_num_retries,
                    ],
                    expires=5 * 60,
                    retry=False,
                )

                return async_obj

            tasks = []
            for k in slice_params_list:
                keyword = k['keyword']
                page_num = k['page_num']
                self.lg.info('create task[where keyword: {}, page_num: {}]...'.format(keyword, page_num))
                try:
                    async_obj = await _create_one_celery_task(
                        keyword=keyword,
                        page_num=page_num,
                        company_url_selector=parser_obj['trade_type_info']['company_url'],
                        company_id_selector=parser_obj['unique_id'],)
                    tasks.append(async_obj)
                except:
                    continue

            # celery ng
            one_res = await _get_celery_async_results(tasks=tasks)

            return one_res

        async def _get_one_all_company_id_list(one_res) -> list:
            """获取该子分类截止页面的所有company_id_list"""
            one_all_company_id_list = []
            for i in one_res:
                try:
                    for j in i:
                        company_id = j.get('company_id', '')
                        if 'gt' + company_id not in self.db_gt_unique_id_list:
                            one_all_company_id_list.append({
                                'company_id': company_id,
                            })
                except TypeError:
                    return []

            one_all_company_id_list = list_remove_repeat_dict_plus(
                target=one_all_company_id_list,
                repeat_key='company_id',)

            return one_all_company_id_list

        get_current_func_info_by_traceback(self=self, logger=self.lg,)
        self.lg.info('即将开始采集gt shop info...')
        new_concurrency = 300
        new_tasks_params_list = []
        parser_obj = await self._get_parser_obj(short_name='gt')
        for cate_name_index, cate_name in enumerate(self.gt_category_list):
            self.lg.info('crawl cate_name: {}, cate_name_index: {}...'.format(cate_name, cate_name_index,))
            tasks_params_list = await _get_tasks_params_list(cate_name=cate_name,)
            try:
                new_tasks_params_list = await self._get_new_tasks_params_list_from_tasks_params_list(
                    tasks_params_list=tasks_params_list,
                    new_concurrency=new_concurrency,
                    new_tasks_params_list=new_tasks_params_list)
            except AssertionError:
                continue

            # new_step = self.concurrency
            new_step = 300
            tasks_params_list_obj = TasksParamsListObj(
                tasks_params_list=new_tasks_params_list,
                step=new_step)
            while True:
                try:
                    slice_params_list = tasks_params_list_obj.__next__()
                except AssertionError:
                    break

                one_res = await _get_one_res(
                    slice_params_list=slice_params_list,
                    parser_obj=parser_obj,)
                # pprint(one_res)
                one_all_company_id_list = await _get_one_all_company_id_list(one_res=one_res)

                self.lg.info('one_all_company_id_list num: {}'.format(len(one_all_company_id_list)))
                await self._crawl_gt_one_type_all_company_info(
                    one_all_company_id_list=one_all_company_id_list)
                collect()

            # 重置
            new_tasks_params_list = []
            collect()
            # break

        # break

        return None

    async def _crawl_gt_one_type_all_company_info(self, one_all_company_id_list):
        """
        抓取gt keyword的所有company_info
        :param one_all_company_id_list:
        :return:
        """
        async def _get_tasks_params_list(one_all_company_id_list) -> list:
            """获取tasks_params_list"""
            get_current_func_info_by_traceback(self=self, logger=self.lg)
            tasks_params_list = []
            for item in one_all_company_id_list:
                company_id = item['company_id']
                if 'gt' + company_id not in self.bloom_filter:
                    tasks_params_list.append({
                        'company_id': company_id,
                    })
                else:
                    continue

            self.lg.info('company_id 去重ing...')
            tasks_params_list = list_remove_repeat_dict_plus(
                target=tasks_params_list,
                repeat_key='company_id')

            return tasks_params_list

        async def _get_one_res(slice_params_list) -> list:
            """获取one_res"""
            get_current_func_info_by_traceback(self=self, logger=self.lg)
            tasks = []
            for k in slice_params_list:
                company_id = k['company_id']
                self.lg.info('create task[where company_id: {}]'.format(company_id))
                company_url = 'http://{}.go2.cn'.format(company_id)
                tasks.append(self.loop.create_task(self._parse_one_company_info(
                    short_name='gt',
                    company_id=company_id,
                    company_url=company_url,)))

            one_res = await async_wait_tasks_finished(tasks=tasks)

            return one_res

        get_current_func_info_by_traceback(self=self, logger=self.lg)
        tasks_params_list = await _get_tasks_params_list(one_all_company_id_list=one_all_company_id_list)
        new_step = self.concurrency
        # new_step = 30
        tasks_params_list_obj = TasksParamsListObj(
            tasks_params_list=tasks_params_list,
            step=new_step,)

        index = 0
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            # asyncio
            one_res = await _get_one_res(slice_params_list=slice_params_list)

            # 存储
            index, self.db_gt_unique_id_list = await self._save_company_one_res(
                one_res=one_res,
                short_name='gt',
                db_unique_id_list=self.db_gt_unique_id_list,
                index=index,)

        collect()

        return None

    async def _ng_spider(self):
        """
        南国批发网spider(m站)
        :return:
        """
        self.db_ng_unique_id_list = await self._get_db_unique_id_list_by_site_id(site_id=11)
        # 根据key抓取
        # self.ng_category_list = await self._get_ng_category()
        # self.ng_category_list = await self._get_al_category6()
        # pprint(self.ng_category_list)
        # self.lg.info('ng所有子分类总个数: {}'.format(len(self.ng_category_list)))
        # assert self.ng_category_list != [], '获取到的self.ng_category_list为空list!异常退出'
        # 
        # await self._crawl_ng_company_info()
        
        # 全站抓取
        self.ng_category_list = []
        one_all_company_id_list = await self._get_ng_all_company_id_list()
        self.lg.info('all_company_id_list: {}'.format(len(one_all_company_id_list)))
        await self._crawl_ng_one_type_all_company_info(one_all_company_id_list=one_all_company_id_list)
    
    async def _get_ng_all_company_id_list(self) -> list:
        """
        穷举获取ng所有company_id
        :return: 
        """
        one_all_company_id_list = []
        self.ng_capacity = 100000
        for company_id in range(1, self.ng_capacity):
            company_id = str(company_id)
            if 'ng' + company_id not in self.db_ng_unique_id_list:
                one_all_company_id_list.append({
                    'company_id': company_id,
                    'province_name': '广东省',
                    'city_name': '广州市',
                })
            else:
                continue

        return one_all_company_id_list
        
    async def _get_ng_category(self) -> list:
        """
        获取ng的cate_name_list
        :return: ['跳绳', ...]
        """
        async def _get_ng_cate_api_info(parser_obj, main_cate_id=None) -> tuple:
            """
            获取ng的cate info
            :param parser_obj:
            :param main_cate_id:
            :return:
            """
            headers = await self._get_phone_headers()
            headers.update({
                'connection': 'keep-alive',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
                # 'Referer': 'http://m.nanguo.cn/',
            })
            url = 'http://m.nanguo.cn/products.html' \
                if main_cate_id is None \
                else 'http://m.nanguo.cn/products.html?id={}'.format(main_cate_id)
            body = await unblock_request(
                url=url,
                headers=headers,
                ip_pool_type=self.ip_pool_type,
                num_retries=self.ng_max_num_retries,)
            # self.lg.info(body)

            # 主分类 li.category-li a ::attr("href") 获取主分类id
            main_cate_info_list = await async_parse_field(
                parser=parser_obj['trade_type_info']['type_url_sub'],
                target_obj=body,
                is_first=False,
                logger=self.lg)
            # pprint(main_cate_info_list)

            # 存储主分类id
            main_cate_id_list = []
            for item in main_cate_info_list:
                try:
                    cate_id = int(await async_parse_field(
                        parser=parser_obj['trade_type_info']['type_id_sub'],
                        target_obj=item,
                        logger=self.lg,))
                    if cate_id not in main_cate_id_list:
                        main_cate_id_list.append(cate_id)
                except Exception:
                    continue
            # pprint(main_cate_id_list)

            # 主分类的子分类获取
            child_cate_name_list = await async_parse_field(
                parser=parser_obj['trade_type_info']['type_name_third'],
                target_obj=body,
                is_first=False,
                logger=self.lg,)

            return (main_cate_id_list, child_cate_name_list)

        async def _get_tasks_params_list(main_cate_id_list) -> list:
            """获取tasks_params_list"""
            get_current_func_info_by_traceback(self=self, logger=self.lg,)
            tasks_params_list = []
            for item in main_cate_id_list:
                tasks_params_list.append({
                    'main_cate_id': item,
                })

            return tasks_params_list

        async def _get_one_res(slice_params_list) -> list:
            tasks = []
            for k in slice_params_list:
                main_cate_id = k['main_cate_id']
                self.lg.info('create task[where main_cate_id: {}]...'.format(main_cate_id))
                tasks.append(self.loop.create_task(_get_ng_cate_api_info(
                    parser_obj=parser_obj,
                    main_cate_id=main_cate_id,
                )))

            one_res = await async_wait_tasks_finished(tasks=tasks)

            return one_res

        get_current_func_info_by_traceback(self=self, logger=self.lg,)
        parser_obj = await self._get_parser_obj(short_name='ng')
        # 先获取一次main_cate_id_list
        main_cate_id_list = (await _get_ng_cate_api_info(parser_obj=parser_obj))[0]
        pprint(main_cate_id_list)
        tasks_params_list = await _get_tasks_params_list(main_cate_id_list)
        tasks_params_list_obj = TasksParamsListObj(
            tasks_params_list=tasks_params_list,
            step=self.concurrency,)
        all_cate_name_list = []
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            one_res = await _get_one_res(
                slice_params_list=slice_params_list,)
            # pprint(one_res)
            for i in one_res:
                child_name_list = i[1]
                for n in child_name_list:
                    if n not in all_cate_name_list:
                        all_cate_name_list.append(n)

        return all_cate_name_list

    async def _crawl_ng_company_info(self):
        """
        抓取ng company_info
        :return:
        """
        async def _get_tasks_params_list(**kwargs) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for page_num in range(1, self.ng_max_page_num + 1):
                tasks_params_list.append({
                    'keyword': kwargs['cate_name'],
                    'page_num': page_num,
                })

            return tasks_params_list

        async def _get_one_res(slice_params_list, parser_obj) -> list:
            """获取one_res"""
            async def _create_one_celery_task(**kwargs):
                keyword = kwargs['keyword']
                page_num = kwargs['page_num']
                company_item_id_selector = kwargs['company_item_id_selector']

                async_obj = _get_ng_one_type_company_id_list_task.apply_async(
                    args=[
                        self.ip_pool_type,
                        keyword,
                        page_num,
                        company_item_id_selector,
                        self.ng_max_num_retries,
                    ],
                    expires=5 * 60,
                    retry=False,
                )

                return async_obj

            tasks = []
            for k in slice_params_list:
                keyword = k['keyword']
                page_num = k['page_num']
                self.lg.info('create task[where keyword: {}, page_num: {}]...'.format(keyword, page_num))
                try:
                    async_obj = await _create_one_celery_task(
                        keyword=keyword,
                        page_num=page_num,
                        company_item_id_selector=parser_obj['trade_type_info']['one_type_cate_id_list'],)
                    tasks.append(async_obj)
                except:
                    continue

            # celery ng
            one_res = await _get_celery_async_results(tasks=tasks)

            return one_res

        async def _get_one_all_company_id_list(one_res) -> list:
            """获取该子分类截止页面的所有company_id_list"""
            one_all_company_id_list = []
            for i in one_res:
                try:
                    for j in i:
                        company_id = j.get('company_id', '')
                        if 'ng' + company_id not in self.db_ng_unique_id_list:
                            one_all_company_id_list.append({
                                'company_id': company_id,
                            })
                except TypeError:
                    return []

            one_all_company_id_list = list_remove_repeat_dict_plus(
                target=one_all_company_id_list,
                repeat_key='company_id',)

            return one_all_company_id_list

        get_current_func_info_by_traceback(self=self, logger=self.lg,)
        self.lg.info('即将开始采集ng shop info...')
        new_concurrency = 1000
        new_tasks_params_list = []
        parser_obj = await self._get_parser_obj(short_name='ng')
        for cate_name_index, cate_name in enumerate(self.ng_category_list):
            self.lg.info('crawl cate_name: {}, cate_name_index: {}...'.format(cate_name, cate_name_index,))
            tasks_params_list = await _get_tasks_params_list(cate_name=cate_name,)
            try:
                new_tasks_params_list = await self._get_new_tasks_params_list_from_tasks_params_list(
                    tasks_params_list=tasks_params_list,
                    new_concurrency=new_concurrency,
                    new_tasks_params_list=new_tasks_params_list)
            except AssertionError:
                continue

            # new_step = self.concurrency
            # 并发量设置为1000, 不用默认的300
            new_step = 1000
            tasks_params_list_obj = TasksParamsListObj(
                tasks_params_list=new_tasks_params_list,
                step=new_step)
            while True:
                try:
                    slice_params_list = tasks_params_list_obj.__next__()
                except AssertionError:
                    break

                one_res = await _get_one_res(
                    slice_params_list=slice_params_list,
                    parser_obj=parser_obj,)
                # pprint(one_res)
                one_all_company_id_list = await _get_one_all_company_id_list(one_res=one_res)

                self.lg.info('one_all_company_id_list num: {}'.format(len(one_all_company_id_list)))
                await self._crawl_ng_one_type_all_company_info(
                    one_all_company_id_list=one_all_company_id_list)
                collect()

            # 重置
            new_tasks_params_list = []
            collect()
            # break

        # break

        return None

    async def _crawl_ng_one_type_all_company_info(self, one_all_company_id_list) -> None:
        """
        获取ng单个keyword所有的company_info
        :param one_all_company_id_list:
        :return:
        """
        async def _get_tasks_params_list(one_all_company_id_list) -> list:
            """获取tasks_params_list"""
            get_current_func_info_by_traceback(self=self, logger=self.lg)
            tasks_params_list = []
            for item in one_all_company_id_list:
                company_id = item['company_id']
                # if 'ng' + company_id not in self.db_ng_unique_id_list:
                if 'ng' + company_id not in self.bloom_filter:
                    self.lg.info('add company_id: {}'.format(company_id))
                    tasks_params_list.append({
                        'company_id': company_id,
                        'province_name': '广东省',
                        'city_name': '广州市',
                    })
                else:
                    continue

            self.lg.info('company_id 去重ing...')
            if not isinstance(self.ng_capacity, int):
                tasks_params_list = list_remove_repeat_dict_plus(
                    target=tasks_params_list,
                    repeat_key='company_id')
            else:
                tasks_params_list = list_remove_repeat_dict_plus_by_bloom_filter(
                    target=tasks_params_list,
                    repeat_key='company_id',
                    capacity=self.ng_capacity,
                    error_rate=1/self.ng_capacity*10,)

            return tasks_params_list

        async def _get_one_res(slice_params_list) -> list:
            """获取one_res"""
            get_current_func_info_by_traceback(self=self, logger=self.lg)
            tasks = []
            for k in slice_params_list:
                # self.lg.info(str(k))
                company_id = k['company_id']
                if 'ng' + company_id in self.db_ng_unique_id_list:
                    self.lg.info('company_id: {} in db, so pass!'.format(company_id))
                    continue

                self.lg.info('create task[where company_id: {}]'.format(company_id))
                company_url = 'http://www.nanguo.cn/company/index/id/{}'.format(company_id)
                tasks.append(self.loop.create_task(self._parse_one_company_info(
                    short_name='ng',
                    company_id=company_id,
                    province_name=k['province_name'],
                    city_name=k['city_name'],
                    company_url=company_url,)))

            one_res = await async_wait_tasks_finished(tasks=tasks)

            return one_res

        get_current_func_info_by_traceback(self=self, logger=self.lg)
        tasks_params_list = await _get_tasks_params_list(one_all_company_id_list=one_all_company_id_list)
        new_step = self.concurrency
        # new_step = 30
        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=new_step)

        index = 0
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            # asyncio
            one_res = await _get_one_res(slice_params_list=slice_params_list)

            # 存储
            index, self.db_ng_unique_id_list = await self._save_company_one_res(
                one_res=one_res,
                short_name='ng',
                db_unique_id_list=self.db_ng_unique_id_list,
                index=index,)

            # await async_sleep(3.)

        collect()

        return None

    async def _pk_spider(self):
        """
        品库spider(m站)
        :return:
        """
        self.db_pk_unique_id_list = await self._get_db_unique_id_list_by_site_id(site_id=10)
        self.pk_category_list = await self._get_pk_category()
        # 汉字
        # self.pk_category_list = await self._get_al_category4()
        # self.pk_category_list = 'z x c v b n m a s d f g h j k l p o i u y t r e w q 1 2 3 4 5 6 7 8 9 0'.split(' ')

        pprint(self.pk_category_list)
        self.lg.info('pk所有子分类总个数: {}'.format(len(self.pk_category_list)))
        assert self.pk_category_list != [], '获取到的self.pk_category_list为空list!异常退出'

        await self._crawl_pk_company_info()

    async def _get_pk_category(self) -> list:
        """
        获取pk 关键字
        :return: ['上衣', ...]
        """
        parser_obj = await self._get_parser_obj(short_name='pk')
        headers = await self._get_phone_headers()
        headers.update({
            'authority': 'm.ppkoo.com',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        url = 'https://m.ppkoo.com/classlist'
        body = await unblock_request(
            url=url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            logger=self.lg)

        tmp_type_name_sub_list = await async_parse_field(
            parser=parser_obj['trade_type_info']['type_name_sub'],
            target_obj=body,
            is_first=False,
            logger=self.lg)

        type_name_sub_list = []
        # 处理item 为 '蕾丝衫/雪纺衫'的
        for item in tmp_type_name_sub_list:
            item_list = item.split('/')
            for i in item_list:
                if i not in type_name_sub_list:
                    type_name_sub_list.append(i)
        # pprint(type_name_sub_list)

        return type_name_sub_list

    async def _crawl_pk_company_info(self):
        """
        抓取品库所有company info
        :return:
        """
        async def _get_tasks_params_list(**kwargs) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for page_num in range(1, self.pk_max_page_num + 1):
                tasks_params_list.append({
                    'keyword': kwargs['cate_name'],
                    'page_num': page_num,
                    'province_name': kwargs['province_name'],
                    'city_name': kwargs['city_name'],
                    'city_id': kwargs['city_id'],
                    'w3': kwargs['w3'],
                })

            return tasks_params_list

        async def _get_one_res(slice_params_list,) -> list:
            """获取one_res"""
            async def _create_one_celery_task(**kwargs):
                ip_pool_type = kwargs['ip_pool_type']
                keyword = kwargs['keyword']
                page_num = kwargs['page_num']
                province_name = kwargs['province_name']
                city_name = kwargs['city_name']
                city_id = kwargs['city_id']
                w3 = kwargs['w3']

                async_obj = _get_pk_one_type_company_id_list_task.apply_async(
                    args=[
                        ip_pool_type,
                        keyword,
                        page_num,
                        province_name,
                        city_name,
                        city_id,
                        w3,
                        self.pk_max_num_retries,
                    ],
                    expires=5 * 60,
                    retry=False,
                )

                return async_obj

            tasks = []
            for k in slice_params_list:
                keyword = k['keyword']
                page_num = k['page_num']
                self.lg.info('create task[where keyword: {}, page_num: {}]...'.format(keyword, page_num))
                try:
                    async_obj = await _create_one_celery_task(
                        ip_pool_type=self.ip_pool_type,
                        keyword=keyword,
                        page_num=page_num,
                        province_name=k['province_name'],
                        city_name=k['city_name'],
                        city_id=k['city_id'],
                        w3=k['w3'],)
                    tasks.append(async_obj)
                except:
                    continue

            # celery pk
            one_res = await _get_celery_async_results(tasks=tasks)

            return one_res

        async def _get_one_all_company_id_list(one_res) -> list:
            """获取该子分类截止页面的所有company_id_list"""
            one_all_company_id_list = []
            tmp_id_list = []
            for i in one_res:
                try:
                    for j in i:
                        company_id = j.get('company_id', '')
                        if 'pk' + company_id not in self.db_pk_unique_id_list:
                            if company_id not in tmp_id_list:
                                one_all_company_id_list.append({
                                    'company_id': company_id,
                                    'province_name': j['province_name'],
                                    'city_name': j['city_name'],
                                    'w3': j['w3'],
                                    'address': j['address'],
                                })
                                tmp_id_list.append(company_id)
                except TypeError:
                    return []

            return one_all_company_id_list

        self.lg.info('即将开始采集pk shop info...')
        new_concurrency = 1200
        new_tasks_params_list = []
        parser_obj = await self._get_parser_obj(short_name='pk')
        self.new_pk_city_info_list = await self._get_pk_new_hn_city_info_list()
        for ii in self.new_pk_city_info_list:
            province_name, city_name, city_id, w3 = ii['province_name'], ii['city_name'], ii['city_id'], ii['w3']
            for cate_name_index, cate_name in enumerate(self.pk_category_list):
                self.lg.info('crawl cate_name: {}, cate_name_index: {}, city_name: {} ...'.format(cate_name, cate_name_index, city_name))
                tasks_params_list = await _get_tasks_params_list(
                    cate_name=cate_name,
                    province_name=province_name,
                    city_name=city_name,
                    city_id=city_id,
                    w3=w3,)
                try:
                    new_tasks_params_list = await self._get_new_tasks_params_list_from_tasks_params_list(
                        tasks_params_list=tasks_params_list,
                        new_concurrency=new_concurrency,
                        new_tasks_params_list=new_tasks_params_list)
                except AssertionError:
                    continue

                # new_step = self.concurrency
                # 并发量设置为1200, 不用默认的300
                new_step = 1200
                tasks_params_list_obj = TasksParamsListObj(
                    tasks_params_list=new_tasks_params_list,
                    step=new_step)
                while True:
                    try:
                        slice_params_list = tasks_params_list_obj.__next__()
                    except AssertionError:
                        break

                    one_res = await _get_one_res(
                        slice_params_list=slice_params_list,)
                    # pprint(one_res)
                    one_all_company_id_list = await _get_one_all_company_id_list(one_res=one_res)

                    self.lg.info('one_all_company_id_list num: {}'.format(len(one_all_company_id_list)))
                    await self._crawl_pk_one_type_all_company_info(
                        one_all_company_id_list=one_all_company_id_list)
                    collect()

                # 重置
                new_tasks_params_list = []
                collect()
                # break

            # break

        return None

    async def _crawl_pk_one_type_all_company_info(self, one_all_company_id_list):
        """
        抓取pk单个keyword所有的公司信息
        :param one_all_company_id_list:
        :return:
        """
        async def _get_tasks_params_list(one_all_company_id_list) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for item in one_all_company_id_list:
                company_id = item['company_id']
                if 'pk' + company_id not in self.db_pk_unique_id_list:
                    tasks_params_list.append({
                        'company_id': company_id,
                        'province_name': item['province_name'],
                        'city_name': item['city_name'],
                        'w3': item['w3'],
                        'address': item['address'],
                    })
                else:
                    continue

            tasks_params_list = list_remove_repeat_dict_plus(
                target=tasks_params_list,
                repeat_key='company_id')

            return tasks_params_list

        async def _get_one_res(slice_params_list) -> list:
            """获取one_res"""
            tasks = []
            for k in slice_params_list:
                # self.lg.info(str(k))
                company_id = k['company_id']
                w3 = k['w3']
                address = k['address']
                if 'pk' + company_id in self.db_pk_unique_id_list:
                    self.lg.info('company_id: {} in db, so pass!'.format(company_id))
                    continue

                self.lg.info('create task[where company_id: {}]'.format(company_id))
                company_url = 'https://{}.ppkoo.com/shop/{}.html'.format(w3, company_id)
                tasks.append(self.loop.create_task(self._parse_one_company_info(
                    short_name='pk',
                    company_id=company_id,
                    province_name=k['province_name'],
                    city_name=k['city_name'],
                    company_url=company_url,
                    ori_address=address,)))

            one_res = await async_wait_tasks_finished(tasks=tasks)

            return one_res

        # 对应company_id 采集该分类截止页面的所有company info
        tasks_params_list = await _get_tasks_params_list(one_all_company_id_list=one_all_company_id_list)
        new_step = self.concurrency
        # new_step = 30
        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=new_step)

        index = 0
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            # asyncio
            one_res = await _get_one_res(slice_params_list=slice_params_list)

            # 存储
            index, self.db_pk_unique_id_list = await self._save_company_one_res(
                one_res=one_res,
                short_name='pk',
                db_unique_id_list=self.db_pk_unique_id_list,
                index=index,)

            # await async_sleep(3.)

        return None

    @staticmethod
    async def _get_pk_new_hn_city_info_list():
        """
        获取pk 城市对应信息
        :return:
        """
        return [
            {
                'city_id': 1,
                'city_name': '广州市',
                'province_name': '广东省',
                'w3': 'www',
            },
            {
                'city_id': 2,
                'city_name': '温州市',
                'province_name': '浙江省',
                'w3': 'wz',
            },
            {
                'city_id': 3,
                'city_name': '杭州市',
                'province_name': '浙江省',
                'w3': 'hz',
            },
            {
                'city_id': 4,
                'city_name': '高碑店市',         # 保定市的高碑店市的白沟
                'province_name': '河北省',
                'w3': 'bg',
            },
        ]

    async def _hn_spider(self):
        """
        货牛牛spider(pc站)
        :return:
        """
        self.db_hn_unique_id_list = await self._get_db_unique_id_list_by_site_id(site_id=9)
        self.hn_category_list = await self._get_hn_category()
        # self.hn_category_list = await self._get_al_category5()
        self.hn_category_list = await self._get_pk_category()

        pprint(self.hn_category_list)
        self.lg.info('hn所有子分类总个数: {}'.format(len(self.hn_category_list)))
        assert self.hn_category_list != [], '获取到的self.hn_category_list为空list!异常退出'

        await self._crawl_hn_company_info()

    async def _get_hn_category(self) -> list:
        """
        获取hn关键字
        :return: ['短袖', ...]
        """
        async def _get_hn_base_info(trade_type_selector) -> tuple:
            """获取相关信息"""
            headers = await self._get_pc_headers()
            headers.update({
                'Proxy-Connection': 'keep-alive',
            })
            url = 'http://www.huoniuniu.com/'
            body = await unblock_request(
                url=url,
                headers=headers,
                ip_pool_type=self.ip_pool_type,
                num_retries=self.hn_max_num_retries,
                logger=self.lg)
            # self.lg.info(body)

            # ['T恤', ....]
            main_sort_name_list = await async_parse_field(
                parser=trade_type_selector['type_name_sub'],
                target_obj=body,
                is_first=False,
                logger=self.lg,)
            main_sort_cid_list = list(set(await async_parse_field(
                parser=trade_type_selector['type_cid_sub'],
                target_obj=body,
                is_first=False,
                logger=self.lg,)))
            city_name_list = await async_parse_field(
                parser=trade_type_selector['city_name'],
                target_obj=body,
                is_first=False,
                logger=self.lg,)
            city_url_list = await async_parse_field(
                parser=trade_type_selector['city_url'],
                target_obj=body,
                is_first=False,
                logger=self.lg,)
            city_info_list = list(zip(city_name_list, city_url_list))
            main_sort_name_list = [item.replace(' ', '') for item in main_sort_name_list]

            return main_sort_name_list, main_sort_cid_list, city_info_list

        async def _get_tasks_params_list(cate_info_list) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for i in cate_info_list:
                tasks_params_list.append({
                    'cate_id': i,
                })

            return tasks_params_list

        async def _get_one_res(slice_params_list) -> list:
            tasks = []
            for k in slice_params_list:
                cate_id = k['cate_id']
                self.lg.info('create task[where cate_id: {}]'.format(cate_id))
                tasks.append(self.loop.create_task(_get_hn_one_cate_id_keyword_list(
                    cate_id=cate_id,
                )))

            one_res = await async_wait_tasks_finished(tasks=tasks)
            # pprint(one_res)

            return one_res

        async def _get_hn_one_cate_id_keyword_list(cate_id) -> list:
            """
            单个cate id 对应的keyword list
            :param cate_id:
            :return: ['短袖', ...]
            """
            headers = await self._get_pc_headers()
            headers.update({
                'Proxy-Connection': 'keep-alive',
            })
            params = (
                ('ajax', '1'),
                ('cid', cate_id),
            )
            url = 'http://www.huoniuniu.com/api/getCategory'
            body = await unblock_request(
                url=url,
                headers=headers,
                params=params,
                ip_pool_type=self.ip_pool_type,
                num_retries=self.hn_max_num_retries,
                logger=self.lg)
            # self.lg.info(body)
            cate_list = json_2_dict(
                json_str=body,
                default_res={},
                logger=self.lg).get('categorys', [])
            # ['短袖', ...]
            data = [item.get('name', '') for item in cate_list]
            self.lg.info('[{}] cate_id: {}'.format(
                '+' if data != [] else '-',
                cate_id))

            return data

        parser_obj = await self._get_parser_obj(short_name='hn')
        # 获取父分类信息, cid, hn城市路由地址
        main_sort_name_list, main_sort_cid_list, self.hn_city_info_list = await _get_hn_base_info(trade_type_selector=parser_obj['trade_type_info'])
        pprint(main_sort_name_list)
        pprint(main_sort_cid_list)
        pprint(self.hn_city_info_list)

        # 获取父分类的子分类
        tasks_params_list = await _get_tasks_params_list(cate_info_list=main_sort_cid_list)
        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=self.concurrency)
        all_keywords_list = main_sort_name_list
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            one_res = await _get_one_res(slice_params_list=slice_params_list)
            for i in one_res:
                for j in i:
                    if j not in all_keywords_list:
                        all_keywords_list.append(j.replace(' ', ''))

        # pprint(all_keywords_list)
        self.lg.info('获取到的父分类的子分类总个数: {}'.format(len(all_keywords_list)))

        all_hn_child_cate_info_list = all_keywords_list

        return all_hn_child_cate_info_list

    async def _crawl_hn_company_info(self):
        """
        采集hn所有商家信息
        :return:
        """
        async def _get_tasks_params_list(**kwargs) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for page_num in range(1, self.hn_max_page_num + 1):
                tasks_params_list.append({
                    'keyword': kwargs['cate_name'],
                    'page_num': page_num,
                    'province_name': kwargs['province_name'],
                    'city_name': kwargs['city_name'],
                    'city_base_url': kwargs['city_base_url'],
                })

            return tasks_params_list

        async def _get_one_res(slice_params_list, parser_obj) -> list:
            """获取one_res"""
            async def _create_one_celery_task(**kwargs):
                ip_pool_type = kwargs['ip_pool_type']
                keyword = kwargs['keyword']
                page_num = kwargs['page_num']
                province_name = kwargs['province_name']
                city_name = kwargs['city_name']
                city_base_url = kwargs['city_base_url']
                shop_item_selector = parser_obj['trade_type_info']['shop_item']
                shop_id_selector = parser_obj['unique_id']
                w3_selector = parser_obj['trade_type_info']['w3']

                async_obj = _get_hn_one_type_company_id_list_task.apply_async(
                    args=[
                        ip_pool_type,
                        keyword,
                        page_num,
                        province_name,
                        city_name,
                        city_base_url,
                        shop_item_selector,
                        shop_id_selector,
                        w3_selector,
                        self.hn_max_num_retries,
                    ],
                    expires=5 * 60,
                    retry=False,
                )

                return async_obj

            tasks = []
            for k in slice_params_list:
                keyword = k['keyword']
                page_num = k['page_num']
                self.lg.info('create task[where keyword: {}, page_num: {}]...'.format(keyword, page_num))
                tasks.append(self.loop.create_task(self._get_hn_one_type_company_id_list(
                    keyword=keyword,
                    page_num=page_num,
                    province_name=k['province_name'],
                    city_name=k['city_name'],
                    city_base_url=k['city_base_url'],
                    shop_item_selector=parser_obj['trade_type_info']['shop_item'],
                    shop_id_selector=parser_obj['unique_id'],
                    w3_selector=parser_obj['trade_type_info']['w3'],)))

                # try:
                #     async_obj = await _create_one_celery_task(
                #         ip_pool_type=self.ip_pool_type,
                #         keyword=keyword,
                #         page_num=page_num,
                #         parser_obj=parser_obj,
                #         province_name=k['province_name'],
                #         city_name=k['city_name'],
                #         city_base_url=k['city_base_url'],
                #     )
                #     tasks.append(async_obj)
                # except:
                #     continue

            # asyncio 测试发现hn 的搜索页requests成功率低, 改用driver
            one_res = await async_wait_tasks_finished(tasks=tasks)
            # celery hn
            # one_res = await _get_celery_async_results(tasks=tasks)

            return one_res

        async def _get_one_all_company_id_list(one_res) -> list:
            """获取该子分类截止页面的所有company_id_list"""
            one_all_company_id_list = []
            tmp_id_list = []
            for i in one_res:
                try:
                    for j in i:
                        company_id = j.get('company_id', '')
                        if 'hn' + company_id not in self.db_hn_unique_id_list:
                            if company_id not in tmp_id_list:
                                one_all_company_id_list.append({
                                    'company_id': company_id,
                                    'province_name': j['province_name'],
                                    'city_name': j['city_name'],
                                    'w3': j['w3'],
                                })
                                tmp_id_list.append(company_id)
                except TypeError:
                    return []

            return one_all_company_id_list

        self.lg.info('即将开始采集hn shop info...')
        new_concurrency = 300
        new_tasks_params_list = []
        parser_obj = await self._get_parser_obj(short_name='hn')
        self.new_hn_city_info_list = await self._get_hn_new_hn_city_info_list()
        for ii in self.new_hn_city_info_list:
            province_name, city_name, city_base_url = ii['province_name'], ii['city_name'], ii['city_base_url']
            for cate_name_index, cate_name in enumerate(self.hn_category_list):
                self.lg.info('crawl cate_name: {}, cate_name_index: {} ...'.format(cate_name, cate_name_index))
                tasks_params_list = await _get_tasks_params_list(
                    cate_name=cate_name,
                    province_name=province_name,
                    city_name=city_name,
                    city_base_url=city_base_url,)
                try:
                    new_tasks_params_list = await self._get_new_tasks_params_list_from_tasks_params_list(
                        tasks_params_list=tasks_params_list,
                        new_concurrency=new_concurrency,
                        new_tasks_params_list=new_tasks_params_list)
                except AssertionError:
                    continue

                # new_step = self.concurrency
                new_step = 30
                tasks_params_list_obj = TasksParamsListObj(tasks_params_list=new_tasks_params_list, step=new_step)
                while True:
                    try:
                        slice_params_list = tasks_params_list_obj.__next__()
                    except AssertionError:
                        break

                    one_res = await _get_one_res(
                        slice_params_list=slice_params_list,
                        parser_obj=parser_obj,)
                    # pprint(one_res)
                    kill_process_by_name('phantomjs')
                    kill_process_by_name('firefox')

                    one_all_company_id_list = await _get_one_all_company_id_list(one_res=one_res)

                    self.lg.info('one_all_company_id_list num: {}'.format(len(one_all_company_id_list)))
                    await self._crawl_hn_one_type_all_company_info(
                        one_all_company_id_list=one_all_company_id_list)
                    collect()

                # 重置
                new_tasks_params_list = []

                # break
                collect()

        return None

    async def _crawl_hn_one_type_all_company_info(self, one_all_company_id_list):
        """
        抓取hn 单个keyword所有的company info
        :param one_all_company_id_list:
        :return:
        """
        async def _get_tasks_params_list(one_all_company_id_list) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for item in one_all_company_id_list:
                company_id = item['company_id']
                if 'hn' + company_id not in self.db_hn_unique_id_list:
                    tasks_params_list.append({
                        'company_id': company_id,
                        'province_name': item['province_name'],
                        'city_name': item['city_name'],
                        'w3': item['w3'],
                    })
                else:
                    pass

            tasks_params_list = list_remove_repeat_dict_plus(
                target=tasks_params_list,
                repeat_key='company_id')

            return tasks_params_list

        async def _get_one_res(slice_params_list) -> list:
            """获取one_res"""
            tasks = []
            for k in slice_params_list:
                # self.lg.info(str(k))
                company_id = k['company_id']
                w3 = k['w3']
                if 'hn' + company_id in self.db_hn_unique_id_list:
                    self.lg.info('company_id: {} in db, so pass!'.format(company_id))
                    continue

                self.lg.info('create task[where company_id: {}]'.format(company_id))
                company_url = 'http://{}.huoniuniu.com/shop/{}'.format(w3, company_id)
                tasks.append(self.loop.create_task(self._parse_one_company_info(
                    short_name='hn',
                    company_id=company_id,
                    province_name=k['province_name'],
                    city_name=k['city_name'],
                    company_url=company_url)))

            one_res = await async_wait_tasks_finished(tasks=tasks)

            return one_res

        # 对应company_id 采集该分类截止页面的所有company info
        tasks_params_list = await _get_tasks_params_list(one_all_company_id_list=one_all_company_id_list)
        # new_step = self.concurrency
        new_step = 30
        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=new_step)

        index = 0
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            # asyncio
            one_res = await _get_one_res(slice_params_list=slice_params_list)
            kill_process_by_name('phantomjs')
            kill_process_by_name('firefox')

            # 存储
            index, self.db_hn_unique_id_list = await self._save_company_one_res(
                one_res=one_res,
                short_name='hn',
                db_unique_id_list=self.db_hn_unique_id_list,
                index=index,)

            # await async_sleep(3.)

        return None

    async def _get_hn_one_type_company_id_list(self, keyword, page_num, province_name, city_name, city_base_url, shop_item_selector, shop_id_selector, w3_selector, timeout=15,):
        """
        获取hn 某关键字的单页company_info
        :param keyword:
        :param page_num:
        :param province_name:
        :param city_name:
        :param city_base_url:
        :param shop_item_selector:
        :param shop_id_selector:
        :param timeout:
        :return: [{'company_id': xxx, 'province_name': '', 'city_name': '', 'w3': 'xxx'}, ...]
        """
        try:
            w3 = await async_parse_field(
                parser=w3_selector,
                target_obj=city_base_url,
                logger=self.lg,)
            assert w3 != '', 'w3为空值!'
        except AssertionError:
            self.lg.error('遇到错误:', exc_info=True)
            return []

        headers = await self._get_pc_headers()
        headers.update({
            'Proxy-Connection': 'keep-alive',
        })
        params = (
            ('q', str(keyword)),
            ('sourcePage', '/'),
            ('page_no', str(page_num)),
        )
        # url = 'http://gz.huoniuniu.com/goods'
        url = city_base_url + '/goods'
        # body = await unblock_request(
        #     url=url,
        #     headers=headers,
        #     params=params,
        #     num_retries=self.hn_max_num_retries,
        #     ip_pool_type=self.ip_pool_type,
        #     timeout=timeout,
        #     logger=self.lg)

        # requests成功率低, 改用driver
        # new_url = _get_url_contain_params(url=url, params=params)
        new_url = url + '?' + urlencode(tuple_or_list_params_2_dict_params(params))
        body = await unblock_request_by_driver(
            url=new_url,
            type=PHANTOMJS,
            executable_path=self.driver_path,
            logger=self.lg,
            ip_pool_type=self.ip_pool_type,
            timeout=25,)
        # self.lg.info(body)

        shop_item_list = await async_parse_field(
            parser=shop_item_selector,
            target_obj=body,
            is_first=False,
            logger=self.lg,)
        # pprint(shop_item_list)

        shop_id_list = []
        for item in shop_item_list:
            try:
                company_id = await async_parse_field(
                    parser=shop_id_selector,
                    target_obj=item,
                    is_first=True,
                    logger=self.lg)
                assert company_id != '', 'company_id不为空值!'
                shop_id_list.append({
                    'company_id': company_id,
                    'province_name': province_name,
                    'city_name': city_name,
                    'w3': w3,
                })
            except AssertionError:
                continue
        shop_id_list = list_remove_repeat_dict_plus(
            target=shop_id_list,
            repeat_key='company_id',)
        # pprint(shop_id_list)
        self.lg.info('[{}] keyword: {}, page_num: {}, province_name: {}, city_name: {}'.format(
            '+' if shop_id_list != [] else '-',
            keyword,
            page_num,
            province_name,
            city_name,
        ))

        return shop_id_list

    async def _get_hn_new_hn_city_info_list(self) -> list:
        """
        得到hn对应省份, city信息
        :return:
        """
        # pprint(self.hn_city_info_list)    # [('广州站', 'http://gz.huoniuniu.com'), ...]
        _ = [
            {
                'province_name': '广东省',
                'city_name': '广州市',
                'city_base_url': 'http://gz.huoniuniu.com',
            },
            {
                'province_name': '广东省',
                'city_name': '普宁市',
                'city_base_url': 'http://pn.huoniuniu.com',
            },
            {
                'province_name': '河北省',
                'city_name': '保定市',
                'city_base_url': 'http://bd.huoniuniu.com',
            },
            {
                'province_name': '广东省',
                'area': '新塘',
                'city_name': '广州市',
                'city_base_url': 'http://xt.huoniuniu.com',
            },
            {
                'province_name': '湖南省',
                'city_name': '郴州市',
                'city_base_url': 'http://cz.huoniuniu.com',
            },
            {
                'province_name': '浙江省',
                'city_name': '杭州市',
                'city_base_url': 'http://hz.huoniuniu.com',
            },
            {
                'province_name': '福建省',
                'city_name': '泉州市',
                'city_base_url': 'http://qz.huoniuniu.com',
            },
            {
                'province_name': '广东省',
                'area': '花都',
                'city_name': '广州市',
                'city_base_url': 'http://hd.huoniuniu.com',
            },
            {
                'province_name': '湖南省',
                'city_name': '株洲市',
                'city_base_url': 'http://zz.huoniuniu.com',
            },
            {
                'province_name': '河南省',
                'city_name': '郑州市',
                'city_base_url': 'http://zez.huoniuniu.com',
            },
        ]

        return _

    async def _yw_spider(self):
        """
        义乌购spider(pc站)
        :return:
        """
        self.db_yw_unique_id_list = await self._get_db_unique_id_list_by_site_id(site_id=8)
        self.yw_category_list = await self._get_yw_category()

        pprint(self.yw_category_list)
        self.lg.info('yw所有子分类总个数: {}'.format(len(self.yw_category_list)))
        assert self.yw_category_list != [], '获取到的self.yw_category_list为空list!异常退出'

        await self._crawl_yw_company_info()

    async def _get_yw_category(self) -> list:
        """
        获取yw所有子分类
        :return: [{'cate_id': xx, 'cate_name': xx}, ...]
        """
        async def _get_yw_main_cate_info_list(cate_name, type_name_parser, type_url_parser) -> list:
            """获取yw主分类的cate info"""
            headers = await self._get_phone_headers()
            headers.update({
                'Connection': 'keep-alive',
            })
            url = 'http://wap.yiwugo.com/categories'
            body = await unblock_request(
                url=url,
                headers=headers,
                ip_pool_type=self.ip_pool_type,
                logger=self.lg,
                num_retries=self.yw_max_num_retries,)
            # self.lg.info(body)
            m_child_cate_name_list = await async_parse_field(
                parser=type_name_parser,
                target_obj=body,
                is_first=False,
                logger=self.lg)
            m_child_cate_url_list = await async_parse_field(
                parser=type_url_parser,
                target_obj=body,
                is_first=False,
                logger=self.lg)
            child_cate_info_list = list(zip(m_child_cate_name_list, m_child_cate_url_list))
            # pprint(child_cate_info_list)
            self.lg.info('[{}] cate_name: {}'.format('+' if child_cate_info_list != [] else '-', cate_name))

            return child_cate_info_list

        async def _get_tasks_params_list(cate_info_list) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for i in cate_info_list:
                tasks_params_list.append({
                    'cate_name': i[0],
                    'cate_id': i[1],
                })

            return tasks_params_list

        async def _get_yw_one_cate_info_list(cate_name, cate_id) -> list:
            """获取yw m站单个页面分类的cate info"""
            headers = await self._get_phone_headers()
            headers.update({
                'Referer': 'http://wap.yiwugo.com/categories',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive',
            })
            params = (
                ('uppertype', str(cate_id)),
            )
            url = 'http://wap.yiwugo.com/categories'
            body = await unblock_request(
                url=url,
                headers=headers,
                params=params,
                ip_pool_type=self.ip_pool_type,
                logger=self.lg,
                num_retries=self.yw_max_num_retries,)
            data = json_2_dict(
                json_str=body,
                logger=self.lg,
                default_res=[]
            )
            data = [{
                'cate_id': item.get('id', ''),
                'cate_name': item.get('type', ''),
            } for item in data]
            self.lg.info('[{}] cate_name: {}, cate_id: {}'.format(
                '+' if data != [] else '-',
                cate_name,
                cate_id))

            return data

        async def _get_one_res(slice_params_list) -> list:
            tasks = []
            for k in slice_params_list:
                cate_name = k['cate_name']
                cate_id = k['cate_id']
                self.lg.info('create task[where cate_name: {}, cate_id: {}]'.format(cate_name, cate_id))
                tasks.append(self.loop.create_task(_get_yw_one_cate_info_list(
                    cate_name=cate_name,
                    cate_id=cate_id,
                )))

            one_res = await async_wait_tasks_finished(tasks=tasks)
            # pprint(one_res)

            return one_res

        parser_obj = await self._get_parser_obj(short_name='yw')
        # 获取父分类
        all_main_cate_info_list = await _get_yw_main_cate_info_list(
            cate_name='main cate type',
            type_name_parser=parser_obj['trade_type_info']['type_name_sub'],
            type_url_parser=parser_obj['trade_type_info']['type_url_sub'],)
        self.lg.info('获取main cate num: {}'.format(len(all_main_cate_info_list)))

        # 获取父分类的子分类
        tasks_params_list = await _get_tasks_params_list(cate_info_list=all_main_cate_info_list)
        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=self.concurrency)
        all_sub_cate_info_list = []
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            one_res = await _get_one_res(slice_params_list=slice_params_list)
            for i in one_res:
                for j in i:
                    all_sub_cate_info_list.append(j)
        # pprint(all_sub_cate_info_list)
        self.lg.info('获取到的父分类的子分类总个数: {}'.format(len(all_sub_cate_info_list)))

        all_yw_child_cate_info_list = all_sub_cate_info_list

        return all_yw_child_cate_info_list

    async def _crawl_yw_company_info(self) -> None:
        """
        采集yw所有的company信息
        :return:
        """
        async def _get_tasks_params_list(cate_name) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for page_num in range(1, self.yw_max_page_num + 1):
                tasks_params_list.append({
                    'keyword': cate_name,
                    'page_num': page_num,
                })

            return tasks_params_list

        async def _get_one_res(slice_params_list) -> list:
            """获取one_res"""
            async def _create_one_celery_task(**kwargs):
                ip_pool_type = kwargs['ip_pool_type']
                keyword = kwargs['keyword']
                page_num = kwargs['page_num']

                async_obj = _get_yw_one_type_company_id_list_task.apply_async(
                    args=[
                        ip_pool_type,
                        keyword,
                        page_num,
                    ],
                    expires=3.5 * 60,
                    retry=False,
                )

                return async_obj

            tasks = []
            for k in slice_params_list:
                keyword = k['keyword']
                page_num = k['page_num']
                self.lg.info('create task[where keyword: {}, page_num: {}]...'.format(keyword, page_num))
                # tasks.append(self.loop.create_task(self._get_yw_one_type_company_id_list(
                #     keyword=keyword,
                #     page_num=page_num,)))

                try:
                    async_obj = await _create_one_celery_task(
                        ip_pool_type=self.ip_pool_type,
                        keyword=keyword,
                        page_num=page_num,
                    )
                    tasks.append(async_obj)
                except:
                    continue

            # asyncio
            # one_res = await async_wait_tasks_finished(tasks=tasks)
            # celery
            one_res = await _get_celery_async_results(tasks=tasks)

            return one_res

        async def _get_one_all_company_id_list(one_res) -> list:
            """获取该子分类截止页面的所有company_id_list"""
            one_all_company_id_list = []
            tmp_id_list = []
            for i in one_res:
                try:
                    for j in i:
                        # self.lg.info(str(j))
                        company_id = j.get('company_id', '')
                        if 'yw' + company_id not in self.db_yw_unique_id_list:
                            if company_id not in tmp_id_list:
                                one_all_company_id_list.append({
                                    'company_id': company_id,
                                    'province_name': '',
                                    'city_name': '',
                                })
                                tmp_id_list.append(company_id)
                except TypeError:
                    self.lg.error('遇到错误:', exc_info=True)
                    return []

            return one_all_company_id_list

        self.lg.info('即将开始采集yw shop info...')
        new_concurrency = 300
        new_tasks_params_list = []
        for cate_name_item_index, cate_name_item in enumerate(self.yw_category_list):
            cate_name = cate_name_item['cate_name']
            self.lg.info('crawl cate_name: {}, cate_name_item_index: {} ...'.format(cate_name, cate_name_item_index))
            tasks_params_list = await _get_tasks_params_list(cate_name=cate_name)
            try:
                new_tasks_params_list = await self._get_new_tasks_params_list_from_tasks_params_list(
                    tasks_params_list=tasks_params_list,
                    new_concurrency=new_concurrency,
                    new_tasks_params_list=new_tasks_params_list)
            except AssertionError:
                continue

            tasks_params_list_obj = TasksParamsListObj(tasks_params_list=new_tasks_params_list, step=self.concurrency)
            while True:
                try:
                    slice_params_list = tasks_params_list_obj.__next__()
                except AssertionError:
                    break

                one_res = await _get_one_res(slice_params_list=slice_params_list)
                # pprint(one_res)
                one_all_company_id_list = await _get_one_all_company_id_list(one_res=one_res)
                self.lg.info('one_all_company_id_list num: {}'.format(len(one_all_company_id_list)))

                await self._crawl_yw_one_type_all_company_info(
                    one_all_company_id_list=one_all_company_id_list)

            # 重置
            new_tasks_params_list = []

            # break
            # await async_sleep(1.5)
            collect()

        return None

    async def _crawl_yw_one_type_all_company_info(self, one_all_company_id_list):
        """
        抓取yw单个分类所有的company_info
        :param one_all_company_id_list: [{'company_id': xxx, 'province_name': xxx, 'city_name': xxx}, ...]
        :return:
        """
        async def _get_tasks_params_list(one_all_company_id_list) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for item in one_all_company_id_list:
                company_id = item['company_id']
                if 'yw' + company_id not in self.db_yw_unique_id_list:
                    tasks_params_list.append({
                        'company_id': company_id,
                        'province_name': item['province_name'],
                        'city_name': item['city_name'],
                    })
                else:
                    pass

            # 去重
            tasks_params_list = list_remove_repeat_dict_plus(
                target=tasks_params_list,
                repeat_key='company_id')

            return tasks_params_list

        async def _get_one_res(slice_params_list) -> list:
            """获取one_res"""
            tasks = []
            for k in slice_params_list:
                company_id = k['company_id']
                if 'yw' + company_id in self.db_yw_unique_id_list:
                    self.lg.info('company_id: {} in db, so pass!'.format(company_id))
                    continue

                self.lg.info('create task[where company_id: {}]'.format(company_id))
                company_url = 'http://www.yiwugo.com/hu/{}.html'.format(company_id)
                tasks.append(self.loop.create_task(self._parse_one_company_info(
                    short_name='yw',
                    company_id=company_id,
                    province_name=k['province_name'],
                    city_name=k['city_name'],
                    company_url=company_url)))

            one_res = await async_wait_tasks_finished(tasks=tasks)

            return one_res

        # 对应company_id 采集该分类截止页面的所有company info
        tasks_params_list = await _get_tasks_params_list(one_all_company_id_list=one_all_company_id_list)
        # now_step = self.concurrency
        # when driver get html
        now_step = 20
        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=now_step)

        index = 0
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            # asyncio
            one_res = await _get_one_res(slice_params_list=slice_params_list)
            kill_process_by_name('phantomjs')
            kill_process_by_name('firefox')

            # 存储
            index, self.db_yw_unique_id_list = await self._save_company_one_res(
                one_res=one_res,
                short_name='yw',
                db_unique_id_list=self.db_yw_unique_id_list,
                index=index,)

            # await async_sleep(3.)

        return None

    async def _ic_spider(self):
        """
        中国制造网spider(m站)
        :return:
        """
        self.db_ic_unique_id_list = await self._get_db_unique_id_list_by_site_id(site_id=7)
        self.ic_category_list = await self._get_ic_category()

        pprint(self.ic_category_list)
        self.lg.info('ic所有子分类总个数: {}'.format(len(self.ic_category_list)))
        assert self.ic_category_list != [], '获取到的self.ic_category_list为空list!异常退出'

        await self._crawl_ic_company_info()

    async def _get_ic_category(self) -> list:
        """
        获取ic所有子分类
        :return:
        """
        async def _get_ic_one_cate_info_list(cate_name, cate_url, type_name_parser, type_url_parser) -> list:
            """获取ic m站单个页面分类的cate info"""
            async def _get_ic_m_cate_url_list(cate_url_list) -> list:
                """给ic的cate url加上父域名"""
                return ['https://3g.made-in-china.com' + item for item in cate_url_list]

            # TODO 测试发现: 其子分类下面的页面并非根据页码增长, 故采集m站的分类, 其是有规律的
            body = await unblock_request(
                url=cate_url,
                headers=await self._get_phone_headers(),
                ip_pool_type=self.ip_pool_type,
                logger=self.lg,)
            m_child_cate_name_list = await async_parse_field(
                parser=type_name_parser,
                target_obj=body,
                is_first=False,
                logger=self.lg)
            m_child_cate_url_list = await async_parse_field(
                parser=type_url_parser,
                target_obj=body,
                is_first=False,
                logger=self.lg)
            m_child_cate_url_list = await _get_ic_m_cate_url_list(m_child_cate_url_list)
            child_cate_info_list = list(zip(m_child_cate_name_list, m_child_cate_url_list))
            # pprint(child_cate_info_list)
            self.lg.info('[{}] cate_name: {}'.format('+' if child_cate_info_list != [] else '-', cate_name))

            return child_cate_info_list

        async def _get_tasks_params_list(cate_info_list) -> list:
            """获取sub的子分类的任务参数"""
            tasks_params_list = []
            for i in cate_info_list:
                tasks_params_list.append({
                    'cate_name': i[0],
                    'cate_url': i[1],
                })

            return tasks_params_list

        async def _get_one_res(slice_params_list, parser_obj):
            tasks = []
            for k in slice_params_list:
                cate_name = k['cate_name']
                cate_url = k['cate_url']
                self.lg.info('create task[where cate_name: {}, cate_url: {}]'.format(cate_name, cate_url))
                tasks.append(self.loop.create_task(_get_ic_one_cate_info_list(
                    cate_name=cate_name,
                    cate_url=cate_url,
                    type_name_parser=parser_obj['trade_type_info']['type_name_third'],
                    type_url_parser=parser_obj['trade_type_info']['type_url_third'],
                )))

            one_res = await async_wait_tasks_finished(tasks=tasks)
            # pprint(one_res)

            return one_res

        parser_obj = await self._get_parser_obj(short_name='ic')
        # 获取父分类
        self.lg.info('getting sub cate info...')
        all_sub_cate_info_list = await _get_ic_one_cate_info_list(
            cate_name='sub',
            cate_url='https://3g.made-in-china.com/catalog/',
            type_name_parser=parser_obj['trade_type_info']['type_name_sub'],
            type_url_parser=parser_obj['trade_type_info']['type_url_sub'],)
        self.lg.info('获取sub cate num: {}'.format(len(all_sub_cate_info_list)))

        # 获取父分类的子分类
        tasks_params_list = await _get_tasks_params_list(cate_info_list=all_sub_cate_info_list)
        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=self.concurrency)
        all_third_cate_info_list = []
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            one_res = await _get_one_res(slice_params_list=slice_params_list, parser_obj=parser_obj)
            for i in one_res:
                for j in i:
                    all_third_cate_info_list.append(j)
        # pprint(all_third_cate_info_list)
        self.lg.info('获取到的父分类的子分类总个数: {}'.format(len(all_third_cate_info_list)))

        # 获取子分类的子分类
        all_ic_child_cate_info_list = all_third_cate_info_list

        return all_ic_child_cate_info_list

    async def _crawl_ic_company_info(self):
        """
        采集ic所有company信息
        :return:
        """
        async def _get_tasks_params_list(cate_url):
            """获取tasks_params_list"""
            tasks_params_list = []

            for page_num in range(1, self.ic_max_page_num + 1):
                tasks_params_list.append({
                    'cate_url': cate_url,
                    'page_num': str(page_num),
                })

            return tasks_params_list

        async def _get_one_res(slice_params_list) -> list:
            """获取one_res"""
            tasks = []
            for k in slice_params_list:
                cate_url = k['cate_url']
                page_num = k['page_num']
                self.lg.info('create task[where page_num: {}, cate_url: {}]'.format(page_num, cate_url))
                tasks.append(self.loop.create_task(self._get_ic_one_type_company_id_list(
                    cate_url=cate_url,
                    page_num=page_num,
                    parser_obj=parser_obj,
                )))

            one_res = await async_wait_tasks_finished(tasks=tasks)

            return one_res

        async def _get_one_ic_company_id_list(one_res) -> list:
            """获取ic 单页待采集的company_id list"""
            one_all_company_id_list = []
            tmp_id_list = []
            for i in one_res:
                try:
                    for j in i:
                        company_id = j.get('company_id', '')
                        if 'ic' + company_id not in self.db_ic_unique_id_list:
                            if company_id not in tmp_id_list:
                                one_all_company_id_list.append({
                                    'company_id': company_id,
                                })
                                tmp_id_list.append(company_id)
                except TypeError:
                    return []

            return one_all_company_id_list

        self.lg.info('即将开始采集ic shop info...')
        parser_obj = await self._get_parser_obj(short_name='ic')
        for item_index, item in enumerate(self.ic_category_list):
            cate_name = item[0]
            cate_url = item[1]
            self.lg.info('crawl cate_name: {}, item_index: {} ...'.format(cate_name, item_index))

            tasks_params_list = await _get_tasks_params_list(cate_url=cate_url)
            tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=self.concurrency)
            while True:
                try:
                    slice_params_list = tasks_params_list_obj.__next__()
                except AssertionError:
                    break

                one_res = await _get_one_res(slice_params_list=slice_params_list)
                one_all_company_id_list = await _get_one_ic_company_id_list(one_res=one_res)
                # pprint(one_all_company_id_list)

                self.lg.info('one_all_company_id_list num: {}'.format(len(one_all_company_id_list)))
                await self._crawl_ic_one_type_all_company_info(
                    one_all_company_id_list=one_all_company_id_list)

            collect()
            # break

        return None

    async def _get_ic_one_type_company_id_list(self, **kwargs) -> list:
        """
        获取ic 单个分类的company_id list
        :return:
        """
        # 某个cate的第一页的url
        cate_url = kwargs['cate_url']
        page_num = kwargs['page_num']
        parser_obj = kwargs['parser_obj']

        # 筛选出cate_id
        cate_id_selector = {
            'method': 're',
            'selector': '\/product\/(\d+)-.*?',
        }
        cate_id = await async_parse_field(
            parser=cate_id_selector,
            target_obj=cate_url,
            logger=self.lg,)
        if cate_id == '':
            self.lg.info('获取到的cate_id为空!')
            return []

        url = 'https://3g.made-in-china.com/product/{}-{}.html'.format(cate_id, page_num)
        body = await unblock_request(
            url=url,
            headers=await self._get_phone_headers(),
            ip_pool_type=self.ip_pool_type,
            logger=self.lg,)
        # self.lg.info(body)

        company_url_list = await async_parse_field(
            parser=parser_obj['trade_type_info']['one_type_url_list'],
            target_obj=body,
            is_first=False,
            logger=self.lg,)

        company_id_selector = {
            'method': 're',
            'selector': '\/gongying\/(\w+)-.*?',
        }
        company_id_list = []
        for item in company_url_list:
            try:
                company_id = await async_parse_field(
                    parser=company_id_selector,
                    target_obj=item,
                    logger=self.lg,)
                assert company_id != '', 'company_id为空值!'
            except AssertionError:
                continue

            company_id_list.append({
                'company_id': company_id,
            })

        company_id_list = list_remove_repeat_dict_plus(target=company_id_list, repeat_key='company_id')
        self.lg.info('[{}] cate_id: {}, page_num: {}'.format(
            '+' if company_id_list != [] else '-',
            cate_id,
            page_num))

        return company_id_list

    async def _crawl_ic_one_type_all_company_info(self, one_all_company_id_list) -> None:
        """
        抓取ic 单个分类对应的所有company_id 的info
        :param one_all_company_id_list:
        :return:
        """
        async def _get_tasks_params_list(one_all_company_id_list) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for item in one_all_company_id_list:
                company_id = item['company_id']
                if 'ic' + company_id not in self.db_ic_unique_id_list:
                    tasks_params_list.append({
                        'company_id': company_id,
                        'province_name': '',
                        'city_name': '',
                    })
                else:
                    pass

            # 去重
            tasks_params_list = list_remove_repeat_dict_plus(
                target=tasks_params_list,
                repeat_key='company_id')

            return tasks_params_list

        async def _get_one_res(slice_params_list) -> list:
            """获取slice_params_list"""
            tasks = []
            for k in slice_params_list:
                company_id = k['company_id']
                if 'ic' + company_id in self.db_ic_unique_id_list:
                    self.lg.info('company_id: {} in db, so pass!'.format(company_id))
                    continue

                self.lg.info('create task[where company_id: {}]'.format(company_id))
                company_url = 'https://3g.made-in-china.com/company-{}/'.format(company_id)
                tasks.append(self.loop.create_task(self._parse_one_company_info(
                    short_name='ic',
                    company_id=company_id,
                    province_name=k['province_name'],
                    city_name=k['city_name'],
                    company_url=company_url)))

            one_res = await async_wait_tasks_finished(tasks=tasks)

            return one_res

        self.lg.info('即将开始采集 ic company info...')
        tasks_params_list = await _get_tasks_params_list(one_all_company_id_list=one_all_company_id_list)
        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=self.concurrency)

        index = 0
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            one_res = await _get_one_res(
                slice_params_list=slice_params_list,)

            # 存储
            index, self.db_ic_unique_id_list = await self._save_company_one_res(
                one_res=one_res,
                short_name='ic',
                db_unique_id_list=self.db_ic_unique_id_list,
                index=index,)
            collect()

        return None

    async def _a114_spider(self):
        """
        114批发市场spider(pc)
        :return:
        """
        self.db_114_unique_id_list = await self._get_db_unique_id_list_by_site_id(site_id=6)
        # 测试发现这个cate_num是有规律的 1-10000
        # self.a114_category_list = await self._get_114_category()
        self.a114_category_list = list(range(1, 15000+1))[58:]

        pprint(self.a114_category_list)
        self.lg.info('114所有子分类总个数: {}'.format(len(self.a114_category_list)))
        assert self.a114_category_list != [], '获取到的self.a114_category_list为空list!异常退出'

        await self._crawl_114_company_info()

    async def _get_114_category(self) -> list:
        """
        得到114的所有子分类信息
        :return:
        """
        async def _get_home_page() -> list:
            """
            得到主页的大分类
            :return: ['c-1.html', ...]
            """
            url = 'http://www.114pifa.com/'
            body = await unblock_request_by_driver(
                url=url,
                executable_path=PHANTOMJS_DRIVER_PATH,
                ip_pool_type=self.ip_pool_type,
                logger=self.lg,
                timeout=20,)
            assert body != '', '_get_home_page中的body为空值!'

            type_url_sub_list = await async_parse_field(
                parser=parser_obj['trade_type_info']['type_url_sub'],
                target_obj=body,
                is_first=False,
                logger=self.lg)

            res = []
            for item in type_url_sub_list:
                try:
                    cate_number = int(await async_parse_field(
                        parser=parser_obj['trade_type_info']['type_url_number'],
                        target_obj=item,
                        logger=self.lg))
                    if cate_number not in res:
                        res.append(cate_number)
                except ValueError:
                    continue

            res.sort()

            return res

        parser_obj = await self._get_parser_obj(short_name='114')
        try:
            home_categroy_list = await _get_home_page()
            pprint(home_categroy_list)
            await async_sleep(.5)
            self.lg.info('home_categroy_list len: {}个!'.format(len(home_categroy_list)))
            all_sub_categroy = await self._crawl_114_sub_categroy(home_categroy_list=home_categroy_list)
        except AssertionError:
            self.lg.error('遇到错误:', exc_info=True)
            return []

        return all_sub_categroy

    async def _crawl_114_sub_categroy(self, home_categroy_list) -> list:
        """
        采集114的各大分类的对应的子分类
        :return: [1, 3, ...]
        """
        async def _get_tasks_params_list() -> list:
            """获取tasks_params_list"""
            tasks_params_list = []

            for item in home_categroy_list:
                try:
                    if item not in tasks_params_list:
                        tasks_params_list.append({
                            'category_number': str(item),
                        })
                except AssertionError:
                    continue

            return tasks_params_list

        async def _get_all_cate_number(all) -> list:
            """获取去所有cate_number"""
            res = []
            # pprint(all)
            for cate_url in all:
                if isinstance(cate_url, str):
                    try:
                        _ = await async_parse_field(
                            parser=parser_obj['trade_type_info']['type_url_number'],
                            target_obj=cate_url,
                            logger=self.lg)
                        cate_num = int(_)
                    except ValueError:
                        continue
                elif isinstance(cate_url, int):
                    cate_num = cate_url

                else:
                    continue

                res.append(cate_num)

            res.sort()

            return res

        self.lg.info('start crawl 各个home_categroy_list的item的子分类...')
        parser_obj = await self._get_parser_obj(short_name='114')
        tasks_params_list = await _get_tasks_params_list()
        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=self.concurrency)

        # 不保留原先的因为其搜索页面为空, 即搜索不到company_info信息
        all = home_categroy_list
        # all = []
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            tasks = []
            for k in slice_params_list:
                category_number = k['category_number']
                self.lg.info('create task[where category_number: {}]...'.format(category_number))
                tasks.append(self.loop.create_task(self._get_114_one_page_third_category_list(
                    parser_obj=parser_obj['trade_type_info'],
                    category_number=category_number,)))

                # 用于测试
                # break

            one_res = await async_wait_tasks_finished(tasks=tasks)
            # kill_process_by_name(process_name='phantomjs')

            for i in one_res:
                for j in i:
                    if j not in all:
                        all.append(j)

        self.lg.info('crawl 各个home_categroy_list的item的子分类 over !')
        res = await _get_all_cate_number(all=all)

        return res

    async def _get_114_one_page_third_category_list(self, **kwargs) -> list:
        """
        获取114单页大分类页面中的所有子分类
        :return:
        """
        parser_obj = kwargs['parser_obj']
        category_number = kwargs['category_number']

        headers = await self._get_pc_headers()
        headers.update({
            'Proxy-Connection': 'keep-alive',
        })
        url = 'http://www.114pifa.com/c-{}.html'.format(category_number)
        # driver并发直接提示请求过于频繁
        # body = await unblock_request_by_driver(
        #     url=url,
        #     type=PHANTOMJS,
        #     executable_path=PHANTOMJS_DRIVER_PATH,
        #     logger=self.lg,
        #     ip_pool_type=self.ip_pool_type,
        #     timeout=20)

        body = await unblock_request(
            url=url,
            headers=headers,
            cookies=None,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.a114_max_num_retries,
            encoding='gbk',)

        if re.compile(r'<title>错误: 不能获取请求的 URL</title>').findall(body) != []\
                or re.compile(r'<title>403 Forbidden</title>').findall(body) != []:
            # 单独处理此种请求, 以提高业务成功率
            body = await unblock_request(
                url=url,
                headers=headers,
                cookies=None,
                ip_pool_type=self.ip_pool_type,
                num_retries=int(self.a114_max_num_retries/2),
                encoding='gbk',)

        # self.lg.info(body)
        if body == '':
            self.lg.error('url: {} 获取到的body为空值!'.format(url))
            return []

        type_url_sub_list = await async_parse_field(
            parser=parser_obj['type_url_third'],
            target_obj=body,
            is_first=False,
            logger=self.lg)
        # pprint(type_url_sub_list)
        # if type_url_sub_list == []:
        #     self.lg.info(body)

        self.lg.info('[{}] category_number: {}'.format('+' if type_url_sub_list != [] else '-', category_number))

        return type_url_sub_list

    async def _crawl_114_company_info(self):
        """
        采集114所有company信息
        :return:
        """
        async def _get_tasks_params_list(cate_num) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []

            for page_num in range(2, self.a114_max_page_num + 1):
                tasks_params_list.append({
                    'cate_num': cate_num,
                    'page_num': str(page_num),
                })

            # 单独插入第一个
            tasks_params_list.insert(0, {
                'cate_num': cate_num,
                'page_num': '',
            })

            return tasks_params_list

        async def _get_one_all_company_id_list(one_res) -> list:
            """获取待采集的company_id list"""
            one_all_company_id_list = []
            tmp_id_list = []
            for i in one_res:
                try:
                    for j in i:
                        company_id = j.get('company_id', '')
                        if '114' + company_id not in self.db_114_unique_id_list:
                            if company_id not in tmp_id_list:
                                one_all_company_id_list.append({
                                    'company_id': company_id,
                                })
                                tmp_id_list.append(company_id)
                except TypeError:
                    return []

            return one_all_company_id_list

        async def _get_one_res(slice_params_list) -> list:
            """获取one_res"""
            async def _create_one_celery_task(**kwargs):
                ip_pool_type = kwargs['ip_pool_type']
                num_retries = kwargs['num_retries']
                parser_obj = kwargs['parser_obj']
                cate_num = kwargs['cate_num']
                page_num = kwargs['page_num']

                async_obj = _get_114_one_type_company_id_list_task.apply_async(
                    args=[
                        ip_pool_type,
                        num_retries,
                        parser_obj,
                        cate_num,
                        page_num,
                    ],
                    expires=5 * 60,
                    retry=False, )

                return async_obj

            tasks = []
            for k in slice_params_list:
                cate_num = k['cate_num']
                page_num = k['page_num']
                self.lg.info('create task[where cate_num: {}, page_num: {}]...'.format(cate_num, page_num))
                # tasks.append(self.loop.create_task(self._get_114_one_type_company_id_list(
                #     parser_obj=parser_obj['trade_type_info'],
                #     cate_num=cate_num,
                #     page_num=page_num,)))

                try:
                    async_obj = await _create_one_celery_task(
                        ip_pool_type=self.ip_pool_type,
                        num_retries=self.a114_max_num_retries,
                        parser_obj=parser_obj['trade_type_info'],
                        cate_num=cate_num,
                        page_num=page_num,)
                    tasks.append(async_obj)
                except:
                    continue

            # asyncio
            # one_res = await async_wait_tasks_finished(tasks=tasks)
            # celery
            one_res = await _get_celery_async_results(tasks=tasks)
            # pprint(one_res)

            return one_res

        self.lg.info('即将开始采集114 shop info...')
        parser_obj = await self._get_parser_obj(short_name='114')

        # 测试(发现很多cate_num都是无效无数据的, 只有部分有数据, eg: 1048有数据)
        # self.a114_category_list = ['1048', '1049', '1050', '1051', '1052', '1053']
        UN_CRAWL_CATE_NUM_LIST = list(range(1, 57)) + [64, 65, 100, 200, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 275, 276, 277, 400, 500, 600, 900, 1000,]
        new_concurrency = 300
        new_tasks_params_list = []
        for cate_num_index, cate_num in enumerate(self.a114_category_list):
            try:
                if int(cate_num) in UN_CRAWL_CATE_NUM_LIST:
                    # 跳过一些无数据的cate_num
                    continue
            except:
                pass

            self.lg.info('crawl cate_num: {}, cate_num_index: {} ...'.format(cate_num, cate_num_index))
            tasks_params_list = await _get_tasks_params_list(cate_num=cate_num)
            try:
                new_tasks_params_list = await self._get_new_tasks_params_list_from_tasks_params_list(
                    tasks_params_list=tasks_params_list,
                    new_concurrency=new_concurrency,
                    new_tasks_params_list=new_tasks_params_list)
            except AssertionError:
                continue

            tasks_params_list_obj = TasksParamsListObj(tasks_params_list=new_tasks_params_list, step=self.concurrency)
            while True:
                try:
                    slice_params_list = tasks_params_list_obj.__next__()
                except AssertionError:
                    break

                one_res = await _get_one_res(slice_params_list=slice_params_list)
                one_all_company_id_list = await _get_one_all_company_id_list(one_res=one_res)

                self.lg.info('one_all_company_id_list num: {}'.format(len(one_all_company_id_list)))
                await self._crawl_114_one_type_all_company_info(
                    one_all_company_id_list=one_all_company_id_list)

            # 重置
            new_tasks_params_list = []
            collect()

        return None

    async def _get_new_tasks_params_list_from_tasks_params_list(self, tasks_params_list, new_tasks_params_list, new_concurrency) -> list:
        """
        从tasks_params_list中获取新的new_tasks_params_list(# 新建任务个数在达标后才启动)
        :return:
        """
        for l in tasks_params_list:
            new_tasks_params_list.append(l)

        if len(new_tasks_params_list) < new_concurrency:
            raise AssertionError('未达标跳过!')

        else:
            self.lg.info('建立base task len: {}个 达标!'.format(len(new_tasks_params_list)))

        return new_tasks_params_list

    async def _get_114_one_type_company_id_list(self, **kwargs) -> list:
        """
        获取114单个子分类的单个页面所有的公司简介的url(m站, pc站无列表显示)
        :param kwargs:
        :return: [{'company_id': 'xxx'}, ...]
        """
        parser_obj = kwargs['parser_obj']
        cate_num = kwargs['cate_num']       # int
        page_num = kwargs['page_num']       # str '' | '2', ...

        headers = await self._get_phone_headers()
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
        body = await unblock_request(
            url=url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.a114_max_num_retries,
            encoding='gbk')
        # self.lg.info(body)

        brief_url_list = await async_parse_field(
            parser=parser_obj['one_type_url_list'],
            target_obj=body,
            is_first=False,
            logger=self.lg)
        # pprint(brief_url_list)

        company_id_list = []
        for item in brief_url_list:
            try:
                company_id = await async_parse_field(
                    parser=parser_obj['one_type_url_list_item'],
                    target_obj=item,
                    logger=self.lg)
                assert company_id != '', 'company_id不为空值!'
            except AssertionError:
                continue
            company_id_list.append({
                'company_id': company_id,
            })

        company_id_list = list_remove_repeat_dict_plus(target=company_id_list, repeat_key='company_id')
        self.lg.info('[{}] url: {}'.format('+' if company_id_list != [] else '-', url))

        return company_id_list

    async def _crawl_114_one_type_all_company_info(self, one_all_company_id_list):
        """
        抓取114单个分类的所有company_info
        :param one_all_company_id_list: [{'company_id': xxx}, ...]
        :return:
        """
        async def _get_tasks_params_list(one_all_company_id_list) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for item in one_all_company_id_list:
                company_id = item['company_id']
                if '114' + company_id not in self.db_114_unique_id_list:
                    tasks_params_list.append({
                        'company_id': company_id,
                        'province_name': '',
                        'city_name': '',
                    })
                else:
                    pass

            # 去重
            tasks_params_list = list_remove_repeat_dict_plus(
                target=tasks_params_list,
                repeat_key='company_id')

            return tasks_params_list

        async def _get_one_res(slice_params_list,) -> list:
            tasks = []
            for k in slice_params_list:
                company_id = k['company_id']
                if '114' + company_id in self.db_114_unique_id_list:
                    self.lg.info('company_id: {} in db, so pass!'.format(company_id))
                    continue

                self.lg.info('create task[where company_id: {}]'.format(company_id))
                company_url = 'http://www.114pifa.com/ca/{}'.format(company_id)
                tasks.append(self.loop.create_task(self._parse_one_company_info(
                    short_name='114',
                    company_id=company_id,
                    province_name=k['province_name'],
                    city_name=k['city_name'],
                    company_url=company_url)))

                # try:
                #     async_obj = await self._create_one_celery_task_where_is_parse_one_company_info_task(
                #         short_name='114',
                #         company_id=company_id,
                #         province_name=k['province_name'],
                #         city_name=k['city_name'],
                #         company_url=company_url,
                #         type_code='',)
                #     tasks.append(async_obj)
                # except:
                #     continue

            # asyncio
            one_res = await async_wait_tasks_finished(tasks=tasks)
            # celery
            # one_res = await _get_celery_async_results(tasks=tasks)

            return one_res

        async def _get_one_res_by_celery(slice_params_list) -> list:
            """
            通过celery
            :param slice_params_list:
            :return:
            """
            async def _create_one_celery_task(**kwargs):
                company_id = kwargs['company_id']

                async_obj = _get_114_company_page_html_task.apply_async(
                    args=[
                        company_id,
                        self.ip_pool_type,
                        self.a114_max_num_retries,
                    ],
                    expires=5*60,
                    retry=False,)

                return async_obj

            # 获取company_id对应的company_html
            tasks = []
            for k in slice_params_list:
                company_id = k['company_id']
                if '114' + company_id in self.db_114_unique_id_list:
                    self.lg.info('company_id: {} in db, so pass!'.format(company_id))
                    continue

                self.lg.info('create task[where status: get 114 company_html, company_id: {}]'.format(company_id))
                try:
                    async_obj = await _create_one_celery_task(company_id=company_id,)
                    tasks.append(async_obj)
                except:
                    continue
            # celery
            one_res = await _get_celery_async_results(tasks=tasks)

            # parse company_info
            tasks = []
            for k in one_res:
                # k:(company_id, company_html)
                try:
                    company_id = k[0]
                    company_html = k[1]
                    if not isinstance(company_html, str):
                        continue

                    self.lg.info('create task[where status: parse_114_company_html, company_id: {}]'.format(company_id))
                    company_url = 'http://www.114pifa.com/ca/{}'.format(company_id)
                    tasks.append(self.loop.create_task(self._parse_one_company_info(
                        short_name='114',
                        company_id=company_id,
                        province_name='',
                        city_name='',
                        company_url=company_url,
                        company_html=company_html,)))
                except (TypeError, IndexError):
                    continue

            self.lg.info('parse 114 company_html ing...')
            one_res = await async_wait_tasks_finished(tasks=tasks)

            return one_res

        self.lg.info('即将开始采集 114 company info...')
        # 对应company_id 采集该分类截止页面的所有company info
        tasks_params_list = await _get_tasks_params_list(one_all_company_id_list=one_all_company_id_list)
        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=self.concurrency)

        index = 0
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            # asyncio
            # one_res = await _get_one_res(
            #     slice_params_list=slice_params_list,)
            # celery
            one_res = await _get_one_res_by_celery(
                slice_params_list=slice_params_list,)

            # 存储
            index, self.db_114_unique_id_list = await self._save_company_one_res(
                one_res=one_res,
                short_name='114',
                db_unique_id_list=self.db_114_unique_id_list,
                index=index,)

        return None

    async def _create_one_celery_task_where_is_parse_one_company_info_task(self, **kwargs):
        """
        创建一个parse_one_company_info_task的celery 任务
        :param kwargs:
        :return:
        """
        short_name = kwargs['short_name']
        company_id = kwargs['company_id']
        province_name = kwargs['province_name']
        city_name = kwargs['city_name']
        company_url = kwargs['company_url']
        type_code = kwargs['type_code']

        async_obj = _parse_one_company_info_task.apply_async(
            args=[
                short_name,
                company_url,
                province_name,
                city_name,
                company_id,
                type_code,
            ],
            expires=5 * 60,
            retry=False,)

        return async_obj

    async def _al_spider(self):
        """
        1688商家spider
        :return:
        """
        self.db_al_unique_id_list = await self._get_db_unique_id_list_by_site_id(site_id=5)
        # self.al_category_list = await self._get_al_category()
        # self.al_category_list = await self._get_al_category2()
        # self.al_category_list = await self._get_al_category3()
        # self.al_category_list = await self._get_al_category4()
        # self.al_category_list = await self._get_al_category5()
        # 读取最新的热搜goods词
        self.al_category_list = (await self._get_al_category6())
        # self.al_category_list = await self._get_al_category7()

        pprint(self.al_category_list)
        self.lg.info('al所有子分类总个数: {}'.format(len(self.al_category_list)))
        assert self.al_category_list != [], '获取到的self.al_category_list为空list!异常退出'

        await self._crawl_al_company_info()

    async def _get_al_category(self) -> list:
        """
        分类信息
        :return:
        """
        async def _get_tasks_params_list() -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for index_cate_id in range(self.al_min_index_cate_id, self.al_max_index_cate_id + 1):
                tasks_params_list.append({
                    'index_cate_id': index_cate_id,
                })

            return tasks_params_list

        self.lg.info('正在获取1688分类信息中...')
        tasks_params_list = await _get_tasks_params_list()
        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=self.concurrency)

        all_cate_type_name = []
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            tasks = []
            for k in slice_params_list:
                index_cate_id = k['index_cate_id']
                self.lg.info('create task[where index_cate_id is {}]...'.format(index_cate_id))
                tasks.append(self.loop.create_task(self._get_al_one_cate_list(
                    index_cate_id=index_cate_id,
                )))

            one_res = await async_wait_tasks_finished(tasks=tasks)
            for i in one_res:
                for j in i:
                    if j not in all_cate_type_name:
                        all_cate_type_name.append(j)

        # 逆序
        all_cate_type_name.reverse()

        return all_cate_type_name

    async def _get_al_category2(self) -> list:
        """
        从db拿keyword
        :return:
        """
        sql_str = '''select top 100000 keyword from dbo.goods_keywords'''
        _ = []
        self.lg.info('正在获取db中keyword for al_category_list...')
        try:
            _ = self.sql_server_cli._select_table(sql_str=sql_str, params=None)
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)

        assert _ != [], '_为空list!'
        self.lg.info('获取db的keyword成功!')

        al_category_list = []
        for i in _:
            try:
                al_category_list.append(i[0])
            except:
                return []

        al_category_list.reverse()

        return al_category_list[2413:]

    async def _get_al_category3(self) -> list:
        """
        从jd总分类拿到keyword
        :return:
        """
        headers = await self._get_pc_headers()
        headers.update({
            'authority': 'www.jd.com',
        })
        url = 'https://www.jd.com/allSort.aspx'
        body = await unblock_request(
            url=url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            logger=self.lg)
        li_selector = {
            'method': 'css',
            'selector': 'dl.clearfix dd a ::text',
        }
        li_list = await async_parse_field(
            parser=li_selector,
            target_obj=body,
            is_first=False,
            logger=self.lg)
        li_list = list_duplicate_remove(li_list)

        return li_list

    async def _get_al_category4(self):
        """
        得到所有汉字
        :return:
        """
        async def _get_one_page(page_num):
            """获取一页"""
            url = 'https://www.qqxiuzi.cn/zh/hanzi/daquan-{}.htm'.format(page_num)
            body = await unblock_request(
                url=url,
                headers=await self._get_pc_headers(),
                encoding='gbk',
                ip_pool_type=self.ip_pool_type)
            # self.lg.info(body)

            one = []
            try:
                one = (Selector(text=body).css('tr:nth-child(2) td p ::text').extract_first() or '') \
                    .split(' ')
            except Exception:
                pass
            self.lg.info('[{}] page_num: {}, chinese_char_num: {}'.format('+' if one != [] else '-', page_num, len(one)))

            return one

        self.lg.info('正在获取所有中文汉字...')
        all = []
        for page_num in range(1, 5):
            one = await _get_one_page(page_num=page_num)
            for i in one:
                if i not in all:
                    all.append(i)

        all = delete_list_null_str(all)
        # self.lg.info(all)
        self.lg.info('总汉字个数: {}'.format(len(all)))

        return all[10712:]

    async def _get_al_category5(self) -> list:
        """
        tb 总分类
        :return: ['鞋子', ...]
        """
        async def oo(target_list, all_sort_list) -> list:
            for i in target_list:
                name = i.get('name', '')
                if name not in all_sort_list:
                    all_sort_list.append(name)

            return all_sort_list

        headers = await self._get_pc_headers()
        headers.update({
            'Referer': 'https://www.taobao.com/',
        })
        params = (
            ('ids', '222887,222890,222889,222886,222906,222898,222907,222885,222895,222878,222908,222879,222893,222896,222918,222917,222888,222902,222880,222913,222910,222882,222883,222921,222899,222905,222881,222911,222894,222920,222914,222877,222919,222915,222922,222884,222912,222892,222900,222923,222909,222897,222891,222903,222901,222904,222916,222924'),
            ('callback', 'tbh_service_cat'),
        )
        url = 'https://tce.alicdn.com/api/data.htm'
        body = await unblock_request(
            url=url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            logger=self.lg)
        all_sort_list = []
        try:
            data = json_2_dict(
                json_str=re.compile('\((.*)\)').findall(body)[0],
                default_res={},
                logger=self.lg)
            assert data != {}, 'data为空dict!'
            # pprint(data)

            for value in data.values():
                head = value.get('value', {}).get('head', [])
                _list = value.get('value', {}).get('list', [])
                all_sort_list = await oo(target_list=head, all_sort_list=all_sort_list)
                all_sort_list = await oo(target_list=_list, all_sort_list=all_sort_list)

        except AssertionError:
            self.lg.error('遇到错误:', exc_info=True)
            return []

        return all_sort_list

    async def _get_al_category6(self) -> list:
        """
        读取最新的淘热搜excel的top 20W关键字
        :return:
        """
        async def _get_tasks_params_list() -> list:
            tasks_params_list = []
            for item in walk(self.tb_20w_path):
                dir_path, dir_names, file_names = item
                for file_name in file_names:
                    new_excel_file_path = '{}/{}'.format(dir_path, file_name)
                    tasks_params_list.append(new_excel_file_path)

            return tasks_params_list

        async def get_one_res(slice_params_list) -> list:
            tasks = []
            for k in slice_params_list:
                excel_file_path = k
                self.lg.info('create task[where excel_file_path: {}] ...'.format(excel_file_path))
                tasks.append(self.loop.create_task(self.read_excel_file(excel_file_path)))

            one_res = await async_wait_tasks_finished(tasks=tasks)

            return one_res

        tb_hot_keywords_file_path = '/Users/afa/myFiles/tmp/tb_hot_keywords.txt'
        # 存储最后返回的keywords list
        all_key_list = []
        # TODO 如果要更新tb_hot_keywords.txt里面的值, 直接在路径下删除该文件即可!
        if path_exists(tb_hot_keywords_file_path):
            self.lg.info('[+] 存在{}, reading ...'.format(tb_hot_keywords_file_path))
            # 存在则直接读取!
            with open(tb_hot_keywords_file_path, 'r',) as f:
                for line in f:
                    all_key_list.append(line.replace('\n', ''))

        else:
            self.lg.info('[-] 不存在{}, creating ...'.format(tb_hot_keywords_file_path))
            # 创建tb_hot_keywords_file_path, 并写入内容
            all_res = []
            all_new_excel_file_path_list = await _get_tasks_params_list()
            # 同步读取...(同步读取, 不容易导致mac卡住! 故异步需控制并发量!)
            # for index, excel_file_path in enumerate(all_new_excel_file_path_list):
            #     self.lg.info('read excel_file index: {}'.format(index))
            #     all_res.append(await self.read_excel_file(
            #         excel_file_path=excel_file_path))

            # 异步读取..
            # 并发量=5, 性能较好! 不易卡住!
            # 5时挂在 2018.4.26.xlsx 第30个!
            step = 5
            tasks_params_list = TasksParamsListObj(
                tasks_params_list=all_new_excel_file_path_list,
                step=step,)
            slice_index = 1
            while True:
                try:
                    slice_params_list = tasks_params_list.__next__()
                except AssertionError:
                    break

                self.lg.info('-> slice_index: {}, step: {}'.format(slice_index, step))
                one_res = await get_one_res(slice_params_list)
                for i in one_res:
                    all_res.append(i)

                # 回收两次让其进入分代回收的第三代
                try:
                    del one_res
                except:
                    pass
                try:
                    del one_res
                except:
                    pass
                collect()
                slice_index += 1

            # 保持原先读取顺序进行拼接
            self.lg.info('按原先读取顺序进行拼接ing...')
            all_new_excel_res = []
            for i in all_new_excel_file_path_list:
                for item in all_res:
                    excel_file_path, new_excel_res = item
                    if i == excel_file_path:
                        self.lg.info('add {} to all_new_excel_res ...'.format(excel_file_path))
                        all_new_excel_res += new_excel_res
                        break
                    else:
                        continue

            try:
                del all_res
            except:
                pass
            collect()

            # 处理新关键字 list
            new_key_list = await self.jieba_handle_excel_res(excel_result=all_new_excel_res)

            all_key_list = []
            for item in new_key_list:
                if item not in all_key_list:
                    self.lg.info('add {}'.format(item))
                    all_key_list.append(item)

            try:
                del all_new_excel_res
                del new_key_list
            except:
                pass
            collect()

            # * 不再进行写入, 保证这个文件一直不存在!!
            # self.lg.info('writing keywords to {} ...'.format(tb_hot_keywords_file_path))
            # with open(tb_hot_keywords_file_path, 'w',) as f:
            #     for item in all_key_list:
            #         print('-> add {} to txt'.format(item))
            #         f.write(item + '\n')

        collect()

        return all_key_list

    async def jieba_handle_excel_res(self, excel_result:list) -> list:
        """
        关键字进行结巴分词处理
        :return:
        """
        self.lg.info('开始处理excel数据...')
        new_sql_add_index = 0
        excel_result_len = len(excel_result)
        try:
            bloom_filter = BloomFilter(capacity=excel_result_len + 1, error_rate=1/excel_result_len*100)
        except ZeroDivisionError:
            self.lg.error('遇到错误:', exc_info=True)
            return []

        all_key_list = []
        for item in excel_result:
            keyword = item.get('关键词', None)
            if not keyword:
                continue

            # 不进行原数据接入(原因太具体很多搜索不到), jieba分词存入
            try:
                for seq in jieba_cut(sentence=keyword, cut_all=False):
                    # 精准模式先拆分原句
                    seq = seq.lower()
                    if ' ' == seq:
                        continue
                    if seq not in bloom_filter:
                        self.lg.info('{}, add {}'.format(new_sql_add_index, seq))
                        all_key_list.append(seq)
                        bloom_filter.add(seq)
                        new_sql_add_index += 1
            except Exception:
                self.lg.error('遇到错误', exc_info=True)
                continue

        try:
            del excel_result
        except:
            pass
        try:
            del bloom_filter
        except:
            pass
        collect()

        return all_key_list

    async def read_excel_file(self, excel_file_path) -> tuple:
        """
        读取excel file
        :return:
        """
        excel_result = []
        try:
            excel_result = await async_read_info_from_excel_file(excel_file_path=excel_file_path)
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)

        self.lg.info('[{}] 读取excel_file: {}!'.format(
            '+' if excel_result != [] else '-',
            excel_file_path))

        return excel_file_path, excel_result

    async def _get_al_category7(self) -> list:
        """
        获取常用英文单词
        :return:
        """
        async def _get_and_parse(page_num) -> list:
            """获取并且解析"""
            url = 'http://www.youdict.com/ciku/id_0_0_0_0_{}.html'.format(page_num)
            # 使用proxy, 无数据
            body = await unblock_request(url=url, headers=headers, cookies=None, use_proxy=False)

            li_selector = {
                'method': 'css',
                'selector': 'h3 a ::text',
            }
            word = await async_parse_field(
                parser=li_selector,
                target_obj=body,
                is_first=False,
                logger=self.lg)
            self.lg.info('[{}] page_num: {}'.format('+' if word != [] else '-', page_num))

            return word

        headers = await self._get_phone_headers()
        headers.update({
            'Proxy-Connection': 'keep-alive',
            # 'Referer': 'http://www.youdict.com/ciku/id_0_0_0_0_2238.html',
        })
        tasks = []
        all = []
        for page_num in range(0, 2239):
            self.lg.info('create task[where page_num is {}]...'.format(page_num))
            tasks.append(self.loop.create_task(_get_and_parse(page_num=page_num)))

        all_res = await async_wait_tasks_finished(tasks=tasks)
        for i in all_res:
            for j in i:
                if j not in all:
                    all.append(j)
        pprint(all)
        self.lg.info('all len: {}'.format(len(all)))
        collect()

        return all

    async def _get_al_one_cate_list(self, index_cate_id:int=0) -> list:
        """
        得到1688某个父分类中所有子分类的cate_list
        :param index_cate_id: 0-16 父分类id
        :return: ['毛鞋子', ...]
        """
        async def _get_one_body(sub_cate_id='') -> str:
            """获取一个cate的body"""
            # 总分类: https://m.1688.com/page/cateList.html
            headers = await self._get_phone_headers()
            headers.update({
                'authority': 'm.1688.com',
            })
            params = (
                ('indexCateId', str(index_cate_id)),
                ('subCateId', str(sub_cate_id)),
            )
            url = 'https://m.1688.com/page/cateList/subCate.html'
            body = await unblock_request(
                url=url,
                headers=headers,
                params=params,
                ip_pool_type=self.ip_pool_type,
                logger=self.lg)
            # self.lg.info(body)

            return body

        async def _get_sub_cate_id_list() -> list:
            """获取第二类子分类id list"""
            tmp_sub_cate_id_list = await async_parse_field(
                parser=parser_obj['trade_type_info']['type_name_sub'],
                target_obj=body1,
                logger=self.lg,
                is_first=False,)
            sub_cate_id_list = []
            for i in tmp_sub_cate_id_list:
                try:
                    sub_cate_id_list.append(re.compile('subCateId=(\d+)').findall(i)[0])
                except IndexError:
                    pass

            return sub_cate_id_list

        body1 = await _get_one_body()
        parser_obj = await self._get_parser_obj(short_name='al')
        sub_cate_id_list = await _get_sub_cate_id_list()
        if sub_cate_id_list == []:
            self.lg.error('获取到的sub_cate_id_list为空list!异常退出!出错index_cate_id:{}'.format(index_cate_id))
            self.lg.info('[{}] index_cate_id: {}'.format('-', index_cate_id))
            return []

        all_cate_name_list = []
        if len(sub_cate_id_list) > 1:
            # 处理多个子分类
            for sub_cate_id in sub_cate_id_list:
                self.lg.info('Get index_cate_id: {}, sub_cate_id: {}...'.format(index_cate_id, sub_cate_id))
                body2 = await _get_one_body(sub_cate_id)
                cate_name_list = await async_parse_field(
                    parser=parser_obj['trade_type_info']['type_name_third'],
                    target_obj=body2,
                    logger=self.lg,
                    is_first=False,)
                for i in cate_name_list:
                    if i not in all_cate_name_list:
                        all_cate_name_list.append(i)
        else:
            all_cate_name_list = await async_parse_field(
                parser=parser_obj['trade_type_info']['type_name_third'],
                target_obj=body1,
                logger=self.lg,
                is_first=False,)

        self.lg.info('[{}] index_cate_id: {}'.format('+' if all_cate_name_list != [] else '-', index_cate_id))

        return all_cate_name_list

    async def _crawl_al_company_info(self):
        """
        采集al所有商铺信息
        :return:
        """
        async def _get_tasks_params_list(cate_name) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for page_num in range(1, self.al_max_page_num + 1):
                tasks_params_list.append({
                    'keyword': cate_name,
                    'page_num': page_num,
                })

            return tasks_params_list

        async def _get_one_all_company_id_list(one_res) -> list:
            """获取该子分类截止页面的所有company_id_list"""
            one_all_company_id_list = []
            get_current_func_info_by_traceback(self=self, logger=self.lg)
            for i in one_res:
                try:
                    for j in i:
                        company_id = j.get('company_id', '')
                        # if 'al' + company_id not in self.db_al_unique_id_list:
                        if 'al' + company_id not in self.bloom_filter:
                            # 原生判重太慢, 改用bloom算法判重
                            one_all_company_id_list.append({
                                'company_id': company_id,
                                'province_name': j['province_name'],
                                'city_name': j['city_name'],
                            })
                except TypeError:
                    return []

            one_all_company_id_list = list_remove_repeat_dict_plus(
                target=one_all_company_id_list,
                repeat_key='company_id',)

            return one_all_company_id_list

        async def _get_one_res(slice_params_list) -> list:
            """获取one_res"""
            async def _create_one_celery_task(**kwargs):
                ip_pool_type = kwargs['ip_pool_type']
                keyword = kwargs['keyword']
                page_num = kwargs['page_num']

                async_obj = _get_al_one_type_company_id_list_task.apply_async(
                    args=[
                        ip_pool_type,
                        keyword,
                        page_num,
                    ],
                    expires=3 * 60,
                    retry=False,
                )

                return async_obj

            tasks = []
            for k in slice_params_list:
                keyword = k['keyword']
                page_num = k['page_num']
                self.lg.info('create task[where keyword: {}, page_num: {}]...'.format(keyword, page_num))
                try:
                    async_obj = await _create_one_celery_task(
                        ip_pool_type=self.ip_pool_type,
                        # logger=self.lg,
                        keyword=keyword,
                        page_num=page_num,
                    )
                    tasks.append(async_obj)
                except:
                    continue

            # celery
            one_res = await _get_celery_async_results(tasks=tasks)
            try:
                del tasks
            except:
                pass

            return one_res

        self.lg.info('即将开始采集al shop info...')
        new_concurrency = 1000
        new_tasks_params_list = []
        # 存储成功被遍历的cate_name
        tmp_cate_name_list = []
        for cate_name_index, cate_name in enumerate(self.al_category_list):
            if cate_name in self.tb_jb_boom_filter:
                # 去除已遍历的过的hot key
                self.lg.info('hot key: {} in self.tb_jb_boom_filter'.format(cate_name))
                continue

            self.lg.info('crawl cate_name: {}, cate_name_index: {} ...'.format(cate_name, cate_name_index))
            tmp_cate_name_list.append(cate_name)
            tasks_params_list = await _get_tasks_params_list(cate_name=cate_name)
            try:
                new_tasks_params_list = await self._get_new_tasks_params_list_from_tasks_params_list(
                    tasks_params_list=tasks_params_list,
                    new_concurrency=new_concurrency,
                    new_tasks_params_list=new_tasks_params_list)
            except AssertionError:
                continue

            # new_concurrency2 = self.concurrency
            # 达标后设置并发量为1000个, 设置过大, 无数据!!
            new_concurrency2 = 1000
            tasks_params_list_obj = TasksParamsListObj(
                tasks_params_list=new_tasks_params_list,
                step=new_concurrency2)
            while True:
                try:
                    slice_params_list = tasks_params_list_obj.__next__()
                except AssertionError:
                    break

                one_res = await _get_one_res(slice_params_list=slice_params_list)
                # pprint(one_res)
                one_all_company_id_list = await _get_one_all_company_id_list(one_res=one_res)
                try:
                    del one_res
                except:
                    pass

                self.lg.info('one_all_company_id_list num: {}'.format(len(one_all_company_id_list)))
                await self._crawl_al_one_type_all_company_info(
                    one_all_company_id_list=one_all_company_id_list)
                try:
                    del one_all_company_id_list
                except:
                    pass

            # 写入txt and tb_jb_boom_filter
            await self._write_tb_jb_hot_keyword_txt(target_list=tmp_cate_name_list)
            await self._add_to_tb_jb_boom_filter(target_list=tmp_cate_name_list)

            # 重置
            new_tasks_params_list = []
            tmp_cate_name_list = []

            # break
            collect()

    async def _write_tb_jb_hot_keyword_txt(self, target_list) -> None:
        """
        写入tb_jb_hot_keyword.txt
        :param target_list:
        :return:
        """
        target_list = list(set(target_list))
        with open(self.tb_jb_hot_keyword_file_path, 'a+') as f:
            for item in target_list:
                f.write(item + '\n')
                self.lg.info('write hot key: {}'.format(item))

        return None

    async def _add_to_tb_jb_boom_filter(self, target_list) -> None:
        """
        写入self.tb_jb_boom_filter
        :param target_list:
        :return:
        """
        target_list = list(set(target_list))
        for item in target_list:
            if item not in self.tb_jb_boom_filter:
                self.tb_jb_boom_filter.add(item)

        return None

    async def _crawl_al_one_type_all_company_info(self, one_all_company_id_list):
        """
        抓取al单个分类的所有company info
        :param one_all_company_id_list:
        :return:
        """
        async def _get_tasks_params_list(one_all_company_id_list) -> list:
            """获取tasks_params_list"""
            get_current_func_info_by_traceback(self=self, logger=self.lg)
            tasks_params_list = []
            for item in one_all_company_id_list:
                company_id = item['company_id']
                # if 'al' + company_id not in self.db_al_unique_id_list:
                if 'al' + company_id not in self.bloom_filter:
                    tasks_params_list.append({
                        'company_id': company_id,
                        'province_name': item['province_name'],
                        'city_name': item['city_name'],
                    })
                else:
                    pass

            # 去重
            tasks_params_list = list_remove_repeat_dict_plus(
                target=tasks_params_list,
                repeat_key='company_id')

            return tasks_params_list

        async def _create_one_celery_task(**kwargs):
            ip_pool_type = kwargs['ip_pool_type']
            company_id = kwargs['company_id']
            province_name = kwargs['province_name']
            city_name = kwargs['city_name']

            async_obj = _get_al_company_page_html_task.apply_async(
                args=[
                    ip_pool_type,
                    company_id,
                    province_name,
                    city_name,
                ],
                expires=5 * 60,
                retry=False,)

            return async_obj

        async def _get_one_res(slice_params_list) -> list:
            """获取one_res"""
            get_current_func_info_by_traceback(self=self, logger=self.lg)
            tasks = []

            # asyncio
            # for k in slice_params_list:
            #     company_id = k['company_id']
            #     self.lg.info('create task[where company_id: {}]'.format(company_id))
            #     company_url = 'https://m.1688.com/winport/company/{}.html'.format(company_id)
            #     tasks.append(self.loop.create_task(self._parse_one_company_info(
            #         short_name='al',
            #         company_id=company_id,
            #         province_name=k['province_name'],
            #         city_name=k['city_name'],
            #         company_url=company_url)))
            #
            # one_res = await async_wait_tasks_finished(tasks=tasks)

            # 通过celery
            for k in slice_params_list:
                company_id = k['company_id']
                self.lg.info('create task[where company_id: {}]'.format(company_id))
                try:
                    async_obj = await _create_one_celery_task(
                        ip_pool_type=self.ip_pool_type,
                        company_id=company_id,
                        province_name=k['province_name'],
                        city_name=k['city_name'],)
                    tasks.append(async_obj)
                except Exception:
                    self.lg.error('遇到错误:', exc_info=True)
                    continue
            celery_one_res = await _get_celery_async_results(tasks=tasks)
            # pprint(celery_one_res)

            tasks = []
            for p in celery_one_res:
                try:
                    company_id, company_html, province_name, city_name = p
                    self.lg.info('create task[where company_id: {}]'.format(company_id))
                    company_url = 'https://m.1688.com/winport/company/{}.html'.format(company_id)
                    tasks.append(self.loop.create_task(self._parse_one_company_info(
                        short_name='al',
                        company_id=company_id,
                        province_name=province_name,
                        city_name=city_name,
                        company_url=company_url,
                        company_html=company_html)))
                except Exception:
                    continue
            one_res = await async_wait_tasks_finished(tasks=tasks)
            try:
                del tasks
            except:
                pass

            return one_res

        get_current_func_info_by_traceback(self=self, logger=self.lg)
        # 对应company_id 采集该分类截止页面的所有company info
        tasks_params_list = await _get_tasks_params_list(one_all_company_id_list=one_all_company_id_list)
        # new_concurrency = self.concurrency
        new_concurrency = 500
        tasks_params_list_obj = TasksParamsListObj(
            tasks_params_list=tasks_params_list,
            step=new_concurrency)

        index = 0
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            # asyncio
            one_res = await _get_one_res(slice_params_list=slice_params_list)

            # 存储
            index, self.db_al_unique_id_list = await self._save_company_one_res(
                one_res=one_res,
                short_name='al',
                db_unique_id_list=self.db_al_unique_id_list,
                index=index,)
            try:
                del one_res
            except:
                pass
            collect()

        return None

    async def _save_company_one_res(self, one_res:list, short_name, db_unique_id_list:list, index:int):
        """
        存储company的one_res
        :param short_name: eg: 'al', '114'
        :param db_unique_id: eg: self.db_al_unique_id_list
        :param index:
        :return: (index, db_unique_id)
        """
        for i in one_res:
            index += 1
            if i != {}:
                tmp_unique_id = i.get('unique_id', '')
                if re.compile('^{}'.format(short_name)).findall(tmp_unique_id) != []:
                    # 处理已加头部的
                    unique_id = tmp_unique_id
                else:
                    unique_id = short_name + tmp_unique_id

                if unique_id in db_unique_id_list:
                    # 已在db的不存储
                    self.lg.info('company_id:{} in db, so pass!'.format(i.get('unique_id', '')))
                    continue

                save_res = await self._save_company_item(
                    company_item=i,
                    index=index,)
                if save_res:
                    # 成功插入的记录
                    if unique_id not in db_unique_id_list:
                        db_unique_id_list.append(unique_id)
                    else:
                        pass
                    if unique_id not in self.bloom_filter:
                        self.bloom_filter.add(unique_id)
                    else:
                        pass
                else:
                    pass
            else:
                pass

        try:
            del one_res
        except:
            pass

        return index, db_unique_id_list

    async def _mt_spider(self):
        """
        mtspider
        :return:
        """
        self.db_mt_unique_id_list = await self._get_db_unique_id_list_by_site_id(site_id=4)
        self.category_list = await self._get_category()
        pprint(self.category_list)
        assert self.category_list != [], '获取到的self.category_list为空list!异常退出'

        # 待抓取的城市名
        self.mt_city_name_list = await self._get_mt_all_city_name_list()
        assert self.mt_city_name_list != [], '获取到的self.mt_city_list为空list'

        await self._crawl_mt_company_info()

    async def _crawl_mt_company_info(self, **kwargs) -> None:
        """
        抓取mt公司信息
        :param kwargs:
        :return:
        """
        async def _get_tasks_params_list(cid, cate_type, one_type_name) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            PAGE_RANGE = range(1, self.mt_max_page_num+1) if one_type_name != '全部' else range(1, 300+1)
            for page_num in PAGE_RANGE:
                tasks_params_list.append({
                    'cid': cid,
                    'cate_type': cate_type,
                    'page_num': page_num,
                })

            return tasks_params_list

        for city_name in self.mt_city_name_list:
            for cid_index, item in enumerate(self.category_list):
                cid, cate_type = item['cid'], item['cate_type']
                one_type_name = item['one_type_name']
                if cid == '' or cate_type == '':
                    # 无值则跳过
                    continue

                tasks_params_list = await _get_tasks_params_list(cid=cid, cate_type=cate_type, one_type_name=one_type_name)
                tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=self.concurrency)

                while True:
                    try:
                        slice_params_list = tasks_params_list_obj.__next__()
                    except AssertionError:
                        break

                    tasks = []
                    # cookies = await self._get_mt_cookies_dict()
                    # if cookies == {}:
                    #     continue
                    for k in slice_params_list:
                        page_num = k['page_num']
                        self.lg.info('create task[where city_name:{}, page_num:{}, cid_index:{}]...'.format(city_name, page_num, cid_index))
                        tasks.append(self.loop.create_task(self._crawl_mt_someone_city_someone_type_one_page_info(
                            city_name=city_name,
                            page_num=page_num,
                            cid=k['cid'],
                            cate_type=k['cate_type'],
                            cookies='')))

                    one_res = await async_wait_tasks_finished(tasks=tasks)
                    # 避免内存泄漏, 主动释放
                    kill_process_by_name(process_name='firefox')
                    kill_process_by_name(process_name='phantomjs')
                    new_res = []
                    for i in one_res:
                        for j in i:
                            # pprint(j)
                            new_res.append(j)

                    self.lg.info('开始采集city_name:{}, cid:{}, 对应的商铺信息...'.format(city_name, cid))
                    await self._crawl_mt_someone_city_some_cid_all_shop_info(
                        city_name=city_name,
                        shop_info_list=new_res)

            self.lg.info('city: {}, 采集完毕!休眠10s...')
            await async_sleep(10)

        return None

    async def _get_mt_cookies_dict(self, num_retries=6) -> dict:
        """
        获取mt主页cookies
        :return:
        """
        cookies = {}
        try:
            driver = BaseDriver(
                executable_path=self.driver_path,
                logger=self.lg,
                user_agent_type=PHONE,
                ip_pool_type=self.ip_pool_type,)
            cookies_str = driver.get_url_cookies_from_phantomjs_session(url='http://i.meituan.com')
            cookies = str_cookies_2_dict(cookies_str)
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
        finally:
            try:
                del driver
            except:
                pass
            collect()
            if num_retries < 0:
                pass
            else:
                if cookies == {}:
                    self.lg.info('{} try...'.format(6-(num_retries-1)))
                    return await self._get_mt_cookies_dict(num_retries=num_retries-1)
                else:
                    pass

            return cookies

    async def _crawl_mt_someone_city_someone_type_one_page_info(self, **kwargs) -> list:
        """
        抓取mt某城市的某个分类的单页信息
        :return:
        """
        async def _get_request_params() -> tuple:
            """请求参数"""
            nonlocal city_name
            return (
                ('cid', str(cid)),      # cid 为-1, 表示没有筛选分类, 1:美食 4:购物 20383:时尚购 20252:健身, 可以从全部分类中获取
                ('bid', '-1'),
                ('sid', 'defaults'),
                ('p', str(page_num)),
                ('ciid', await self._get_mt_ciid(city_name=city_name)),           # ciid是城市的对应id, 可以为空值
                ('bizType', 'area'),
                ('csp', ''),
                ('stid_b', '_b2'),
                ('cateType', 'poi'),    # 都设置为poi, 没有deal
                ('nocount', 'true'),
            )

        async def _parse(body) -> list:
            """解析"""
            parser_obj = await self._get_parser_obj(short_name='mt')
            shop_url_list = await async_parse_field(
                parser=parser_obj['shop_url'],
                target_obj=body,
                is_first=False,
                logger=self.lg)

            res = []
            for item in shop_url_list:
                try:
                    unique_id = await async_parse_field(
                        parser=parser_obj['unique_id'],
                        target_obj=item,
                        logger=self.lg)
                    assert unique_id != '', 'unique_id不为空值!'
                except AssertionError:
                    continue

                res.append({
                    'shop_url': item,
                    'unique_id': unique_id,
                    'cid': cid,
                })

            return res

        city_name = kwargs['city_name']
        cid = kwargs['cid']
        cate_type = kwargs['cate_type']
        page_num = kwargs['page_num']
        cookies = kwargs['cookies']

        city_name_pinyin:str = ''.join(lazy_pinyin(city_name))
        headers = await self._get_phone_headers()
        referer = 'http://i.meituan.com/{}/all/?cid={}&p={}&cateType=poi&stid_b=3'.format(
            city_name_pinyin,
            cid,
            page_num)
        headers.update({
            'Accept': 'text/html',
            'Referer': referer,
            'X-Requested-With': 'XMLHttpRequest',
            'Proxy-Connection': 'keep-alive',
        })
        params = await _get_request_params()
        url = 'http://i.meituan.com/select/{}/page_{}.html'.format(city_name_pinyin, page_num)
        # self.lg.info('分类的单页url:{}'.format(url))

        # 1. request
        # body = await unblock_request(
        #     url=url,
        #     headers=headers,
        #     params=params,
        #     cookies=cookies,
        #     ip_pool_type=self.ip_pool_type)
        # 处理跳转链接
        # dump_url = Selector(text=body).css('div.go-visit a.i-link ::attr("href")').extract_first() or ''
        # if dump_url != '':
        #     self.lg.info('跳转链接:{}, 重新请求中...'.format(dump_url))
        #     body = await unblock_request(url=dump_url, headers=headers, params=params, ip_pool_type=self.ip_pool_type)
        #     self.lg.info(body)

        # 2. requests_html
        # js_code = """
        # <script type="text/javascript" src="http://code.jquery.com/jquery-1.4.1.min.js"></script>
        # <script type="text/javascript">
        # //获取当前点击的对象
        #     $('.i-link').click(
        #         function() {
        #             console.log("当前URL为:", $(this).attr('href'));
        #         }
        #     );
        # </script>
        # """
        # body = await self.unblock_request_by_requests_html(url=url, headers=headers, params=params, js_code=js_code)
        # self.lg.info(body)

        # 3. selenium
        exec_code = """
        sleep(1)
        self.driver.find_element_by_class_name('i-link').click()
        sleep(4)
        """
        url = _get_url_contain_params(url, params)
        self.lg.info('分类的单页url:{}'.format(url))
        with await self.sema:
            # 不用点击的页面(即直接返回正确结果的)就当做异常抛出
            body = await unblock_request_by_driver(
                url=url,
                type=PHANTOMJS,
                executable_path=self.driver_path,
                logger=self.lg,
                headless=True,
                user_agent_type=PHONE,
                ip_pool_type=self.ip_pool_type,
                timeout=self.driver_timeout + 5,    # 设置成25保证更高的业务成功率
                exec_code=exec_code,)
            # self.lg.info(body)
            # if 'deal-container' not in body:
            #     self.lg.error('此次抓取未获取到需求信息! 出错url: {}'.format(url))
            #     return []

            res = await _parse(body=body)
            self.lg.info('[{}] city_name:{}, cid:{}, cate_type:{}, page_num:{}'.format(
                '+' if res != [] else '-',
                city_name,
                cid,
                cate_type,
                page_num,))

            return res

    async def unblock_request_by_requests_html(self, url, headers=None, params=None, cookies=None, js_code=None):
        """
        基于requests_html(>= python3.6)的异步非阻塞请求
        :return:
        """
        class PreparedRequest(object):
            def __init__(self, url, headers):
                self.url = url
                self.headers = headers

        with requests_html.AsyncHTMLSession(mock_browser=True) as s:
            proxies = Requests._get_proxies(ip_pool_type=self.ip_pool_type)
            prepared_request = PreparedRequest(url=url, headers=headers)
            s.rebuild_proxies(prepared_request=prepared_request, proxies=proxies)
            resp = await s.request(
                method='get',
                url=url,
                headers=headers,
                params=params,
                cookies=cookies,)

            if js_code is not None:
                resp.html.render(script=js_code)

            return resp.text

    async def _crawl_mt_someone_city_some_cid_all_shop_info(self, **kwargs) -> None:
        """
        采集mt某个城市的某个cid的全部商铺信息
        :return:
        """
        async def _get_tasks_params_list():
            """获取tasks_params_list"""
            nonlocal shop_info_list, city_name

            tasks_params_list = []
            for item in shop_info_list:
                unique_id = item['unique_id']
                if 'mt' + unique_id not in self.db_mt_unique_id_list:
                    tasks_params_list.append({
                        'company_url': item['shop_url'],
                        'company_id': unique_id,
                        'type_code': item['cid'],
                        'city_name': city_name,
                    })

            return tasks_params_list

        city_name = kwargs['city_name']
        shop_info_list = kwargs['shop_info_list']
        if shop_info_list == []:
            return None

        tasks_params_list = await _get_tasks_params_list()
        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=self.concurrency)

        index = 0
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            tasks = []
            for k in slice_params_list:
                company_id = k['company_id']
                company_url = k['company_url']
                type_code = k['type_code']      # 分类的cid

                if 'mt' + company_id in self.db_mt_unique_id_list:
                    self.lg.info('该company_id[{}]已存在于db中...跳过'.format('mt' + company_id))
                    continue

                self.lg.info('create task[where city_name:{}, company_id:{}]...'.format(city_name, company_id))
                tasks.append(self.loop.create_task(self._parse_one_company_info(
                    short_name='mt',
                    city_name=city_name,
                    company_id=company_id,
                    company_url=company_url,
                    type_code=type_code)))

            one_res = await async_wait_tasks_finished(tasks=tasks)

            fail_count = 0
            for i in one_res:
                index += 1
                if i != {}:
                    # pprint(i)
                    unique_id = i.get('unique_id', '')
                    res = await self._save_company_item(
                        company_item=i,
                        index=index)
                    self.mt_ocr_record_shop_id = unique_id
                    if res:
                        self.db_mt_unique_id_list.append(i['unique_id'])
                    else:
                        self.lg.info('该company_id[{}]已存在于db中...'.format(unique_id))
                else:
                    fail_count += 1

            await self._mt_crawl_exception_handler(
                fail_count=fail_count,
                one_res_len=len(one_res))
            try:
                await async_sleep(2.)
            except:
                pass

    async def _mt_crawl_exception_handler(self, **kwargs):
        """
        店铺信息抓取异常，认证处理
        :return:
        """
        fail_count: int = kwargs['fail_count']
        one_res_len: int = kwargs['one_res_len']

        if fail_count/one_res_len > 1/2:
            try:
                res = await async_send_msg_2_wx(sc_key=self.sc_key, title='美团认证提醒!', msg=get_uuid1())
                # 超时则异常退出!
                await wait_for(self._mt_robot_y(), timeout=10*60)
            except (AsyncTimeoutError, Exception):
                self.lg.error('遇到错误:', exc_info=True)
            finally:
                return None

    async def _mt_robot_y(self):
        # 打码接入
        # print('--->>> 动态打码中...')
        # print('初始化chrome...')
        # chrome_options = webdriver.ChromeOptions()
        # # chrome_options.add_argument('--user-agent={0}'.format(get_random_phone_ua()))
        #
        # driver = webdriver.Chrome(
        #     executable_path=CHROME_DRIVER_PATH,
        #     options=chrome_options
        # )
        # print('初始化完毕!')
        # try:
        #     driver.get('https://meishi.meituan.com/i/poi/{}'.format(self.mt_ocr_record_shop_id.replace('mt', '')))
        #     html = driver.page_source
        #     # print(html)
        #     if '验证中心' in html:
        #         # geckodriver 21.0 等待时间超过 5 秒，会提示 ConnectionResetError
        #         sleep(1)
        #         await self._get_mt_captcha_img(driver=driver)
        #
        #         res = await self._ocr_mt_captcha()
        #         while True:
        #             if '看不清' in res:
        #                 print('看不清, 重新点击验证码...')
        #                 driver.find_element_by_id('yodaNextImgCode').send_keys(Keys.ENTER)
        #                 sleep(1)
        #                 await self._get_mt_captcha_img(driver=driver)
        #             else:
        #                 break
        #
        #         print('输入中...')
        #         driver.find_element_by_css_selector('input#yodaImgCodeInput').send_keys(res)
        #
        #         sleep(2)
        #         # TODO 报错cannot read globalerror
        #         driver.find_element_by_id('yodaImgCodeSure').send_keys(Keys.ENTER)
        #     else:
        #         pass
        # except Exception as e:
        #     print(e)
        #
        # sleep(2 * 60)
        # try:
        #     driver.quit()
        # except:
        #     pass
        # collect()

        while True:
            a = input('请找个店铺地址进行mt的人工识别!(完成请输入y)')
            if a in ('Y', 'y'):
                self.mt_robot = False
                break

    async def _get_mt_captcha_img(self, driver) -> None:
        """
        截取验证码
        :return:
        """
        driver.save_screenshot('tmp_mt.png')
        captcha_css_selector = driver.find_element_by_css_selector('#yodaImgCode')
        location = captcha_css_selector.location
        size = captcha_css_selector.size
        print('location: {}, size: {}'.format(location, size))

        # 裁剪出验证码
        img1 = Image.open('tmp_mt.png')
        left = location['x']
        upper = location['y']
        right = left + size['width']
        lower = upper + size['height']

        box = (left, upper, right, lower)
        print('box:{}'.format(box))

        img2 = img1.crop(box)
        img2.save('mt_captcha.png')

        return

    async def _ocr_mt_captcha(self) -> str:
        """
        打码
        :return:
        """
        with open('/Users/afa/myFiles/pwd/yundama_pwd.json', 'r') as f:
            yundama_info = json_2_dict(f.read())

        username = yundama_info['username']
        pwd = yundama_info['pwd']
        app_key = yundama_info['app_key']
        res = yundama_ocr_captcha(
            username=username,
            pwd=pwd,
            app_key=app_key,
            code_type=1004,  # 4位字符数字
            img_path='./mt_captcha.png')

        print('识别结果:{}'.format(res))

        return res

    async def _get_mt_all_city_name_list(self) -> list:
        """
        得到mt已覆盖的城市名(只返回待抓取的城市名)
        :return:
        """
        _ = await self._get_crawl_city_area()
        for i in ['北京', '上海', '天津', '重庆']:
            _.append(i)

        res = []
        for i in _:
            if i not in ['北京', '石家庄', '武汉']:
                res.append(i)

        return ['天津']

    async def _get_category(self, city_name='北京') -> list:
        """
        获取某城市的所有分类信息(once)
        :return:
        """
        async def _parse(body) -> list:
            """解析"""
            async def _get_one_type_url(i) -> str:
                nonlocal categroy_info_parser_obj

                one_type_url = await async_parse_field(
                    parser=categroy_info_parser_obj['one_type_url'],
                    target_obj=i,
                    logger=self.lg)
                assert one_type_url != '', 'one_type_url不为空值'
                if re.compile('http').findall(one_type_url) == []:
                    if re.compile('//').findall(one_type_url) != []:
                        one_type_url = 'https:' + one_type_url
                    else:  # 酒店
                        one_type_url = 'https://i.meituan.com' + one_type_url
                else:
                    pass

                return one_type_url

            async def _get_one_type_name(i) -> str:
                nonlocal categroy_info_parser_obj

                one_type_name = await async_parse_field(
                    parser=categroy_info_parser_obj['one_type_name'],
                    target_obj=i,
                    logger=self.lg)
                assert one_type_name != '', 'one_type_name不为空值!'

                return one_type_name

            async def _get_cid_and_cate_type(one_type_url) -> tuple:
                nonlocal categroy_info_parser_obj

                cid = await async_parse_field(
                    parser=categroy_info_parser_obj['cid'],
                    target_obj=one_type_url,
                    logger=self.lg)
                cate_type = await async_parse_field(
                    parser=categroy_info_parser_obj['cate_type'],
                    target_obj=one_type_url,
                    logger=self.lg)

                return cid, cate_type

            categroy_info_parser_obj = (await self._get_parser_obj(short_name='mt'))\
                .get('categroy_info', {})
            ul_list = await async_parse_field(
                parser=categroy_info_parser_obj['ul_list'],
                target_obj=body,
                is_first=False,
                logger=self.lg)
            type_list = []
            for item in ul_list[:]:  # 不跳过热门
                li_list =  await async_parse_field(
                    parser=categroy_info_parser_obj['ul_li'],
                    target_obj=item,
                    is_first=False,
                    logger=self.lg)
                for i in li_list[1:]:  # 跳过全部
                    try:
                        one_type_url = await _get_one_type_url(i=i)
                        one_type_name = await _get_one_type_name(i=i)
                        cid, cate_type = await _get_cid_and_cate_type(one_type_url)
                    except AssertionError:
                        self.lg.error('遇到错误:', exc_info=True)
                        continue
                    type_list.append({
                        'one_type_url': one_type_url,
                        'one_type_name': one_type_name,
                        'cid': cid,
                        'cate_type': cate_type,
                    })

            return type_list

        city_name: str = ''.join(lazy_pinyin(city_name))
        headers = await self._get_phone_headers()
        headers.update({
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://i.meituan.com/category?city={}&cevent=imt/homepage/category2/99999'.format(city_name),
        })
        params = (
            ('city', city_name),
        )
        url = 'http://i.meituan.com/category'
        # 老是请求失败
        # body = await unblock_request(url=url, headers=headers, params=params, ip_pool_type=self.ip_pool_type, num_retries=10)
        body = await unblock_request_by_driver(
            url=_get_url_contain_params(url, params),
            executable_path=self.driver_path,
            logger=self.lg,
            user_agent_type=PHONE,
            ip_pool_type=self.ip_pool_type,)
        # self.lg.info(str(body))
        assert body != '', '获取分类数据的body为空值!'

        type_list = await _parse(body=body)
        # pprint(type_list)

        return type_list

    async def _hy_spider(self):
        """
        黄页spider(采用穷举采集的方式)
        :return:
        """
        self.db_hy_unique_id_list = await self._get_db_unique_id_list_by_site_id(site_id=2)
        await self._crawl_hy_company_info()

    async def _get_db_unique_id_list_by_site_id(self, site_id:int) -> list:
        """
        获取db中的unique id list
        :return:
        """
        self.lg.info('正在获取db中的site_id:{} 的unique_id...'.format(site_id))
        try:
            res = self.sql_server_cli._select_table(sql_str=gs_select_str_1, params=(site_id,), logger=self.lg)
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            return []
        self.lg.info('unique_id获取成功!')
        self.lg.info('正在组成unique_id list ...')
        oo = []
        for item in res:
            oo.append(item[0])

        for item in res:
            self.bloom_filter.add(item[0])

        self.lg.info('组成unique_id list 成功!')

        return oo

    async def _crawl_hy_company_info(self, **kwargs):
        """
        抓取黄页的公司信息
        :return:
        """
        async def _get_tasks_params_list() -> list:
            """得到tasks params list"""
            tasks_params_list = []
            for company_id in range(self.hy_min_company_id, self.hy_max_company_id):
                if 'hy{}'.format(company_id) not in self.db_hy_unique_id_list:
                    tasks_params_list.append({
                        'company_id': company_id,
                        'company_url': 'http://b2b.huangye88.com/qiye{}/'.format(company_id),
                    })

            return tasks_params_list

        tasks_params_list = await _get_tasks_params_list()
        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=self.concurrency)

        index = 0
        from time import time

        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            tasks = []
            for k in slice_params_list:
                company_id = k['company_id']
                company_url = k['company_url']
                self.lg.info('create task[where company_id:{}]...'.format(company_id))
                # 用ensure_furture效果一样
                tasks.append(self.loop.create_task(self._parse_one_company_info(
                    short_name='hy',
                    company_id=company_id,
                    company_url=company_url)))

            s_time = time()
            for child_task in as_completed(fs=tasks):
                # 完成一个打印一个
                child_res = await child_task
                if child_res:
                    index += 1
                    if child_res != {}:
                        await self._save_company_item(
                            company_item=child_res,
                            index=index)

            self.lg.info('此次耗时 {} s!'.format(round(float(time() - s_time), 3)))
            kill_process_by_name(process_name='phantomjs')

            # one_res = await async_wait_tasks_finished(tasks=tasks)
            # kill_process_by_name(process_name='phantomjs')
            #
            # for i in one_res:
            #     index += 1
            #     if i != {}:
            #         await self._save_company_item(
            #             company_item=i,
            #             index=index)

            await async_sleep(2.)

    async def _ty_spider(self) -> None:
        """
        天眼查企业信息爬虫
        :return:
        """
        if self.ty_cookies_dict == {}:
            await self._ty_login()

        province_and_city_info = await self._get_ty_province_and_city_info()
        pprint(province_and_city_info)
        await self._crawl_ty_company_info(province_and_city_info=province_and_city_info)

    async def _ty_login(self) -> dict:
        """
        天眼模拟登陆
        :return: 登陆后的cookies
        """
        headers = await self._get_pc_headers()
        headers.update({
            'Origin': 'https://www.tianyancha.com',
            'Referer': 'https://www.tianyancha.com/',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json; charset=UTF-8',
        })
        with open('/Users/afa/myFiles/pwd/tianyancha_pwd.json', 'r') as f:
            ty_pwd_info = json_2_dict(f.read(), logger=self.lg)

        data = dumps({
            'mobile': ty_pwd_info['username'],
            'cdpassword': ty_pwd_info['pwd'],
            'loginway': 'PL',
            'autoLogin': True
        })
        login_url = 'https://www.tianyancha.com/cd/login.json'
        proxies = Requests._get_proxies(ip_pool_type=self.ip_pool_type)
        with session() as s:
            with s.post(url=login_url, headers=headers, data=data, proxies=proxies) as resp:
                token = json_2_dict(resp.text).get('data', {}).get('token', '')
                self.lg.info('[{}] 登陆ty!'.format('+' if token != '' else '-'))
                assert token != '', '获取到的token为空值!'
                cookies = resp.cookies.get_dict()
                cookies.update({
                    'auth_token': token,
                })
                # pprint(cookies)
                self.ty_cookies_dict = cookies

                return cookies

    async def _get_ty_province_and_city_info(self) -> list:
        """
        得到天眼查省份, 城市信息
        :return:
        """
        async def _parse_info(body) -> list:
            """页面解析"""
            async def _get_zhixia_city_info() -> list:
                """获取直辖市信息"""
                nonlocal province_city_info_selector, body

                # 获取直辖市
                try:
                    zhixai_city_name = await async_parse_field(
                        parser=province_city_info_selector['zhixia_city_name'],
                        target_obj=body,
                        is_first=False,
                        logger=self.lg)
                    assert zhixai_city_name != '', 'zhixai_city_name为空值!'
                    zhixia_city_url = await async_parse_field(
                        parser=province_city_info_selector['zhixia_city_url'],
                        target_obj=body,
                        is_first=False,
                        logger=self.lg)
                    _ = list(zip(zhixai_city_name, zhixia_city_url))
                    assert zhixia_city_url != '', 'zhixia_city_url为空值!'
                    # pprint(_)
                except (AssertionError, Exception):
                    self.lg.error('遇到错误', exc_info=True)
                    return []

                province_and_city_info = []
                for item in _:
                    province_and_city_info.append({
                        'province_name': item[0],
                        'province_url': item[1],
                        'city_items': [],
                    })

                return province_and_city_info

            async def _get_other_province_info(province_and_city_info) -> list:
                """获取其他省份的信息"""
                nonlocal province_city_info_selector, body

                row = Selector(text=body).css('div.row').extract() or []
                assert row != [], 'row为空list!'
                for item in row:
                    try:
                        one_area_info = await self._parse_one_area_info(
                            province_city_info_selector=province_city_info_selector,
                            item=item)
                        province_name = one_area_info.get('province_name', '')
                        province_url = one_area_info.get('province_url', '')
                        city_name_list = one_area_info.get('city_name_list', [])
                        city_url_list = one_area_info.get('city_url_list', [])
                        _ = list(zip(city_name_list, city_url_list))
                    except (AssertionError, Exception):
                        self.lg.error('遇到错误:', exc_info=True)
                        continue

                    province_and_city_info.append({
                        'province_name': province_name,
                        'province_url': province_url,
                        'city_items': [{
                            'city_name': i[0],
                            'city_url': i[1],
                        } for i in _],
                    })

                return province_and_city_info

            parser_obj = await self._get_parser_obj(short_name='ty')
            province_city_info_selector = parser_obj['province_city_info']
            province_and_city_info = await _get_zhixia_city_info()
            # pprint(province_and_city_info)

            province_and_city_info = await _get_other_province_info(province_and_city_info=province_and_city_info)
            # pprint(province_and_city_info)

            return province_and_city_info

        async def _delete_uncrawl_area() -> list:
            """删除不抓取的地区"""
            nonlocal province_and_city_info

            crawl_province_area = await self._get_crawl_province_area()
            crawl_city_area = await self._get_crawl_city_area()

            # 删除省份
            new_province_and_city_info = []
            for index, i in enumerate(province_and_city_info):
                province_name = i['province_name']
                province_url = i['province_url']
                city_items = i['city_items']
                if province_name in crawl_province_area:
                    tmp_city_items = []
                    for j in city_items:
                        if j.get('city_name', '') in crawl_city_area:
                            tmp_city_items.append(j)

                    new_province_and_city_info.append({
                        'province_name': province_name,
                        'province_url': province_url,
                        'city_items': tmp_city_items
                    })

            return new_province_and_city_info

        url = 'https://www.tianyancha.com/'
        body = await unblock_request(url=url, headers=await self._get_pc_headers(), ip_pool_type=self.ip_pool_type)
        # self.lg.info(str(body))
        assert body != '', 'body为空值!'

        province_and_city_info = await _parse_info(body=body)
        # pprint(province_and_city_info)
        province_and_city_info = await _delete_uncrawl_area()
        # pprint(province_and_city_info)

        return province_and_city_info

    async def _qcc_spider(self) -> None:
        """
        企查查企业信息爬虫
        :return:
        """
        province_and_city_info = await self._get_qcc_province_and_city_info()
        pprint(province_and_city_info)
        await self._crawl_qcc_company_info(province_and_city_info=province_and_city_info)

    async def _get_qcc_province_and_city_info(self) -> list:
        """
        获取企查查省份信息
        :return:
        """
        async def _parse_info() -> list:
            """页面解析"""
            async def _get_area_info() -> list:
                """得到区域信息"""
                nonlocal body

                try:
                    one_area_info = await self._parse_one_area_info(
                        province_city_info_selector=province_city_info_selector,
                        item=body,
                        province_name_is_first=False,
                        province_url_is_first=False)
                    # pprint(one_area_info)
                    province_name = [i.replace(' ', '') for i in one_area_info.get('province_name', [])]
                    province_url = ['https://www.qichacha.com' + i for i in one_area_info.get('province_url', [])  if i != '']
                    city_name_list = one_area_info.get('city_name_list', [])
                    city_url_list = one_area_info.get('city_url_list', [])
                    _ = list(zip(province_name, province_url))
                except (AssertionError, Exception):
                    self.lg.error('遇到错误:', exc_info=True)
                    return []

                province_and_city_info = []
                for item in _:
                    province_and_city_info.append({
                        'province_name': item[0],
                        'province_url': item[1],
                        'city_items': [],
                    })

                return province_and_city_info

            nonlocal body
            parser_obj = await self._get_parser_obj(short_name='qcc')
            province_city_info_selector = parser_obj['province_city_info']
            province_and_city_info = await _get_area_info()

            return province_and_city_info

        async def _delete_uncrawl_area() -> list:
            """删除不抓取的地区"""
            nonlocal province_and_city_info

            crawl_province_area = await self._get_crawl_province_area()
            new_province_and_city_info = []
            for item in province_and_city_info:
                if item.get('province_name', '') in crawl_province_area:
                    new_province_and_city_info.append(item)

            return new_province_and_city_info

        headers = await self._get_pc_headers()
        headers.update({
            'authority': 'www.qichacha.com',
        })
        url = 'https://www.qichacha.com/'
        body = await unblock_request(url=url, headers=headers, ip_pool_type=self.ip_pool_type)
        # self.lg.info(str(body))
        assert body != '', 'body为空值!'

        province_and_city_info = await _parse_info()
        province_and_city_info = await _delete_uncrawl_area()

        return province_and_city_info

    async def _crawl_ty_company_info(self, **kwargs):
        """
        在天眼查中抓取待采集的目标
        :param kwargs:
        :return:
        """
        async def _get_tasks_params_list(item) -> list:
            """获取tasks_params_list"""
            tasks_params_list = []
            for page_num in range(1, self.ty_max_page_num):
                tasks_params_list.append({
                    'province_name': item['province_name'],
                    'city_name': item['city_name'],
                    'city_url': item['city_url'],
                    'page_num': page_num,
                })

            return tasks_params_list

        province_and_city_info = kwargs['province_and_city_info']

        all = []
        new_city_info_list = await self._get_ty_city_info_list(province_and_city_info)
        # pprint(new_city_info_list)
        for item in new_city_info_list:
            tasks_params_list = await _get_tasks_params_list(item=item)
            tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=self.concurrency)
            all_res = []
            # 每完成concurrency个任务 自增1
            self.oo_index = 0
            while True:
                try:
                    slice_params_list = tasks_params_list_obj.__next__()
                except AssertionError:
                    break

                tasks = []
                for k in slice_params_list:
                    province_name = k['province_name']
                    city_name = k['city_name']
                    page_num = k['page_num']
                    self.lg.info('create task[where province_name:{}, city_name:{}, page_num:{}]...'.format(province_name, city_name, page_num))
                    tasks.append(self.loop.create_task(self._crawl_one_page_from_ty_area_search(
                        province_name=province_name,
                        city_name=city_name,
                        city_url=k['city_url'],
                        page_num=page_num,)))

                one_res = await async_wait_tasks_finished(tasks=tasks)
                self.oo_index += 1

                # 失败数
                fail_count = 0
                for i in one_res:
                    if i == []:
                        fail_count += 1
                    for j in i:
                        all_res.append(j)

                await self._ty_crawl_exception_handler(
                    fail_count=fail_count,
                    one_res_len=len(one_res))
                await async_sleep(1.)

            self.lg.info('province_name:{}, city_name:{}, all_res个数: {}'.format(item['province_name'], item['city_name'], len(all_res)))
            self.lg.info('休眠{}s...'.format(5))
            await async_sleep(5)

            company_items = await self._block_crawl_company_info(
                short_name='ty',
                this_province_company_url_list=all_res)

            # 增加到all
            all.append({
                'province_name': item['province_name'],
                'company_items': company_items,
            })

    async def _ty_crawl_exception_handler(self, **kwargs) -> None:
        """
        ty抓取异常的处理
        :return:
        """
        fail_count = kwargs['fail_count']
        one_res_len = kwargs['one_res_len']
        sleep_time = 30

        if self.ty_robot:
            # url = 'https://antirobot.tianyancha.com/captcha/verify?return_url=https%3A%2F%2Fwww.tianyancha.com%2Fsearch%2Fp100%3Fbase%3Dbj%26rnd%3D%26rnd%3D%26rnd%3D%26rnd%3D%26rnd%3D%26rnd%3D&rnd='
            # self.lg.info('请点击校验地址进行校验: {}'.format(url))
            while True:
                a = input('请进行ty的人工识别!(完成请输入y)')
                if a in ('Y', 'y'):
                    self.ty_robot = False
                    break
            await self._ty_login()
        else:
            # TODO 测试发现每100次，被强迫登出, 进行再次登录
            if self.oo_index + 1 >= 100 / self.concurrency:
                self.oo_index = 0
                self.lg.info('进行再次登录...')
                await self._ty_login()

            if fail_count / one_res_len > 1/4:
                self.lg.info('失败超一定比例, 休眠{}s...'.format(sleep_time))
                await async_sleep(sleep_time)
                self.lg.info('进行再次登录...')
                await self._ty_login()

        return None

    async def _crawl_qcc_company_info(self, **kwargs):
        """
        在企查查中抓取待采集的目标
        :param kwargs:
        :return:
        """
        province_and_city_info = kwargs['province_and_city_info']
        all = []
        for item in province_and_city_info:
            tasks_params_list = []
            for page_num in range(1, self.qcc_max_page_num):
                tasks_params_list.append({
                    'province_name': item['province_name'],
                    'province_url': item['province_url'],
                    'page_num': page_num,
                })

            tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=self.concurrency)
            all_res = []
            while True:
                try:
                    slice_params_list = tasks_params_list_obj.__next__()
                except AssertionError:
                    break

                tasks = []
                for k in slice_params_list:
                    province_name = k['province_name']
                    page_num = k['page_num']
                    self.lg.info('create task[where province_name:{}, page_num:{}]...'.format(province_name, page_num))
                    tasks.append(self.loop.create_task(self._crawl_one_page_from_qcc_area_search(
                        province_name=province_name,
                        province_url=k['province_url'],
                        page_num=page_num,)))

                one_res = await async_wait_tasks_finished(tasks=tasks)
                for i in one_res:
                    for j in i:
                        all_res.append(j)
                await async_sleep(1)

            self.lg.info('province_name:{}, all_res个数: {}'.format(item['province_name'], len(all_res)))
            self.lg.info('休眠{}s...'.format(5))
            await async_sleep(5)

            company_items = await self._block_crawl_company_info(
                short_name='qcc',
                this_province_company_url_list=all_res)

            # 增加到all
            all.append({
                'province_name': item['province_name'],
                'company_items': company_items,
            })

    async def _crawl_one_page_from_ty_area_search(self, **kwargs) -> list:
        """
        抓取ty单页信息
        :param kwargs:
        :return:
        """
        province_name = kwargs['province_name']
        city_name = kwargs['city_name']
        city_url = kwargs['city_url']
        page_num = kwargs['page_num']

        try:
            base = re.compile('base=(\w+)').findall(city_url)[0]
        except IndexError:
            self.lg.error('获取base时索引异常!')
            return []

        headers = await self._get_pc_headers()
        params = (
            ('base', base),
        )
        # 形如: https://www.tianyancha.com/search/p250?base=sjz
        url = 'https://www.tianyancha.com/search/p{}'.format(page_num)
        body = await unblock_request(url=url, headers=headers, params=params, cookies=self.ty_cookies_dict, ip_pool_type=self.ip_pool_type)
        # self.lg.info(str(body))
        # 414 Request-URI Too Large 要求点选
        if body == '':
            self.lg.info('获取到的body为空值!')
            return []

        if '-天眼查' not in body:
            # 标记处理
            self.ty_robot = True

        _, _new = await self._get_company_status_is_right_new_company_url_list(
            short_name='ty',
            body=body,
            province_name=province_name,
            city_name=city_name)
        label = '+' if _ != [] else '-'
        self.lg.info('[{}] province_name:{}, city_name:{}, page_num:{}, 实际在业个数:{}'.format(label, province_name, city_name, page_num, len(_new)))

        return _new

    async def _get_ty_city_info_list(self, province_and_city_info) -> list:
        """
        获取ty的待抓取的city_list(只抓取city)
        :param province_and_city_info:
        :return: [{'city_name': 'xxx', 'province_name': 'xxx', 'city_url': 'xxx'}, ...]
        """
        _ = []
        for item in province_and_city_info:
            city_items = item['city_items']
            province_name = item['province_name']
            if city_items == []:
                _.append({
                    'province_name': province_name,
                    'city_name': item['province_name'],
                    'city_url': item['province_url']
                })
            else:
                for i in city_items:
                    _.append({
                        'province_name': province_name,
                        'city_name': i['city_name'],
                        'city_url': i['city_url'],
                    })

        return _

    async def _crawl_one_page_from_qcc_area_search(self, **kwargs) -> list:
        """
        抓取企查查单页信息
        :param kwargs:
        :return: [] or [{'company_url': 'xxxx',}, ...]
        """
        province_name = kwargs['province_name']
        province_url = kwargs['province_url']
        page_num = kwargs['page_num']

        headers = await self._get_phone_headers()
        headers.update({
            'authority': 'www.qichacha.com',
        })
        url = province_url + '_{}'.format(page_num)
        body = await unblock_request(url=url, headers=headers, ip_pool_type=self.ip_pool_type)
        # self.lg.info(str(body))
        if body == '':
            self.lg.info('获取到的body为空值!')
            return []

        _, _new = await self._get_company_status_is_right_new_company_url_list(
            short_name='qcc',
            body=body,
            province_name=province_name,
            city_name='')
        label = '+' if _ != [] else '-'
        self.lg.info('[{}] province_name:{}, page_num:{}, 实际在业个数:{}'.format(label, province_name, page_num, len(_new)))

        return _new

    async def _get_company_status_is_right_new_company_url_list(self, **kwargs) -> tuple:
        """
        筛选出经营状态正常的company_url(公司状态异常的处理)
        :param body: 待解析的body
        :return: (_:未处理前的, _new:处理后的)
        """
        short_name = kwargs['short_name']
        body = kwargs['body']
        province_name = kwargs.get('province_name', '')
        city_name = kwargs.get('city_name', '')

        _ = await self._parse_company_url_and_company_status(
            parser_obj=await self._get_parser_obj(short_name=short_name),
            target_obj=body
        )
        # pprint(_)

        # 公司状态异常的处理
        _new = []
        danger_status_list = ['吊销，未注销', '注销', '吊销']
        for i in _:
            if i['company_status'] not in danger_status_list:
                if short_name == 'ty':
                    company_url = i['company_url']
                elif short_name == 'qcc':
                    company_url = 'https://m.qichacha.com' + i['company_url']
                else:
                    raise NotImplemented('未知的获取company_url的方法!')

                _new.append({
                    'company_url': company_url,
                    'province_name': province_name,
                    'city_name': city_name,
                })
        # pprint(_new)

        return _, _new

    async def _parse_company_url_and_company_status(self, parser_obj, target_obj) -> list:
        """
        从搜索页中解析company_url和company_status
        :param parser_obj: 解析对象
        :param target_obj: 待解析目标
        :return:
        """
        try:
            company_url = await async_parse_field(
                parser=parser_obj['company_url'],
                target_obj=target_obj,
                is_first=False,
                logger=self.lg)
            company_status = await async_parse_field(
                parser=parser_obj['company_status'],
                target_obj=target_obj,
                is_first=False,
                logger=self.lg)
            _ = list(zip(company_url, company_status))
        except (AssertionError, Exception):
            self.lg.error('遇到错误:', exc_info=True)
            return []

        return [{
            'company_url': i[0],
            'company_status': i[1],
        } for i in _]

    async def _block_crawl_company_info(self, **kwargs) -> list:
        """
        根据company_url 分块抓取(eg: 企查查, 天眼查)的所有页面详情
        :return:
        """
        short_name = kwargs['short_name']
        # 身份 or city company_url_list
        this_province_company_url_list = kwargs['this_province_company_url_list']

        tasks_params_list = await self._get_block_crawl_company_tasks_params_list(
            short_name=short_name,
            this_province_company_url_list=this_province_company_url_list,)

        tasks_params_list_obj = TasksParamsListObj(tasks_params_list=tasks_params_list, step=self.concurrency)
        all_res = []
        self.oo_index = 0
        index = 0
        while True:
            try:
                slice_params_list = tasks_params_list_obj.__next__()
            except AssertionError:
                break

            tasks = []
            for k in slice_params_list:
                company_url = k['company_url']
                province_name = k['province_name']
                city_name = k['city_name']
                self.lg.info('create task[where province_name:{}, city_name:{}, company_url:{}]...'.format(province_name, city_name, company_url))
                tasks.append(self.loop.create_task(self._parse_one_company_info(
                    company_url=company_url,
                    province_name=province_name,
                    city_name=city_name,
                    short_name=short_name,)))

            one_res = await async_wait_tasks_finished(tasks=tasks)
            self.oo_index += 1

            # 失败数
            fail_count = 0
            for i in one_res:
                index += 1
                if i != {}:
                    all_res.append(i)
                    await self._save_company_item(
                        company_item=i,
                        index=index)
                else:
                    fail_count += 1

            await self._ty_crawl_exception_handler(
                fail_count=fail_count,
                one_res_len=len(one_res))
            await async_sleep(2)

        self.lg.info('all_res所有数据抓取完毕! 总个数: {}'.format(len(all_res)))

        return all_res

    async def _get_block_crawl_company_tasks_params_list(self, **kwargs) -> list:
        """
        得到分块抓取多公司信息的tasks_params_list
        :param short_name:
        :return:
        """
        short_name = kwargs['short_name']
        this_province_company_url_list = kwargs['this_province_company_url_list']

        tasks_params_list = []
        if short_name == 'ty'\
                or short_name == 'qcc':
            for item in this_province_company_url_list:
                tasks_params_list.append({
                    'company_url': item['company_url'],
                    'province_name': item['province_name'],
                    'city_name': item['city_name'],
                })

        else:
            raise NotImplemented

        return tasks_params_list

    async def _parse_one_company_info(self, **kwargs) -> dict:
        """
        解析单页的信息
        :return: {} or {xxx}
        """
        short_name = kwargs['short_name']
        company_url = kwargs.get('company_url', '')
        province_name = kwargs.get('province_name', '')
        city_name = kwargs.get('city_name', '')
        company_id = kwargs.get('company_id', '')
        type_code = kwargs.get('type_code', '')
        company_html = kwargs.get('company_html', None)
        ori_address = kwargs.get('ori_address', None)

        if company_html is None:
            # 未传入company_html
            company_html = await self._get_someone_company_page_html(
                short_name=short_name,
                company_url=company_url,
                company_id=company_id,
                city_name=city_name,
                type_code=type_code)
            if company_html == '':
                return {}
        else:
            pass
        # self.lg.info(str(company_html))

        parser_obj = await self._get_parser_obj(short_name=short_name)
        try:
            unique_id = await self._get_company_unique_id(parser_obj=parser_obj, target_obj=company_url)
            company_name = await self._get_company_name(parser_obj=parser_obj, target_obj=company_html)
            company_link = await self._get_company_link(parser_obj=parser_obj, target_obj=company_html)
            legal_person = await self._get_legal_person(parser_obj=parser_obj, target_obj=company_html)
            phone = await self._get_phone(parser_obj=parser_obj, target_obj=company_html)
            email_address = await self._get_email_address(parser_obj=parser_obj, target_obj=company_html)
            address = await self._get_address(parser_obj=parser_obj, target_obj=company_html, ori_address=ori_address)
            brief_introduction = await self._get_brief_introduction(parser_obj=parser_obj, target_obj=company_html, company_id=company_id)
            business_range = await self._get_business_range(parser_obj=parser_obj, target_obj=company_html)
            founding_time = await self._get_founding_time(parser_obj=parser_obj, target_obj=company_html)
            province_id = await self._get_province_id(parser_obj=parser_obj, target_obj=company_html, province_name=province_name, city_name=city_name, address=address)
            city_id = await self._get_city_id(parser_obj=parser_obj, target_obj=company_html, city_name=city_name, address=address)
            employees_num = await self._get_employees_num(parser_obj=parser_obj, target_obj=company_html)
            type_code = await self._get_type_code(parser_obj=parser_obj, type_code=type_code)
            lng = await self._get_lng(parser_obj=parser_obj, target_obj=company_html)
            lat = await self._get_lat(parser_obj=parser_obj, target_obj=company_html)
        except (AssertionError, Exception):
            self.lg.error('遇到错误: 出错company_url:{}'.format(company_url), exc_info=True)
            return {}

        company_item = CompanyItem()
        company_item['province_id'] = province_id
        company_item['city_id'] = city_id
        company_item['unique_id'] = unique_id
        company_item['company_url'] = company_url
        company_item['company_link'] = company_link
        company_item['company_name'] = company_name
        company_item['legal_person'] = legal_person
        company_item['phone'] = phone
        company_item['email_address'] = email_address
        company_item['address'] = address
        company_item['brief_introduction'] = brief_introduction
        company_item['business_range'] = business_range
        company_item['founding_time'] = founding_time
        company_item['lng'] = lng
        company_item['lat'] = lat
        company_item['employees_num'] = employees_num
        company_item['create_time'] = get_shanghai_time()
        company_item['site_id'] = await self._get_site_id(short_name=short_name)
        company_item['type_code'] = type_code
        # pprint(company_item)

        self.lg.info('[{}] task[where province_name:{}, city_name:{}, province_id:{}, city_id:{}, company_url:{}]'.format(
            '+',
            province_name,
            city_name,
            province_id,
            city_id,
            company_url,))

        return dict(company_item)

    async def _get_lng(self, parser_obj, target_obj) -> float:
        """
        获取经度信息
        :param parser_obj:
        :param target_obj:
        :return:
        """
        if parser_obj['short_name'] == 'mt':
            lng = await async_parse_field(
                parser=parser_obj['lng'],
                target_obj=target_obj,
                logger=self.lg,)
        else:
            return 0.

        return float(lng)

    async def _get_lat(self, parser_obj, target_obj) -> float:
        """
        获取纬度信息
        :param parser_obj:
        :param target_obj:
        :return:
        """
        if parser_obj['short_name'] == 'mt':
            lat = await async_parse_field(
                parser=parser_obj['lat'],
                target_obj=target_obj,
                logger=self.lg,)
        else:
            return 0.

        return float(lat)

    async def _get_type_code(self, parser_obj, type_code) -> str:
        """
        得到分类的code
        :param type_code:
        :return:
        """
        if parser_obj['short_name'] == 'mt':
            return 'mt' + type_code
        else:
            return ''

    async def _get_site_id(self, short_name) -> int:
        """
        获取采集源site_id
        :param short_name:
        :return:
        """
        if short_name == 'qcc':
            site_id = 3
        elif short_name == 'ty':
            site_id = 1
        elif short_name == 'hy':
            site_id = 2
        elif short_name == 'mt':
            site_id = 4
        elif short_name == 'al':
            site_id = 5
        elif short_name == '114':
            site_id = 6
        elif short_name == 'ic':
            site_id = 7
        elif short_name == 'yw':
            site_id = 8
        elif short_name == 'hn':
            site_id = 9
        elif short_name == 'pk':
            site_id = 10
        elif short_name == 'ng':
            site_id = 11
        elif short_name == 'gt':
            site_id = 12
        else:
            raise NotImplemented('site_id没有实现!')

        return site_id

    async def _save_company_item(self, company_item, index) -> bool:
        """
        异步存储company_item
        :param company_item:
        :return:
        """
        async def _get_args() -> list:
            """获取args"""
            return [
                self.insert_into_sql,
                await _get_insert_params(),
                self.lg,
            ]

        async def _get_insert_params() -> tuple:
            nonlocal company_item

            params = [
                company_item['province_id'],
                company_item['city_id'],
                company_item['unique_id'],
                company_item['company_url'],
                company_item['company_link'],
                company_item['company_name'],
                company_item['legal_person'],
                dumps(company_item['phone'], ensure_ascii=False),
                dumps(company_item['email_address'], ensure_ascii=False),
                company_item['address'],
                company_item['brief_introduction'],
                company_item['business_range'],
                company_item['founding_time'],
                company_item['create_time'],
                company_item['site_id'],
                company_item['employees_num'],
                company_item['type_code'],
                company_item['lng'],
                company_item['lat'],
            ]

            return tuple(params)

        # 非阻塞(死锁, 单独存)
        # loop = get_event_loop()
        # args = await _get_args()
        # try:
        #     res = loop.run_in_executor(None, self.sql_server_cli._insert_into_table_3, *args)
        # except Exception:
        #     self.lg.error('遇到错误:', exc_info=True)
        # finally:
        #     try:
        #         del loop
        #     except:
        #         pass
        #     collect()
        #
        #     return res

        # 阻塞
        try:
            self.sql_server_cli = await _get_new_db_conn(
                db_obj=self.sql_server_cli,
                index=index,
                logger=self.lg,)
        except:
            try:
                self.sql_server_cli = await _get_new_db_conn(
                    db_obj=self.sql_server_cli,
                    index=index,
                    logger=self.lg,)
            except:
                self.sql_server_cli = await _get_new_db_conn(
                    db_obj=self.sql_server_cli,
                    index=index,
                    logger=self.lg,)

        res = await self.sql_server_cli._insert_into_table_3(
            sql_str=self.insert_into_sql,
            params=await _get_insert_params(),
            logger=self.lg)

        return res

    async def _get_employees_num(self, parser_obj, target_obj) -> str:
        """
        公司人数
        :param parser_obj:
        :param target_obj:
        :return:
        """
        if parser_obj['short_name'] == 'hy':
            employees_num = await self._get_hy_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='员工人数')

        elif parser_obj['short_name'] == '114':
            employees_num = await self._get_114_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='员工人数',
                parser_obj_dict_name='company_info_detail_li_1',)

        elif parser_obj['short_name'] == 'ic':
            employees_num = await self._get_ic_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='员工人数',
                parser_obj_dict_name='company_info_detail_li_1',)

        else:
            employees_num = await async_parse_field(
                parser=parser_obj['employees_num'],
                target_obj=target_obj,
                logger=self.lg)

        return employees_num

    async def _get_company_name(self, parser_obj, target_obj) -> str:
        """
        得到企业名称
        :param parser_obj:
        :param target_obj:
        :return:
        """
        # self.lg.info(str(target_obj))
        if parser_obj['short_name'] == 'hy':
            company_name = await self._get_hy_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='公司名称')

        elif parser_obj['short_name'] == 'al':
            company_name = await self._get_al_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='公司名称')

        elif parser_obj['short_name'] == 'pk':
            target_obj = json_2_dict(
                json_str=target_obj,
                logger=self.lg,
                default_res={})
            company_name = target_obj.get('shop_name', '')

        elif parser_obj['short_name'] == 'ng':
            company_name = await self._get_ng_li_text_by_label_name(
                parser_obj_dict_name='company_info_detail_li_1',
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='店铺名称',)

        else:
            company_name = await async_parse_field(
                parser=parser_obj['company_name'],
                target_obj=target_obj,
                logger=self.lg)

        if parser_obj['short_name'] == '114':
            if company_name !='':
                if len(company_name) <= 3:
                    # 人名字默认设置为无
                    company_name = '无'

        # if company_name == '':
        #     self.lg.info(target_obj)

        assert company_name != '', 'company_name为空值!'

        return company_name

    async def _get_company_link(self, parser_obj, target_obj) -> str:
        """
        得到企业官网地址
        :param parser_obj:
        :param target_obj:
        :return:
        """
        if parser_obj['short_name'] == 'hy':
            company_link = await self._get_hy_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='公司网站',)
        else:
            company_link = await async_parse_field(
                parser=parser_obj['company_link'],
                target_obj=target_obj,
                logger=self.lg)

        # 可为空值
        # assert company_link != '', 'company_link为空值!'

        return company_link

    async def _get_legal_person(self, parser_obj, target_obj) -> str:
        """
        获取法人
        :param parser_obj:
        :param target_obj:
        :return:
        """
        if parser_obj['short_name'] == 'hy':
            legal_person = await self._get_hy_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='企业法人',)

        elif parser_obj['short_name'] == 'al':
            legal_person = await self._get_al_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='法人代表',)

        elif parser_obj['short_name'] == '114':
            legal_person = await self._get_114_li_text_by_label_name(
                parser_obj_dict_name='company_info_detail_li_1',
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='法定代表人',)

        else:
            legal_person = await async_parse_field(
                parser=parser_obj['legal_person'],
                target_obj=target_obj,
                logger=self.lg)

        # 法人可以为空, eg: https://www.tianyancha.com/company/2876734
        # 但是本爬虫不采集法人为空的高端企业! $_$
        # hy 可空
        # assert legal_person != '', 'legal_person为空值!'

        return legal_person

    async def _get_phone(self, parser_obj, target_obj) -> list:
        """
        获取phone
        :param parser_obj:
        :param target_obj:
        :return:
        """
        is_first = True
        if parser_obj['short_name'] == 'al':
            is_first = False

        _phone1, _phone2 = '', ''
        if parser_obj['short_name'] == 'hy':
            phone = await self._get_hy_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='公司电话',)

        elif parser_obj['short_name'] == '114':
            phone = '无'
            _phone1 = await self._get_114_li_text_by_label_name(
                parser_obj_dict_name='company_info_detail_li_2',
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='手机',)
            _phone2 = await self._get_114_li_text_by_label_name(
                parser_obj_dict_name='company_info_detail_li_2',
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='电话',)

        elif parser_obj['short_name'] == 'ic':
            phone = '无'
            _phone1 = await self._get_ic_li_text_by_label_name(
                parser_obj_dict_name='company_info_detail_li_2',
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='手机',)
            _phone2 = await self._get_ic_li_text_by_label_name(
                parser_obj_dict_name='company_info_detail_li_2',
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='电话',)

        elif parser_obj['short_name'] == 'yw':
            phone = '无'
            _phone1 = await async_parse_field(
                parser=parser_obj['phone1'],
                target_obj=target_obj,
                logger=self.lg,
                is_first=is_first)
            _phone2 = await async_parse_field(
                parser=parser_obj['phone2'],
                target_obj=target_obj,
                logger=self.lg,
                is_first=is_first)

        elif parser_obj['short_name'] == 'hn':
            phone = await self._get_hn_li_text_by_label_name(
                parser_obj_dict_name='company_info_detail_li_1',
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='电话',)

        elif parser_obj['short_name'] == 'pk':
            phone = '无'
            target_obj = json_2_dict(
                json_str=target_obj,
                logger=self.lg,
                default_res={})
            _phone1 = target_obj.get('phone_mob', '')
            _phone2 = ''

        elif parser_obj['short_name'] == 'ng':
            phone = '无'
            _phone1 = await self._get_ng_li_text_by_label_name(
                parser_obj_dict_name='company_info_detail_li_2',
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='电话客服',)
            _phone2 = await self._get_ng_li_text_by_label_name(
                parser_obj_dict_name='company_info_detail_li_2',
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='手机客服',)

        else:
            phone = await async_parse_field(
                parser=parser_obj['phone'],
                target_obj=target_obj,
                logger=self.lg,
                is_first=is_first)

        # assert phone != '', 'phone为空值!'
        if is_first and phone == '':
            return []

        if parser_obj['short_name'] == 'ty':
            phone_list = json_2_dict(phone, default_res=[], logger=self.lg)
            phone_list = [{
                'phone': i,
            } for i in phone_list]

        elif parser_obj['short_name'] == 'mt':
            phone_list = phone.split('/')
            phone_list = [{
                'phone': i,
            } for i in phone_list]

        elif parser_obj['short_name'] == 'al':
            phone_list = [{
                'phone': i,
            } for i in phone]

        elif parser_obj['short_name'] == '114' or \
                parser_obj['short_name'] == 'ic' or \
                parser_obj['short_name'] == 'yw' or \
                parser_obj['short_name'] == 'pk' or \
                parser_obj['short_name'] == 'ng':
            phone_list = []
            if _phone1 != '' and len(_phone1) >= 5:
                phone_list.append({
                    'phone': _phone1,
                })
            if _phone2 != '' and len(_phone2) >= 5:
                phone_list.append({
                    'phone': _phone2,
                })
            # self.lg.info('phone1:{}, phone2:{}'.format(_phone1, _phone2))

        else:
            phone_list = [{
                'phone': phone,
            }]

        # 去重
        phone_list = list_remove_repeat_dict_plus(target=phone_list, repeat_key='phone')
        # pprint(phone_list)
        if phone_list != []:
            if phone_list == [{'phone': ''}]:
                # 处理114的异常情况
                phone_list = []

        if parser_obj['short_name'] == '114' or \
                parser_obj['short_name'] == 'ic' or \
                parser_obj['short_name'] == 'yw' or \
                parser_obj['short_name'] == 'hn' or \
                parser_obj['short_name'] == 'pk' or \
                parser_obj['short_name'] == 'ng' or \
                parser_obj['short_name'] == 'gt':
            assert phone_list != [], 'phone_list不能为空list!'

        return phone_list

    async def _get_email_address(self, parser_obj, target_obj) -> list:
        """
        获取email
        :return:
        """
        if parser_obj['short_name'] == 'hy':
            email_address = await self._get_hy_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='公司邮箱',)
        else:
            is_first = True
            if parser_obj['short_name'] == 'ty':
                is_first = False

            email_address = await async_parse_field(
                parser=parser_obj['email_address'],
                target_obj=target_obj,
                logger=self.lg,
                is_first=is_first)

        # assert email_address != '', 'email_address为空值!'
        new_email_address = email_address
        if parser_obj['short_name'] == 'ty':
            new_email_address = ''
            for item in email_address:
                if '@' in item:
                    new_email_address = item
                    break

        if new_email_address == ''\
                or new_email_address == '暂无信息':
            return []

        else:
            # 只允许有一个，并且只取第一个
            return [{
                'email_address': new_email_address,
            }]

    async def _get_address(self, parser_obj, target_obj, **kwargs) -> str:
        """
        获取address
        :param parser_obj:
        :param target_obj:
        :return:
        """
        ori_address = kwargs.get('ori_address', None)

        is_first = True
        if parser_obj['short_name'] == 'ty'\
                or parser_obj['short_name'] == 'hy':
            is_first = False

        if parser_obj['short_name'] == 'al':
            address = await self._get_al_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='经营地址',)
            if address == '':
                # 无经营地址则取联系地址的字段
                address = await self._get_al_li_text_by_label_name(
                    parser_obj=parser_obj,
                    target_obj=target_obj,
                    label_name='联系地址',)

        elif parser_obj['short_name'] == '114':
            address = await self._get_114_li_text_by_label_name(
                parser_obj_dict_name='company_info_detail_li_2',
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='地址',)

        elif parser_obj['short_name'] == 'ic':
            address = await self._get_ic_li_text_by_label_name(
                parser_obj_dict_name='company_info_detail_li_2',
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='地址',)

        elif parser_obj['short_name'] == 'yw':
            address = await self._get_yw_li_text_by_label_name(
                parser_obj_dict_name='company_info_detail_li_1',
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='商铺地址',)

        elif parser_obj['short_name'] == 'hn':
            address = await self._get_hn_li_text_by_label_name(
                parser_obj_dict_name='company_info_detail_li_1',
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='地址',)

        elif parser_obj['short_name'] == 'pk':
            address = ori_address

        else:
            address = await async_parse_field(
                parser=parser_obj['address'],
                target_obj=target_obj,
                logger=self.lg,
                is_first=is_first)

        if parser_obj['short_name'] == 'ty':
            try:
                address = address[0]
            except IndexError:
                raise IndexError('获取address时索引异常!')
        elif parser_obj['short_name'] == 'hy':
            new_address = address
            for item in address:
                # self.lg.info(item)
                if '地址' in item:
                    try:
                        new_address = re.compile('地址：(.*)').findall(item)[0]
                        # self.lg.info(new_address)
                        break
                    except IndexError:
                        raise IndexError('获取hy的address时索引异常!')
            if isinstance(new_address, list):
                address = ''
            else:
                address = new_address
        else:
            pass

        if parser_obj['short_name'] == 'hy':
            # address可为空!
            pass
        else:
            assert address != '', 'address为空值!'

        return address

    async def _get_brief_introduction(self, parser_obj, target_obj, company_id) -> str:
        """
        获取company简介
        :param parser_obj:
        :param target_obj:
        :return:
        """
        if parser_obj['short_name'] == 'al':
            brief_introduction = await self._get_al_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='主营产品',)
            brief_introduction = '主营产品:' + brief_introduction \
                if brief_introduction != '' \
                else brief_introduction

        elif parser_obj['short_name'] == 'gt':
            introduction_html = await self._get_gt_introduction_html(company_id=company_id)
            brief_introduction = await async_parse_field(
                parser=parser_obj['brief_introduction'],
                target_obj=introduction_html,
                logger=self.lg)
            if '该商家暂无商家介绍' \
                    or '商家暂无此信息' \
                    in brief_introduction:
                brief_introduction = ''

        else:
            brief_introduction = await async_parse_field(
                parser=parser_obj['brief_introduction'],
                target_obj=target_obj,
                logger=self.lg)

        if parser_obj['short_name'] == 'hy'\
                or parser_obj['short_name'] == 'ic'\
                or parser_obj['short_name'] == 'gt':
            brief_introduction = re.compile('<br>|<a.*?>|</a>|<br/>|<br />').sub(' ', brief_introduction)

        # 可为空值
        # assert brief_introduction != '', 'brief_introduction为空值!'

        return await self._wash_data(brief_introduction)

    async def _get_gt_introduction_html(self, company_id) -> str:
        """
        获取gt company简介html
        :param company_id:
        :return:
        """
        self.lg.info('crawling company_id: {} introduction ...'.format(company_id))
        headers = await self._get_pc_headers()
        headers.update({
            # 'Referer': 'http://z.go2.cn/product/oaamaeq.html',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        url = 'http://{}.go2.cn/introduce.html'.format(company_id)
        body = await unblock_request(
            url=url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            logger=self.lg,
            num_retries=self.gt_max_num_retries,)
        # self.lg.info(body)

        return body

    async def _get_business_range(self, parser_obj, target_obj):
        """
        获取business_range
        :param parser_obj:
        :param target_obj:
        :return:
        """
        if parser_obj['short_name'] == 'hy':
            business_range = await self._get_hy_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='主营产品',)
            if business_range != '':
                business_range = '主营产品: ' + business_range

            # 主营产品为空, 则采集主营行业
            if business_range == '':
                business_range = await self._get_hy_li_text_by_label_name(
                    parser_obj=parser_obj,
                    target_obj=target_obj,
                    label_name='主营行业', )
                if business_range != '':
                    business_range = '主营行业: ' + business_range

        elif parser_obj['short_name'] == 'al':
            # TODO 可为'', business_range = ''的数据中发现company_name很多都为人名, 与原始页面一对比, 确实company_name为人名, 采集正确!!
            business_range = await self._get_al_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='经营范围',)

        elif parser_obj['short_name'] == '114':
            business_range = await self._get_114_li_text_by_label_name(
                parser_obj_dict_name='company_info_detail_li_1',
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='服务领域',)

        elif parser_obj['short_name'] == 'ic':
            business_range = await self._get_ic_li_text_by_label_name(
                parser_obj_dict_name='company_info_detail_li_1',
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='主营产品',)

        elif parser_obj['short_name'] == 'yw':
            business_range = await self._get_yw_li_text_by_label_name(
                parser_obj_dict_name='company_info_detail_li_1',
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='主营商品',)

        else:
            is_first = True
            if parser_obj['short_name'] == 'qcc':
                is_first = False

            business_range = await async_parse_field(
                parser=parser_obj['business_range'],
                target_obj=target_obj,
                logger=self.lg,
                is_first=is_first)
            # pprint(business_range)

        if parser_obj['short_name'] == 'qcc':
            try:
                business_range = business_range[5]
            except IndexError:
                raise IndexError('获取business_range时索引异常!')
        else:
            pass

        if parser_obj['short_name'] == 'mt' \
                or parser_obj['short_name'] == '114'\
                or parser_obj['short_name'] == 'ic'\
                or parser_obj['short_name'] == 'yw'\
                or parser_obj['short_name'] == 'hn'\
                or parser_obj['short_name'] == 'pk'\
                or parser_obj['short_name'] == 'gt'\
                or parser_obj['short_name'] == 'al':
            # mt可为空, 因为读其名知其意
            pass
        else:
            assert business_range != '', 'business_range为空值!'

        return await self._wash_data(business_range)

    async def _wash_data(self, data):
        """
        清洗data
        :param data:
        :return:
        """
        replace_str_list = [
            ('&lt;', '<'),
            ('&gt;', '>')
        ]
        add_sensitive_str_list = [
            '\u3000',
            '\xa0',
            '&nbsp;'
        ]

        return wash_sensitive_info(
            data=data,
            replace_str_list=replace_str_list,
            add_sensitive_str_list=add_sensitive_str_list)

    async def _get_founding_time(self, parser_obj, target_obj):
        """
        获取company成立时间
        :param parser_obj:
        :param target_obj:
        :return:
        """
        if parser_obj['short_name'] == 'hy':
            founding_time = await self._get_hy_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='成立时间',)
            # self.lg.info('founding_time:{}'.format(founding_time))

        elif parser_obj['short_name'] == 'al':
            founding_time = await self._get_al_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='成立日期',)

        elif parser_obj['short_name'] == '114':
            # eg: 1995年11月06日
            founding_time = await self._get_114_li_text_by_label_name(
                parser_obj_dict_name='company_info_detail_li_1',
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='成立时间',)
            if founding_time == '':
                # eg: 2001
                founding_time = await self._get_114_li_text_by_label_name(
                    parser_obj_dict_name='company_info_detail_li_1',
                    parser_obj=parser_obj,
                    target_obj=target_obj,
                    label_name='公司成立年',)

        else:
            is_first = True
            if parser_obj['short_name'] == 'qcc':
                is_first = False

            founding_time = await async_parse_field(
                parser=parser_obj['founding_time'],
                target_obj=target_obj,
                logger=self.lg,
                is_first=is_first)
            # pprint(founding_time)

        if parser_obj['short_name'] == 'qcc':
            try:
                founding_time = founding_time[3]
            except IndexError:
                raise IndexError('获取founding_time时索引异常!')

        elif parser_obj['short_name'] == 'ty'\
                or parser_obj['short_name'] == 'hy':
            try:
                # 1980年10月
                founding_time = re.compile('年|日').sub('-', founding_time)
                founding_time = re.compile('月').sub('', founding_time)
                founding_time = date_util_parse(founding_time)
            except Exception as e:
                # raise e
                # 设置一个默认值
                founding_time = datetime(1900, 1, 1)

        elif parser_obj['short_name'] == 'mt'\
                or parser_obj['short_name'] == 'ic'\
                or parser_obj['short_name'] == 'yw'\
                or parser_obj['short_name'] == 'hn'\
                or parser_obj['short_name'] == 'pk'\
                or parser_obj['short_name'] == 'ng'\
                or parser_obj['short_name'] == 'gt':
            founding_time = datetime(1900, 1, 1)

        elif parser_obj['short_name'] == 'al'\
                or parser_obj['short_name'] == '114':
            try:
                # 2017年03月24日
                founding_time = re.compile('年|月').sub('-', founding_time)
                founding_time = re.compile('日').sub('', founding_time)
                founding_time = date_util_parse(founding_time)
            except Exception as e:
                # raise e
                # 设置一个默认值
                founding_time = datetime(1900, 1, 1)

        else:
            pass

        assert founding_time != '', 'founding_time为空值!'

        return founding_time

    async def _get_company_unique_id(self, parser_obj, target_obj):
        """
        获取company 唯一的id
        :param parser_obj:
        :param target_obj:
        :return:
        """
        unique_id = await async_parse_field(
            parser=parser_obj['unique_id'],
            target_obj=target_obj,
            logger=self.lg)
        assert unique_id != '', 'unique_id为空值!'

        if parser_obj['short_name'] == 'hy':
            unique_id = 'hy' + unique_id

        if parser_obj['short_name'] == 'mt':
            unique_id = 'mt' + unique_id

        if parser_obj['short_name'] == 'al':
            unique_id = 'al' + unique_id

        if parser_obj['short_name'] == '114':
            unique_id = '114' + unique_id

        if parser_obj['short_name'] == 'ic':
            unique_id = 'ic' + unique_id

        if parser_obj['short_name'] == 'yw':
            unique_id = 'yw' + unique_id

        if parser_obj['short_name'] == 'hn':
            unique_id = 'hn' + unique_id

        if parser_obj['short_name'] == 'pk':
            unique_id = 'pk' + unique_id

        if parser_obj['short_name'] == 'ng':
            unique_id = 'ng' + unique_id

        if parser_obj['short_name'] == 'gt':
            unique_id = 'gt' + unique_id

        return unique_id

    async def _get_province_id(self, parser_obj, target_obj, province_name, city_name, address):
        """
        获取对应的省份code
        :return:
        """
        local_place = ''
        if parser_obj['short_name'] == 'hy':
            local_place = await self._get_hy_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='所在地',)
            # self.lg.info(local_place)
            try:
                province_name = local_place[0:2]
            except IndexError:
                raise IndexError('获取hy的province_name时索引异常! local_place: {}'.format(local_place))

        if parser_obj['short_name'] == '114':
            local_place = await self._get_114_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='地址',
                parser_obj_dict_name='company_info_detail_li_2',)
            assert local_place != '', 'local_place不能为空值!否则无法定位省份信息!'

        if parser_obj['short_name'] == 'ic':
            local_place = await self._get_ic_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='地址',
                parser_obj_dict_name='company_info_detail_li_2',)
            assert local_place != '', 'local_place不能为空值!否则无法定位省份信息!'

        if parser_obj['short_name'] == 'yw':
            local_place = await self._get_yw_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='商铺地址',
                parser_obj_dict_name='company_info_detail_li_1',)
            assert local_place != '', 'local_place不能为空值!否则无法定位省份信息!'
            if '义乌' in local_place:
                return '330000'

            else:
                raise ValueError('未知地址信息: {}'.format(local_place))

        if parser_obj['short_name'] == 'gt':
            local_place = await self._get_gt_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='城市',)
            try:
                # eg: '四川省'
                province_name = local_place.split(' ')[0]
                if province_name == '暂无':
                    address = await async_parse_field(
                        parser=parser_obj['address'],
                        target_obj=target_obj,
                        logger=self.lg,
                        is_first=True)
                    if '国际商贸城' or '商贸城' in address:
                        province_name = '四川省'

            except IndexError:
                raise IndexError('获取local_place时索引异常! local_place:{}'.format(local_place))

        for item in self.province_and_city_code_list:
            c_name = item[0]
            code = item[1]
            parent_code = item[2]
            if parser_obj['short_name'] == 'mt':
                if city_name in c_name:
                    # 单独处理mt的, 因为province_name传过来为空值!
                    return parent_code

            elif parser_obj['short_name'] == '114'\
                    or parser_obj['short_name'] == 'ic':
                # 处理114的, 因为province_name, city_name传过来都是空值!
                # 根据local_place来获取
                if parent_code == '':
                    # 说明是省份or直辖市
                    if c_name in local_place:
                        return code
                    else:
                        pass
                else:
                    # 否则就是 市级别
                    if re.compile('000$').findall(parent_code) != []:
                        # 说明是市,县级别
                        if c_name in local_place:
                            return parent_code
                        else:
                            pass
                    else:
                        # 说明其为县区级别, 不进行对比操作!!
                        pass
            else:
                if province_name in c_name:
                    return code

        raise AssertionError('未知的province_name:{}, db中未找到!'.format(province_name))

    async def _get_city_id(self, parser_obj, target_obj, city_name, address) -> str:
        """
        获取对应的city的code
        :param city_name:
        :return: '' or not ''
        """
        local_place = ''
        if parser_obj['short_name'] == 'hy':
            local_place = await self._get_hy_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='所在地', )
            try:
                province_name = local_place[0:2]
                city_name = local_place[3:5]
                if province_name not in ['北京', '上海', '重庆', '天津']:
                    pass
                else:
                    city_name = province_name
            except IndexError:
                raise IndexError('获取hy的city_name时索引异常! local_place: {}'.format(local_place))

        if parser_obj['short_name'] == '114':
            local_place = await self._get_114_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='地址',
                parser_obj_dict_name='company_info_detail_li_2',)
            assert local_place != '', 'local_place不能为空值!否则无法定位城市信息!'

        if parser_obj['short_name'] == 'ic':
            local_place = await self._get_ic_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='地址',
                parser_obj_dict_name='company_info_detail_li_2',)
            assert local_place != '', 'local_place不能为空值!否则无法定位城市信息!'
            # self.lg.info(local_place)

        if parser_obj['short_name'] == 'yw':
            local_place = await self._get_yw_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='商铺地址',
                parser_obj_dict_name='company_info_detail_li_1',)
            assert local_place != '', 'local_place不能为空值!否则无法城市定位信息!'
            if '义乌' in local_place:
                return '330782'

            else:
                raise ValueError('未知地址信息: {}'.format(local_place))

        if parser_obj['short_name'] == 'gt':
            local_place = await self._get_gt_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='城市',)
            try:
                province_name = local_place.split(' ')[0]
                if province_name == '暂无':
                    # 处理local_place为'暂无'的
                    address = await async_parse_field(
                        parser=parser_obj['address'],
                        target_obj=target_obj,
                        logger=self.lg,
                        is_first=True)
                    if '国际商贸城' or '商贸城' in address:
                        city_name = '成都市'
                    else:
                        pass
                else:
                    # eg: '成都市'
                    city_name = local_place.split(' ')[1]
            except IndexError:
                raise IndexError('获取local_place时索引异常! local_place:{}'.format(local_place))

        for item in self.province_and_city_code_list:
            c_name = item[0]
            code = item[1]
            # str
            parent_code = item[2]

            if parser_obj['short_name'] == '114'\
                    or parser_obj['short_name'] == 'ic':
                # 处理114的, 因为province_name, city_name传过来都是空值!
                # 根据local_place来获取city_id
                if parent_code == '':
                    # 说明是省份or直辖市
                    if re.compile('市').findall(c_name) != []:
                        # 只匹配四个直辖市, 匹配不到就跳过
                        if c_name in local_place:
                            return code
                        else:
                            continue
                    else:
                        continue
                else:
                    # self.lg.info('该地址为市级别: {}'.format(local_place))
                    # 否则就是 市级别
                    if re.compile('000$').findall(parent_code) != []:
                        # 说明是市, 县级别
                        if c_name in local_place:
                            # self.lg.info('code: {}, c_name: {}'.format(code, c_name))
                            return code
                        else:
                            continue
                    else:
                        # 说明其为县区级别, 不进行对比操作!!
                        continue
            else:
                if city_name in c_name:
                    return code

        if parser_obj['short_name'] == '114' \
                or parser_obj['short_name'] == 'ic'\
                or parser_obj['short_name'] == 'hn'\
                or parser_obj['short_name'] == 'pk'\
                or parser_obj['short_name'] == 'gt':
            raise AssertionError('未知的city_name:{}, db中未找到!'.format(city_name))

        else:
            # 可以为空, 企查查的为空
            pass

        return ''

    async def _get_gt_li_text_by_label_name(self, parser_obj, target_obj, label_name) -> str:
        """
        根据label_name获取gt对应的值
        :param parser_obj:
        :param target_obj:
        :param label_name:
        :return:
        """
        company_info_detail_li = await async_parse_field(
            parser=parser_obj['company_info_detail_li_1'],
            target_obj=target_obj,
            logger=self.lg,
            is_first=False)
        company_info_detail_li = list_duplicate_remove(company_info_detail_li)
        for item in company_info_detail_li:
            item = item.replace('\r', '').replace('\t', '').replace('\n', '')
            # self.lg.info(item)
            label = (Selector(text=item).css('label ::text').extract_first() or '') \
                .replace(':', '').replace(' ', '').replace('：', '')
            _text = await self._wash_data(
                data=Selector(text=item).css('span ::text').extract_first() or ''
            )

            # self.lg.info('label: {}'.format(label))
            # self.lg.info('_text: {}'.format(_text))
            if label == label_name:
                return _text

        return ''

    async def _get_yw_li_text_by_label_name(self, parser_obj_dict_name:str, parser_obj, target_obj, label_name):
        """
        根据label_name获取对应的值
        :param parser_obj_dict_name:
        :param parser_obj:
        :param target_obj:
        :param label_name:
        :return:
        """
        company_info_detail_li = await async_parse_field(
            parser=parser_obj[parser_obj_dict_name],
            target_obj=target_obj,
            logger=self.lg,
            is_first=False)
        company_info_detail_li = list_duplicate_remove(company_info_detail_li)
        for item in company_info_detail_li:
            item = item.replace('\r', '').replace('\t', '').replace('\n', '')
            # self.lg.info(item)
            label = (Selector(text=item).css('span.c999 ::text').extract_first() or '') \
                .replace(':', '').replace(' ', '').replace('：', '')
            _text = await self._wash_data(
                data=Selector(text=item).css('span.con ::text').extract_first() or ''
            )

            # self.lg.info('label: {}'.format(label))
            # self.lg.info('_text: {}'.format(_text))
            if label == label_name:
                return _text

        return ''

    async def _get_ng_li_text_by_label_name(self, parser_obj_dict_name, parser_obj, target_obj, label_name):
        """
        根据label_name获取ng对应的值
        :param parser_obj_dict_name:
        :param parser_obj:
        :param target_obj:
        :param label_name:
        :return:
        """
        company_info_detail_li = await async_parse_field(
            parser=parser_obj[parser_obj_dict_name],
            target_obj=target_obj,
            logger=self.lg,
            is_first=False)
        company_info_detail_li = list_duplicate_remove(company_info_detail_li)
        # 旨在兼容company_info_detail_li_1 or company_info_detail_li_2
        # 处理得到店铺名称 or 联系方式的label选择器
        if parser_obj_dict_name == 'company_info_detail_li_1':
            label_css_selector = 'span ::text'
            _text_css_selector = {
                'method': 're',
                'selector': '<\/em>(.*?)<\/div>',
            }
        else:
            label_css_selector = 'div.companyContactConsultName ::text'
            _text_css_selector = {
                'method': 'css',
                'selector': 'div.companyContactConsultTouch ::text',
            }
        
        for item in company_info_detail_li:
            # 下面这步取消
            # item = item.replace(' ', '')
            # self.lg.info(item)
            label = (Selector(text=item).css(label_css_selector).extract_first() or '') \
                .replace(':', '').replace(' ', '').replace('：', '')
            _text = await self._wash_data(
                data=await async_parse_field(
                    parser=_text_css_selector,
                    target_obj=item,
                    is_first=True,
                    logger=self.lg,))

            # self.lg.info('label: {}'.format(label))
            # self.lg.info('_text: {}'.format(_text))
            if label == label_name:
                return _text

        return ''


    async def _get_hn_li_text_by_label_name(self, parser_obj_dict_name:str, parser_obj, target_obj, label_name):
        """
        根据label_name获取hn对应的值
        :param parser_obj_dict_name: 解析对象的名字, eg: company_info_detail_li_1
        :param parser_obj:
        :param target_obj:
        :param label_name:
        :return:
        """
        company_info_detail_li = await async_parse_field(
            parser=parser_obj[parser_obj_dict_name],
            target_obj=target_obj,
            logger=self.lg,
            is_first=False)
        company_info_detail_li = list_duplicate_remove(company_info_detail_li)
        for item in company_info_detail_li:
            # self.lg.info(item)
            # 旨在兼容company_info_detail_li_1 or company_info_detail_li_2
            label = (Selector(text=item).css('div.left span.title ::text').extract_first() or '') \
                .replace(':', '').replace(' ', '').replace('：', '')
            _text = await self._wash_data(Selector(text=item).css('div.right p ::text').extract_first() or '')

            # self.lg.info('label: {}'.format(label))
            # self.lg.info('_text: {}'.format(_text))
            if label == label_name:
                return _text

        return ''

    async def _get_ic_li_text_by_label_name(self, parser_obj_dict_name:str, parser_obj, target_obj, label_name):
        """
        根据label_name获取对应的值
        :param parser_obj_dict_name: 解析对象的名字, eg: company_info_detail_li_1, company_info_detail_li_2
        :param parser_obj:
        :param target_obj:
        :param label_name:
        :return:
        """
        company_info_detail_li = await async_parse_field(
            parser=parser_obj[parser_obj_dict_name],
            target_obj=target_obj,
            logger=self.lg,
            is_first=False)
        company_info_detail_li = list_duplicate_remove(company_info_detail_li)
        for item in company_info_detail_li:
            item = item.replace(' ', '')
            # self.lg.info(item)
            # 旨在兼容company_info_detail_li_1 or company_info_detail_li_2
            label = (Selector(text=item).css('th ::text').extract_first() or '') \
                .replace(':', '').replace(' ', '').replace('：', '')
            _text = await self._wash_data(data=Selector(text=item).css('td ::text').extract_first() or '')

            # self.lg.info('label: {}'.format(label))
            # self.lg.info('_text: {}'.format(_text))
            if label == label_name:
                return _text

        return ''

    async def _get_114_li_text_by_label_name(self, parser_obj_dict_name:str, parser_obj, target_obj, label_name):
        """
        根据label_name获取对应的值
        :param parser_obj_dict_name: 解析对象的名字, eg: company_info_detail_li_1, company_info_detail_li_2
        :param parser_obj:
        :param target_obj:
        :param label_name:
        :return:
        """
        company_info_detail_li = await async_parse_field(
            parser=parser_obj[parser_obj_dict_name],
            target_obj=target_obj,
            logger=self.lg,
            is_first=False)
        company_info_detail_li = list_duplicate_remove(company_info_detail_li)
        for item in company_info_detail_li:
            item = item.replace(' ', '')
            # self.lg.info(item)
            # 旨在兼容company_info_detail_li_1 or company_info_detail_li_2
            label = (Selector(text=item).css('span ::text').extract_first() or '') \
                .replace(':', '').replace(' ', '').replace('：', '')

            if re.compile('<li>').findall(item) != []:
                # company_info_detail_li_1中是li
                css_selector = 'li'
            elif re.compile('<small>').findall(item) != []:
                # company_info_detail_li_2是small
                css_selector = 'small'
            else:
                raise ValueError('在获取label_name:{}时, 未找到相应标签无法进行正常解析!'.format(label_name))

            # 无值就取''
            _text = ''
            try:
                _text = await self._wash_data(
                    data=(Selector(text=item).css('{} ::text'.format(css_selector)).extract() or ['', ''])[1]\
                        .replace(' ', ''))
            except IndexError:
                pass

            # self.lg.info('label: {}'.format(label))
            # self.lg.info('_text: {}'.format(_text))
            if label == label_name:
                return _text

        return ''

    async def _get_al_li_text_by_label_name(self, parser_obj, target_obj, label_name):
        """
        根据label_name获取对应的值
        :param parser_obj:
        :param target_obj:
        :param label_name:
        :return:
        """
        company_info_detail_li = await async_parse_field(
            parser=parser_obj['company_info_detail_li'],
            target_obj=target_obj,
            logger=self.lg,
            is_first=False)
        company_info_detail_li = list_duplicate_remove(company_info_detail_li)
        for item in company_info_detail_li:
            # self.lg.info(item)
            label = (Selector(text=item).css('em ::text').extract_first() or '')\
                .replace(':', '').replace(' ', '')
            _text = (Selector(text=item).css('span ::text').extract_first() or '')\
                .replace(' ', '')
            # self.lg.info(label)
            # self.lg.info(_text)
            if label == label_name:
                return _text

        return ''

    async def _get_hy_li_text_by_label_name(self, parser_obj, target_obj, label_name):
        """
        根据label_name 获取其对应的值
        :param label_name:
        :return:
        """
        company_info_detail_li = await async_parse_field(
            parser=parser_obj['company_info_detail_li'],
            target_obj=target_obj,
            logger=self.lg,
            is_first=False)
        company_info_detail_li = list_duplicate_remove(company_info_detail_li)
        for item in company_info_detail_li:
            # self.lg.info(item)
            label = Selector(text=item).css('label ::text').extract_first() or ''
            item = re.compile('<label.*?>.*</label>').sub('', item)
            _text = Selector(text=item).css('::text').extract_first() or ''
            # self.lg.info(label)
            # self.lg.info(_text)
            if label == label_name:
                return _text

        return ''

    async def _get_someone_company_page_html(self, **kwargs) -> str:
        """
        对应获取某个公司的html
        :return:
        """
        short_name = kwargs['short_name']
        company_url = kwargs['company_url']
        company_id = kwargs['company_id']
        city_name = kwargs['city_name']
        type_code = kwargs['type_code']

        if short_name == 'qcc':
            return await self._get_qcc_company_page_html(company_url=company_url)

        elif short_name == 'ty':
            return await self._get_ty_company_page_html(company_url=company_url)

        elif short_name == 'hy':
            return await self._get_hy_company_page_html(company_id=company_id)

        elif short_name == 'mt':
            return await self._get_mt_company_page_html(
                company_id=company_id,
                city_name=city_name,
                type_code=type_code)

        elif short_name == 'al':
            return await self._get_al_company_page_html(company_id=company_id)

        elif short_name == '114':
            return await self._get_114_company_page_html(company_id=company_id)

        elif short_name == 'ic':
            return await self._get_ic_company_page_html(company_id=company_id)

        elif short_name == 'yw':
            return await self._get_yw_company_page_html(company_id=company_id)

        elif short_name == 'hn':
            return await self._get_hn_company_page_html(
                company_id=company_id,
                company_url=company_url)

        elif short_name == 'pk':
            return await self._get_pk_company_page_html(
                company_id=company_id,
                city_name=city_name,)

        elif short_name == 'ng':
            return await self._get_ng_company_page_html(company_id=company_id)

        elif short_name == 'gt':
            return await self._get_gt_company_page_html(company_id=company_id)

        else:
            raise NotImplemented

    async def _get_gt_company_page_html(self, company_id) -> str:
        """
        获取gt pc站的公司详情html
        :param company_id:
        :return:
        """
        headers = await self._get_pc_headers()
        headers.update({
            # 'Referer': 'http://z.go2.cn/product/oaamaeq.html',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        url = 'http://{}.go2.cn/'.format(company_id)
        body = await unblock_request(
            url=url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            logger=self.lg,
            num_retries=self.gt_max_num_retries,)
        # self.lg.info(body)
        if body == '':
            self.lg.error('company body为空值! company_id: {}'.format(company_id))

        return body

    async def _get_ng_company_page_html(self, company_id) -> str:
        """
        获取ng m站的公司简介html
        :param company_id:
        :return:
        """
        headers = await self._get_phone_headers()
        headers.update({
            'Connection': 'keep-alive',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            # 'Referer': 'http://m.nanguo.cn/company/index/id/13583',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        params = (
            ('id', str(company_id)),
        )
        url = 'http://m.nanguo.cn/company/info/'
        body = await unblock_request(
            url=url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.ng_max_num_retries,
            logger=self.lg)
        # self.lg.info(body)

        return body

    async def _get_pk_company_page_html(self, company_id, city_name) -> str:
        """
        获取pk的是接口数据, 最后转换为json str返回!
        :param company_id:
        :param city_name:
        :return: eg: '{"id":"58507","is_gold":"N","shop_name":"\u9999\u9999\u5bb6\u725b\u4ed4","path_image":"http:\/\/www.ppkoo.com\/static\/images\/no-img.jpg","build_name":"\u5973\u4eba\u8857","floor_name":"\u4e94\u697c","is_sale_one":"N","is_return_cash":"N","is_shipai":"N","shop_location":"515-C","qq":"6361960","phone_mob":"18620916223","date_add":"2018-04-24 09:38","cat_id":null,"is_attention":0,"product_count":"60","sale_count":"1","favour_count":"0"}'
        """
        async def _get_city_id(city_name) -> int:
            """获取city_id"""
            for item in self.new_pk_city_info_list:
                if item.get('city_name', '') == city_name:
                    return item.get('city_id')

            raise ValueError('city_name value异常!请检查!')

        # 获取店铺信息
        # https://m.ppkoo.com/shop/58507
        headers = await self._get_phone_headers()
        headers.update({
            'origin': 'https://m.ppkoo.com',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'accept': 'application/json, text/plain, */*',
            'authority': 'www.ppkoo.com',
        })
        city_id = await _get_city_id(city_name)
        params = (
            ('business_id', str(company_id)),
            ('city_id', str(city_id)),
            # ('v', '9248394389559154'),
        )
        url = 'https://www.ppkoo.com/api/Business/index'
        body = await unblock_request(
            url=url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.pk_max_page_num,
            logger=self.lg,)
        # self.lg.info(body)
        if body == '':
            self.lg.error('company body为空值! company_id: {}, city_id: {}'.format(company_id, city_id))
            return ''

        data = json_2_dict(
            json_str=body,
            default_res={},
            logger=self.lg).get('business', {})
        # pprint(data)
        try:
            res = dumps(data)
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            return ''

        return res

    async def _get_hn_company_page_html(self, company_id, company_url) -> str:
        """
        获取hn单页的company_info
        :param company_id:
        :param company_url:
        :return:
        """
        headers = await self._get_pc_headers()
        headers.update({
            'Proxy-Connection': 'keep-alive',
            # 'Referer': 'http://hz.huoniuniu.com/goods?q=%E7%9F%AD%E8%A2%96&sourcePage=/',
        })
        w3_selector = {
            'method': 're',
            'selector': ':\/\/(\w+)\.',
        }
        try:
            w3 = await async_parse_field(
                parser=w3_selector,
                target_obj=company_url,
                logger=self.lg,)
        except AssertionError:
            self.lg.error('遇到错误:', exc_info=True)
            return ''

        url = 'http://{}.huoniuniu.com/shop/{}'.format(w3, company_id)
        # 并发requests失败率高, 改用driver
        # body = await unblock_request(
        #     url=url,
        #     headers=headers,
        #     ip_pool_type=self.ip_pool_type,
        #     num_retries=self.hn_max_num_retries,
        #     logger=self.lg)

        body = await unblock_request_by_driver(
            url=url,
            type=PHANTOMJS,
            executable_path=self.driver_path,
            logger=self.lg,
            ip_pool_type=self.ip_pool_type,
            timeout=25,)

        # self.lg.info(body)

        if body == '':
            self.lg.error('company body为空值! shop_url: {}'.format(url))

        return body

    async def _get_yw_company_page_html(self, company_id) -> str:
        """
        获取yw单页的company_info
        :param company_id:
        :return:
        """
        url = 'http://www.yiwugo.com/hu/{}.html'.format(company_id)
        # 成功率低
        # headers = await self._get_pc_headers()
        # headers.update({
        #     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        # })
        # body = await unblock_request(
        #     url=url,
        #     headers=headers,
        #     ip_pool_type=self.ip_pool_type,
        #     logger=self.lg,
        #     num_retries=6,)

        body = await unblock_request_by_driver(
            url=url,
            type=PHANTOMJS,
            executable_path=self.driver_path,
            logger=self.lg,
            ip_pool_type=self.ip_pool_type,
            timeout=20,
        )
        # self.lg.info(body)

        if body == '':
            self.lg.error('company body为空值! shop_url: {}'.format(url))

        return body

    async def _get_ic_company_page_html(self, company_id) -> str:
        """
        获取ic单页company info
        :param company_id:
        :return:
        """
        detail_url = 'https://3g.made-in-china.com/company-{}/info.html'.format(company_id)
        contact_url = 'https://3g.made-in-china.com/company-{}/contact.html'.format(company_id)
        phone_headers = await self._get_phone_headers()
        detail_body = await unblock_request(
            url=detail_url,
            headers=phone_headers,
            ip_pool_type=self.ip_pool_type,
            logger=self.lg,)
        contact_body = await unblock_request(
            url=contact_url,
            headers=phone_headers,
            ip_pool_type=self.ip_pool_type,
            logger=self.lg,)
        # self.lg.info(detail_body)
        # self.lg.info(contact_body)

        body_compile = re.compile('<body.*?>(.*)</body>')
        try:
            body = '<body>' + body_compile.findall(detail_body)[0] + body_compile.findall(contact_body)[0] + '</body>'
            # self.lg.info(body)
        except IndexError:
            self.lg.info('获取body_1 or body_2时索引异常!\n出错detail_url:{}, contact_url:{}'.format(detail_url, contact_url))
            return ''

        return body

    async def _get_114_company_page_html(self, company_id) -> str:
        """
        获取114单页company info
        :param company_id:
        :return:
        """
        headers = await self._get_pc_headers()
        headers.update({
            'Proxy-Connection': 'keep-alive',
            # 'Referer': 'http://www.114pifa.com/c-3181.html',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        url = 'http://www.114pifa.com/ca/{}'.format(company_id)
        body = await unblock_request(
            url=url,
            headers=headers,
            cookies=None,
            ip_pool_type=self.ip_pool_type,
            encoding='gbk',
            num_retries=self.a114_max_num_retries,
            logger=self.lg)
        if body == '':
            self.lg.error('company body为空值! shop_url: {}'.format(url))

        return body

    async def _get_al_company_page_html(self, company_id) -> str:
        """
        获取al单页店铺info
        :param company_id:
        :return:
        """
        headers = await self._get_phone_headers()
        headers.update({
            'authority': 'm.1688.com',
            'cache-control': 'max-age=0',
        })
        # self.lg.info(company_id)
        url = 'https://m.1688.com/winport/company/{}.html'.format(company_id)
        body = await unblock_request(
            url=url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            logger=self.lg)
        # self.lg.info(body)
        if body == '':
            self.lg.error('店铺body为空值! shop_url: {}'.format(url))

        return body

    async def _get_mt_company_page_html(self, company_id, city_name, type_code) -> str:
        """
        获取mt单页店铺信息
        :param company_url:
        :return:
        """
        headers = await self._get_phone_headers()
        city_name_pinyin = ''.join(lazy_pinyin(city_name))
        random_page_num = get_random_int_number(1, 100)
        referer = 'http://i.meituan.com/select/{}/page_{}.html?cid={}&bid=-1&sid=defaults&p={}&bizType=area&csp=&stid_b=_b2&cateType=poi&nocount=true'.format(
            city_name_pinyin,
            random_page_num,
            type_code,
            random_page_num,)
        headers.update({
            # 'Referer': 'http://i.meituan.com/select/shijiazhuang/page_32.html?cid=20097&bid=-1&sid=defaults&p=32&bizType=area&csp=&stid_b=_b2&cateType=poi&nocount=true',
            'Referer': referer,
        })
        url = 'https://meishi.meituan.com/i/poi/{}'.format(company_id)
        body = await unblock_request(url=url, headers=headers, ip_pool_type=self.ip_pool_type)
        # self.lg.info(body)
        if body == '':
            self.lg.error('shop_url: {}'.format(url))

        return body

    async def _get_hy_company_page_html(self, company_id) -> str:
        """
        获取hy某个company的html
        :param company_id:
        :return:
        """
        detail_url = 'http://m.huangye88.com/gongsi/{}/detail.html'.format(company_id)
        contact_url = 'http://m.huangye88.com/gongsi/{}/contact.html'.format(company_id)
        headers = await self._get_phone_headers()
        with await self.sema:
            # requests老是无数据, 改用驱动
            # body_1 = await unblock_request(url=detail_url, headers=headers, ip_pool_type=self.ip_pool_type)
            body_1 = await unblock_request_by_driver(
                executable_path=self.driver_path,
                url=detail_url,
                user_agent_type=PHONE,
                ip_pool_type=self.ip_pool_type,
                logger=self.lg,
                timeout=self.driver_timeout,)
            # self.lg.info(body_1)
            if body_1 == ''\
                    or '对不起，您要找的页面可能不存在或已删除' in body_1:
                self.lg.error('detail_url: {}, 获取到的body为空值!'.format(detail_url))
                return ''

            # 可以为空
            # body_2 = await unblock_request(url=contact_url, headers=headers, ip_pool_type=self.ip_pool_type)
            body_2 = await unblock_request_by_driver(
                executable_path=self.driver_path,
                url=contact_url,
                user_agent_type=PHONE,
                ip_pool_type=self.ip_pool_type,
                logger=self.lg,
                timeout=self.driver_timeout,)
            # self.lg.info(body_2)

            body_compile = re.compile('<body.*?>(.*)</body>')
            try:
                body = '<body>' + body_compile.findall(body_1)[0] + body_compile.findall(body_2)[0]
                # self.lg.info(body)
            except IndexError:
                self.lg.info('获取body_1 or body_2时索引异常!\n出错detail_url:{}, contact_url:{}'.format(detail_url, contact_url))
                return ''

            return body

    async def _get_ty_company_page_html(self, company_url) -> str:
        """
        获取天眼查某个company的html
        :param company_url:
        :return:
        """
        headers = await self._get_pc_headers()
        body = await unblock_request(url=company_url, headers=headers, cookies=self.ty_cookies_dict, ip_pool_type=self.ip_pool_type)
        # self.lg.info(str(body))
        if body == '':
            self.lg.error('company_url: {}, 获取到的body为空值!'.format(company_url))
        else:
            if '天眼查' not in body:
                # self.lg.info(str(body))
                self.ty_robot = True

        return body

    async def _get_qcc_company_page_html(self, company_url) -> str:
        """
        获取到企查查某个company的html
        :param company_url:
        :return:
        """
        headers = await self._get_phone_headers()
        headers.update({
            'authority': 'm.qichacha.com',
        })
        body = await unblock_request(url=company_url, headers=headers, ip_pool_type=self.ip_pool_type)
        # self.lg.info(str(body))
        if body == '':
            self.lg.error('company_url: {}, 获取到的body为空值!'.format(company_url))

        return body

    async def _parse_one_area_info(self, province_city_info_selector, item, province_name_is_first=True, province_url_is_first=True) -> dict:
        """
        解析一个地域信息
        :return:
        """
        async def _get_province_name():
            """省份"""
            province_name = await async_parse_field(
                parser=province_city_info_selector['province_name'],
                target_obj=item,
                is_first=province_name_is_first,
                logger=self.lg)
            assert province_name != '', 'province_name为空值!'

            return province_name

        async def _get_province_url():
            """省份url"""
            province_url = await async_parse_field(
                parser=province_city_info_selector['province_url'],
                target_obj=item,
                is_first=province_url_is_first,
                logger=self.lg)
            assert province_url != '', 'province_url为空值!'

            return province_url

        async def _get_city_name_list() -> list:
            """省份下面的市"""
            if province_city_info_selector['city_name'] is None:
                return []

            city_name_list = await async_parse_field(
                parser=province_city_info_selector['city_name'],
                target_obj=item,
                is_first=False,
                logger=self.lg)
            assert city_name_list != [], 'city_name_list为空list!'

            return city_name_list

        async def _get_city_url_list() -> list:
            """省份下面市的url"""
            if province_city_info_selector['city_url'] is None:
                return []

            city_url_list = await async_parse_field(
                parser=province_city_info_selector['city_url'],
                target_obj=item,
                is_first=False,
                logger=self.lg)
            assert city_url_list != [], 'city_url_list为空list!'

            return city_url_list

        try:
            province_name = await _get_province_name()
            province_url = await _get_province_url()
            city_name_list = await _get_city_name_list()
            city_url_list = await _get_city_url_list()
        except (AssertionError, Exception) as e:
            raise e

        return {
            'province_name': province_name,
            'province_url': province_url,
            'city_name_list': city_name_list,
            'city_url_list': city_url_list,
        }

    @staticmethod
    async def _get_parser_obj(short_name) -> dict:
        """
        得到解析对象
        :param short_name:
        :return:
        """
        parser_obj = None
        for item in COMPANY_ITEM_LIST:
            if item['short_name'] == short_name:
                parser_obj = item
        assert parser_obj is not None, 'parser_obj为None!'

        return parser_obj

    async def _get_pc_headers(self) -> dict:
        return {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_random_pc_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    async def _get_phone_headers(self) -> dict:
        return {
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_phone_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

    @staticmethod
    async def _get_mt_ciid(city_name) -> str:
        """
        获取mt城市代码(弃用)
        :return:
        """
        _ = {
            '北京': 1,
            '上海': 10,
            '天津': 40,
            '重庆': 45,
            '石家庄': 76,
            '保定': 84,
            '张家口': 125,
            '沈阳': 66,
            '南京': 55,
            '杭州': 50,
            '金华': 188,
            '青岛': 60,
            '武汉': 57,
            '广州': 20,
            '深圳': 30,
        }
        ciid = ''
        for key, value in _.items():
            if city_name == key:
                return str(value)

        return ciid

    @staticmethod
    async def _get_crawl_province_area() -> list:
        """
        抓取的省份
        :return:
        """
        return ['北京', '天津', '上海', '重庆', '河北', '辽宁', '江苏', '浙江', '山东', '湖北', '广东']

    @staticmethod
    async def _get_crawl_city_area() -> list:
        """
        抓取的城市
        :return:
        """
        return ['石家庄', '保定', '张家口', '沈阳', '南京', '杭州', '金华', '青岛', '武汉', '广州', '深圳']

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        try:
            del self.lg
        except:
            pass
        collect()

@click_command()
@click_option('--spider_name', type=str, default=None, help='what is spider_name !!')
def init_spider(spider_name,):
    """
    main
    :param spider_name:
    :return:
    """
    global SPIDER_NAME

    SPIDER_NAME = spider_name
    try:
        _ = CompanySpider()
        loop = get_event_loop()
        res = loop.run_until_complete(_._fck_run())
    except KeyboardInterrupt:
        kill_process_by_name('phantomjs')
        kill_process_by_name('firefox')
    finally:
        try:
            loop.close()
            del loop
        except:
            pass

def test_parse_one_company_info():
    """
    use: 使用时注释掉func init_spider
    :return:
    """
    def get_al_kwargs():
        company_id = 'my2010gd'
        company_url = 'https://m.1688.com/winport/company/{}.html'.format(company_id)

        return {
            'short_name': 'al',
            'company_id': company_id,
            'company_url': company_url,
            'province_name': '广东',
            'city_name': '广州市',
        }

    kwargs = get_al_kwargs()
    try:
        _ = CompanySpider()
        loop = get_event_loop()
        res = loop.run_until_complete(_._parse_one_company_info(**kwargs))
        pprint(res)
    except Exception as e:
        print(e)
    finally:
        try:
            loop.close()
        except:
            pass

if __name__ == '__main__':
    init_spider()
    # test_parse_one_company_info()