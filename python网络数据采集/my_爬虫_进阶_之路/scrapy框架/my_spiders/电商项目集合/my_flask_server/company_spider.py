# coding:utf-8

'''
@author = super_fazai
@File    : company_spider.py
@connect : superonesfazai@gmail.com
'''

"""
企业商家信息爬虫

以实现:
    1. 天眼查
待实现
    1. 中国黄页
"""

from gc import collect

from settings import (
    MY_SPIDER_LOGS_PATH,
    COMPANY_ITEM_LIST,
    PHANTOMJS_DRIVER_PATH,
)
from my_items import CompanyItem
from sql_str_controller import (
    gs_insert_str_1,
    gs_select_str_1,)
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from multiplex_code import _get_new_db_conn

from requests import session
from datetime import datetime
from dateutil.parser import parse as date_util_parse
from fzutils.ip_pools import (
    fz_ip_pool,
    tri_ip_pool,)
from fzutils.data.list_utils import list_remove_repeat_dict
from fzutils.spider.selector import async_parse_field
from fzutils.spider.fz_driver import PHONE
from fzutils.spider.async_always import *

class CompanySpider(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            ip_pool_type=tri_ip_pool,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/companys/_/'
        )
        # 并发量, ty(推荐: 5)高并发被秒封-_-! 慢慢抓
        self.concurrency = 10
        assert 100 > self.concurrency, 'self.concurrency并发量不允许大于100!'
        self.sema = Semaphore(self.concurrency)
        # 设置天眼查抓取截止页数(查询限制5000个) max 250页
        self.ty_max_page_num = 250
        # 设置企查查抓取截止页数
        self.qcc_max_page_num = 2000
        # hy抓取开始company_id
        self.hy_min_company_id = 1000
        # 设置hy抓取截止company_id(20000000)(直接写20000000, 程序会卡死)
        self.hy_max_company_id = 100000
        self.sql_server_cli = SqlServerMyPageInfoSaveItemPipeline()
        self._set_province_code_list_and_city_code_list()
        self.ty_cookies_dict = {}
        # ty robot
        self.ty_robot = False
        # 存储的sql_str
        self.insert_into_sql = gs_insert_str_1
        # driver path
        self.driver_path = PHANTOMJS_DRIVER_PATH
        # driver timeout
        self.driver_timeout = 20

    def _set_province_code_list_and_city_code_list(self) -> None:
        '''
        获取province, city的code
        :return:
        '''
        sql_str = '''select c_name, code, parent_code from dbo.Region'''
        self.province_and_city_code_list = []
        self.lg.info('正在获取province_and_city_code_list...')
        try:
            self.province_and_city_code_list = self.sql_server_cli._select_table(sql_str=sql_str, params=None)
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)

        assert self.province_and_city_code_list != [], 'self.province_and_city_code_list为空list!'
        self.lg.info('获取province_and_city_code_list成功!')

    async def _fck_run(self) -> None:
        await self._company_spider(short_name='hy')

    async def _company_spider(self, short_name:str) -> None:
        '''
        公司 or 商家信息爬虫
        :return:
        '''
        if short_name == 'ty':
            # vip(1年360) 会员才能查看多页的企业信息内容, 而且vip每天只能查看5000家公司, 真抠-_-!, pass
            await self._ty_spider()

        elif short_name == 'qcc':
            await self._qcc_spider()

        elif short_name == 'hy':
            await self._hy_spider()

        else:
            raise NotImplemented

    async def _hy_spider(self):
        '''
        黄页spider(采用穷举采集的方式)
        :return:
        '''
        self.db_hy_unique_id_list = await self._get_hy_db_unique_id_list()
        await self._crawl_hy_company_info()

    async def _get_hy_db_unique_id_list(self) -> list:
        '''
        获取db中的unique id list
        :return:
        '''
        self.lg.info('正在获取db中的hy的unique_id...')
        try:
            res = self.sql_server_cli._select_table(sql_str=gs_select_str_1, params=None, logger=self.lg)
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            return []
        self.lg.info('hy的unique_id获取成功!')

        return [item[0] for item in res]

    async def _crawl_hy_company_info(self, **kwargs):
        '''
        抓取黄页的公司信息
        :return:
        '''
        async def _get_tasks_params_list() -> list:
            '''得到tasks params list'''
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

        all_res = []
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
                self.lg.info('create task[where company_id:{}]...'.format(company_id))
                tasks.append(self.loop.create_task(self._parse_one_company_info(
                    short_name='hy',
                    company_id=company_id,
                    company_url=company_url)))

            one_res = await async_wait_tasks_finished(tasks=tasks)
            for i in one_res:
                index += 1
                if i != {}:
                    # all_res.append(i)
                    await self._save_company_item(
                        company_item=i,
                        index=index)

            await async_sleep(2.)

    async def _ty_spider(self) -> None:
        '''
        天眼查企业信息爬虫
        :return:
        '''
        if self.ty_cookies_dict == {}:
            await self._ty_login()

        province_and_city_info = await self._get_ty_province_and_city_info()
        pprint(province_and_city_info)
        await self._crawl_ty_company_info(province_and_city_info=province_and_city_info)

    async def _ty_login(self) -> dict:
        '''
        天眼模拟登陆
        :return: 登陆后的cookies
        '''
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
        '''
        得到天眼查省份, 城市信息
        :return:
        '''
        async def _parse_info(body) -> list:
            '''页面解析'''
            async def _get_zhixia_city_info() -> list:
                '''获取直辖市信息'''
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
                '''获取其他省份的信息'''
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
            '''删除不抓取的地区'''
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
        '''
        企查查企业信息爬虫
        :return:
        '''
        province_and_city_info = await self._get_qcc_province_and_city_info()
        pprint(province_and_city_info)
        await self._crawl_qcc_company_info(province_and_city_info=province_and_city_info)

    async def _get_qcc_province_and_city_info(self) -> list:
        '''
        获取企查查省份信息
        :return:
        '''
        async def _parse_info() -> list:
            '''页面解析'''
            async def _get_area_info() -> list:
                '''得到区域信息'''
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
            '''删除不抓取的地区'''
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
        '''
        在天眼查中抓取待采集的目标
        :param kwargs:
        :return:
        '''
        async def _get_tasks_params_list(item) -> list:
            '''获取tasks_params_list'''
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
        '''
        ty抓取异常的处理
        :return:
        '''
        fail_count:int = kwargs['fail_count']
        one_res_len:int = kwargs['one_res_len']
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
        '''
        在企查查中抓取待采集的目标
        :return:
        '''
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
        '''
        抓取ty单页信息
        :param kwargs:
        :return:
        '''
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
        '''
        获取ty的待抓取的city_list(只抓取city)
        :param province_and_city_info:
        :return: [{'city_name': 'xxx', 'province_name': 'xxx', 'city_url': 'xxx'}, ...]
        '''
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
        '''
        抓取企查查单页信息
        :return: [] or [{'company_url': 'xxxx',}, ...]
        '''
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
        '''
        筛选出经营状态正常的company_url(公司状态异常的处理)
        :param body: 待解析的body
        :return: (_:未处理前的, _new:处理后的)
        '''
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
        '''
        从搜索页中解析company_url和company_status
        :param parser_obj: 解析对象
        :param target_obj: 待解析目标
        :return:
        '''
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
        '''
        根据company_url 分块抓取(eg: 企查查, 天眼查)的所有页面详情
        :return:
        '''
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
        '''
        得到分块抓取多公司信息的tasks_params_list
        :param short_name:
        :return:
        '''
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
        '''
        解析单页的信息
        :return: {} or {xxx}
        '''
        province_name = kwargs.get('province_name', '')
        company_url = kwargs.get('company_url', '')
        short_name = kwargs['short_name']
        city_name = kwargs.get('city_name', '')
        company_id = kwargs.get('company_id', '')

        company_html = await self._get_someone_company_page_html(
            short_name=short_name,
            company_url=company_url,
            company_id=company_id,)
        # self.lg.info(str(company_html))
        if company_html == '':
            return {}

        parser_obj = await self._get_parser_obj(short_name=short_name)
        try:
            unique_id = await self._get_company_unique_id(parser_obj=parser_obj, target_obj=company_url)
            company_name = await self._get_company_name(parser_obj=parser_obj, target_obj=company_html)
            company_link = await self._get_company_link(parser_obj=parser_obj, target_obj=company_html)
            legal_person = await self._get_legal_person(parser_obj=parser_obj, target_obj=company_html)
            phone = await self._get_phone(parser_obj=parser_obj, target_obj=company_html)
            email_address = await self._get_email_address(parser_obj=parser_obj, target_obj=company_html)
            address = await self._get_address(parser_obj=parser_obj, target_obj=company_html)
            brief_introduction = await self._get_brief_introduction(parser_obj=parser_obj, target_obj=company_html)
            business_range = await self._get_business_range(parser_obj=parser_obj, target_obj=company_html)
            founding_time = await self._get_founding_time(parser_obj=parser_obj, target_obj=company_html)
            province_id = await self._get_province_id(parser_obj=parser_obj, target_obj=company_html, province_name=province_name)
            city_id = await self._get_city_id(parser_obj=parser_obj, target_obj=company_html, city_name=city_name)
            employees_num = await self._get_employees_num(parser_obj=parser_obj, target_obj=company_html)
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
        company_item['employees_num'] = employees_num
        company_item['create_time'] = get_shanghai_time()
        company_item['site_id'] = await self._get_site_id(short_name=short_name)
        # pprint(company_item)

        self.lg.info('[{}] task[where province_name:{}, city_name:{}, company_url:{}]'.format(
            '+',
            province_name,
            city_name,
            company_url,))

        return dict(company_item)

    async def _get_site_id(self, short_name) -> int:
        '''
        获取采集源site_id
        :param short_name:
        :return:
        '''
        if short_name == 'qcc':
            site_id = 3
        elif short_name == 'ty':
            site_id = 1
        elif short_name == 'hy':
            site_id = 2
        else:
            raise NotImplemented('site_id没有实现!')

        return site_id

    async def _save_company_item(self, company_item, index) -> bool:
        '''
        异步存储company_item
        :param company_item:
        :return:
        '''
        async def _get_args() -> list:
            '''获取args'''
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
        '''
        公司人数
        :param parser_obj:
        :param target_obj:
        :return:
        '''
        if parser_obj['short_name'] == 'hy':
            employees_num = await self._get_hy_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='员工人数')
        else:
            employees_num = await async_parse_field(
                parser=parser_obj['employees_num'],
                target_obj=target_obj,
                logger=self.lg)

        return employees_num

    async def _get_company_name(self, parser_obj, target_obj) -> str:
        '''
        得到企业名称
        :param parser_obj:
        :param target_obj:
        :return:
        '''
        if parser_obj['short_name'] == 'hy':
            company_name = await self._get_hy_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='公司名称')
        else:
            company_name = await async_parse_field(parser=parser_obj['company_name'], target_obj=target_obj, logger=self.lg)

        assert company_name != '', 'company_name为空值!'

        return company_name

    async def _get_company_link(self, parser_obj, target_obj) -> str:
        '''
        得到企业官网地址
        :param parser_obj:
        :param target_obj:
        :return:
        '''
        if parser_obj['short_name'] == 'hy':
            company_link = await self._get_hy_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='公司网站',)
        else:
            company_link = await async_parse_field(parser=parser_obj['company_link'], target_obj=target_obj, logger=self.lg)

        # 可为空值
        # assert company_link != '', 'company_link为空值!'

        return company_link

    async def _get_legal_person(self, parser_obj, target_obj) -> str:
        '''
        获取法人
        :param parser_obj:
        :param target_obj:
        :return:
        '''
        if parser_obj['short_name'] == 'hy':
            legal_person = await self._get_hy_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='企业法人',)
        else:
            legal_person = await async_parse_field(parser=parser_obj['legal_person'], target_obj=target_obj, logger=self.lg)

        # 法人可以为空, eg: https://www.tianyancha.com/company/2876734
        # 但是本爬虫不采集法人为空的高端企业! $_$
        # hy 可空
        # assert legal_person != '', 'legal_person为空值!'

        return legal_person

    async def _get_phone(self, parser_obj, target_obj) -> list:
        '''
        获取phone
        :param parser_obj:
        :param target_obj:
        :return:
        '''
        if parser_obj['short_name'] == 'hy':
            phone = await self._get_hy_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='公司电话',)
        else:
            phone = await async_parse_field(parser=parser_obj['phone'], target_obj=target_obj, logger=self.lg)

        # assert phone != '', 'phone为空值!'
        if phone == '':
            return []

        if parser_obj['short_name'] == 'ty':
            phone_list = json_2_dict(phone, default_res=[])
            phone_list = [{
                'phone': i,
            } for i in phone_list]

        else:
            phone_list = [{
                'phone': phone,
            }]

        # 去重
        phone_list = list_remove_repeat_dict(target=phone_list, repeat_key='phone')

        return phone_list

    async def _get_email_address(self, parser_obj, target_obj) -> list:
        '''
        获取email
        :return:
        '''
        if parser_obj['short_name'] == 'hy':
            email_address = await self._get_hy_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='公司邮箱',)
        else:
            is_first = True
            if parser_obj['short_name'] == 'ty':
                is_first = False

            email_address = await async_parse_field(parser=parser_obj['email_address'], target_obj=target_obj, logger=self.lg, is_first=is_first)

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

        else:   # 只允许有一个，并且只取第一个
            return [{
                'email_address': new_email_address,
            }]

    async def _get_address(self, parser_obj, target_obj) -> str:
        '''
        获取address
        :param parser_obj:
        :param target_obj:
        :return:
        '''
        is_first = True
        if parser_obj['short_name'] == 'ty'\
                or parser_obj['short_name'] == 'hy':
            is_first = False

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

    async def _get_brief_introduction(self, parser_obj, target_obj) -> str:
        '''
        获取company简介
        :param parser_obj:
        :param target_obj:
        :return:
        '''
        brief_introduction = await async_parse_field(parser=parser_obj['brief_introduction'], target_obj=target_obj, logger=self.lg)
        if parser_obj['short_name'] == 'hy':
            brief_introduction = re.compile('<br>|<a.*?>|</a>').sub(' ', brief_introduction)

        # 可为空值
        # assert brief_introduction != '', 'brief_introduction为空值!'

        return await self._wash_data(brief_introduction)

    async def _get_business_range(self, parser_obj, target_obj):
        '''
        获取business_range
        :param parser_obj:
        :param target_obj:
        :return:
        '''
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

        assert business_range != '', 'business_range为空值!'

        return await self._wash_data(business_range)

    async def _wash_data(self, data):
        '''
        清洗data
        :return:
        '''
        replace_str_list = [
            ('&lt;', '<'),
            ('&gt;', '>')
        ]
        add_sensitive_str_list = ['\u3000', '\xa0', '&nbsp;']

        return wash_sensitive_info(
            data=data,
            replace_str_list=replace_str_list,
            add_sensitive_str_list=add_sensitive_str_list)

    async def _get_founding_time(self, parser_obj, target_obj):
        '''
        获取company成立时间
        :param parser_obj:
        :param target_obj:
        :return:
        '''
        if parser_obj['short_name'] == 'hy':
            founding_time = await self._get_hy_li_text_by_label_name(
                parser_obj=parser_obj,
                target_obj=target_obj,
                label_name='成立时间',)
            # self.lg.info('founding_time:{}'.format(founding_time))
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
        else:
            pass

        assert founding_time != '', 'founding_time为空值!'

        return founding_time

    async def _get_company_unique_id(self, parser_obj, target_obj):
        '''
        获取company 唯一的id
        :param parser_obj:
        :param target_obj:
        :return:
        '''
        unique_id = await async_parse_field(parser=parser_obj['unique_id'], target_obj=target_obj, logger=self.lg)
        assert unique_id != '', 'unique_id为空值!'

        if parser_obj['short_name'] == 'hy':
            unique_id = 'hy' + unique_id

        return unique_id

    async def _get_province_id(self, parser_obj, target_obj, province_name):
        '''
        获取对应的省份code
        :return:
        '''
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

        for item in self.province_and_city_code_list:
            c_name = item[0]
            code = item[1]
            if province_name in c_name:
                return code

        raise AssertionError('未知的province_name:{}, db中未找到!'.format(province_name))

    async def _get_city_id(self, parser_obj, target_obj, city_name) -> str:
        '''
        获取对应的city的code
        :param city_name:
        :return: '' or not ''
        '''
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

        for item in self.province_and_city_code_list:
            c_name = item[0]
            code = item[1]
            if city_name in c_name:
                return code

        # 可以为空, 企查查的为空
        # raise AssertionError('未知的city_name:{}, db中未找到!'.format(city_name))

        return ''

    async def _get_hy_li_text_by_label_name(self, parser_obj, target_obj, label_name):
        '''
        根据label_name 获取其对应的值
        :param label_name:
        :return:
        '''
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
        '''
        对应获取某个公司的html
        :return:
        '''
        short_name = kwargs['short_name']
        company_url = kwargs['company_url']
        company_id = kwargs['company_id']

        if short_name == 'qcc':
            return await self._get_qcc_company_page_html(company_url=company_url)

        elif short_name == 'ty':
            return await self._get_ty_company_page_html(company_url=company_url)

        elif short_name == 'hy':
            return await self._get_hy_company_page_html(company_id=company_id)

        else:
            raise NotImplemented

    async def _get_hy_company_page_html(self, company_id) -> str:
        '''
        获取hy某个company的html
        :param company_id:
        :return:
        '''
        detail_url = 'http://m.huangye88.com/gongsi/{}/detail.html'.format(company_id)
        contact_url = 'http://m.huangye88.com/gongsi/{}/contact.html'.format(company_id)
        headers = await self._get_phone_headers()
        # requests老是无数据, 改用驱动
        # body_1 = await unblock_request(url=detail_url, headers=headers, ip_pool_type=self.ip_pool_type)
        body_1 = await unblock_request_by_driver(
            executable_path=self.driver_path,
            url=detail_url,
            user_agent_type=PHONE,
            ip_pool_type=self.ip_pool_type,
            logger=self.lg)
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
            logger=self.lg)
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
        '''
        获取天眼查某个company的html
        :param company_url:
        :return:
        '''
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
        '''
        获取到企查查某个company的html
        :param company_url:
        :return:
        '''
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
        '''
        解析一个地域信息
        :return:
        '''
        async def _get_province_name():
            '''省份'''
            province_name = await async_parse_field(
                parser=province_city_info_selector['province_name'],
                target_obj=item,
                is_first=province_name_is_first,
                logger=self.lg)
            assert province_name != '', 'province_name为空值!'

            return province_name

        async def _get_province_url():
            '''省份url'''
            province_url = await async_parse_field(
                parser=province_city_info_selector['province_url'],
                target_obj=item,
                is_first=province_url_is_first,
                logger=self.lg)
            assert province_url != '', 'province_url为空值!'

            return province_url

        async def _get_city_name_list() -> list:
            '''省份下面的市'''
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
            '''省份下面市的url'''
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
        '''
        得到解析对象
        :param short_name:
        :return:
        '''
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
    async def _get_crawl_province_area() -> list:
        '''
        抓取的省份
        :return:
        '''
        return ['北京', '天津', '上海', '重庆', '河北', '辽宁', '江苏', '浙江', '山东', '湖北', '广东']

    @staticmethod
    async def _get_crawl_city_area() -> list:
        '''
        抓取的城市
        :return:
        '''
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

if __name__ == '__main__':
    _ = CompanySpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())



