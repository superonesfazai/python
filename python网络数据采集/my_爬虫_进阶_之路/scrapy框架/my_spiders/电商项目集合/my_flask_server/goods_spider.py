# coding:utf-8

'''
@author = super_fazai
@File    : goods_spider.py
@connect : superonesfazai@gmail.com
'''

"""
goods spider
"""

from gc import collect

from settings import (
    PHANTOMJS_DRIVER_PATH,
    MY_SPIDER_LOGS_PATH,
    IP_POOL_TYPE,
    GOODS_ITEM_LIST,)
from sql_str_controller import (
    al_select_str_1,
    al_update_str_1,
    al_update_str_2,
    al_insert_str_1,
    al_insert_str_2,)
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from fzutils.spider.selector import async_parse_field
from fzutils.spider.async_always import *

class GoodsSpider(AsyncCrawler):
    def __init__(self, short_name:str, logger=None, *params, **kwargs):
        self.parser_obj = self._get_parser_obj(short_name=short_name)
        AsyncCrawler.__init__(
            *params,
            **kwargs,

            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=logger,
            log_save_path=self.parser_obj['log_save_path'],

            is_use_driver=self.parser_obj['is_use_driver'],
            driver_type=self.parser_obj['driver_type'],
            driver_executable_path=self.parser_obj['driver_executable_path'],
            user_agent_type=self.parser_obj['user_agent_type']
        )
        self.result_data = {}
        # al 活动goods
        self.is_activity_goods = False

    async def _get_goods_data(self):
        '''
        获取goods data
        :return:
        '''
        pass

    async def _parse_goods_data(self, goods_url:str):
        '''
        解析goods data
        :param goods_url:
        :return:
        '''
        try:
            goods_id:(str, list, tuple) = await self._get_goods_id_from_url(goods_url=goods_url)
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            return await self._data_error_init()

        if not (await self._judge_goods_id_is_error(goods_id=goods_id)):
            return await self._data_error_init()

        if isinstance(goods_id, str):
            goods_id = goods_id
        else:
            goods_id = goods_id[0]

        m_goods_url = await self._get_m_goods_url(goods_id=goods_id)
        self.error_base_record = await self._get_error_base_record(goods_id=goods_id)

        goods_html = await self._get_someone_goods_page_html(
            m_goods_url=m_goods_url,
            goods_id=goods_id)
        if goods_html == '':
            self.lg.error('获取的body为空值!' + self.error_base_record)
            return await self._data_error_init()

        # TODO 先不重构
        pull_off_shelves_res = await self._goods_is_pull_off_shelves(body=goods_html, goods_id=goods_id)
        if isinstance(pull_off_shelves_res, dict):
            return pull_off_shelves_res

    async def _goods_is_pull_off_shelves(self, body, goods_id) -> (bool, dict, None):
        '''
        首先通过body, 来查看是否能直接判断该商品已下架
        :param body:
        :return:
        '''
        async def _judge_al() -> (dict, None):
            '''判断al'''
            pull_off_shelves = Selector(text=body).css('div.d-content p.info::text').extract_first() or ''
            if pull_off_shelves == '该商品无法查看或已下架':  # 表示商品已下架, 同样执行插入数据操作
                return await self._handle_al_goods_is_delete(goods_id=goods_id)
            else:
                return None

        short_name = self.parser_obj['short_name']
        if short_name == 'al':
            return await _judge_al()
        else:
            return None

    async def _handle_al_goods_is_delete(self, goods_id) -> dict:
        '''
        处理商品无法查看或者下架的
        :return:
        '''
        try:
            sql_cli = SqlServerMyPageInfoSaveItemPipeline()
            is_in_db = sql_cli._select_table(sql_str=al_select_str_1, params=(str(goods_id),))
            # self.lg.info(str(is_in_db))
        except Exception:
            self.lg.error('数据库连接失败!' + self.error_base_record, exc_info=True)
            return await self._data_error_init()

        self.result_data = {}
        # 初始化下架商品的属性
        tmp_data_s = await self._init_al_pull_off_shelves_goods()
        if is_in_db != []:
            # 表示该goods_id以前已被插入到db中, 于是只需要更改其is_delete的状态即可
            sql_cli._update_table_2(sql_str=al_update_str_1, params=(goods_id), logger=self.lg)
            self.lg.info('@@@ 该商品goods_id原先存在于db中, 此处将其is_delete=1')
            # 用来判断原先该goods是否在db中
            tmp_data_s['before'] = True

        else:
            # 表示该goods_id没存在于db中
            self.lg.info('@@@ 该商品已下架[但未存在于db中], ** 此处将其插入到db中...')
            tmp_data_s['before'] = False

        return tmp_data_s

    async def _init_al_pull_off_shelves_goods(self) -> dict:
        '''
        初始化al原先就下架的商品信息
        :return:
        '''
        is_delete = 1
        result = {
            'company_name': '',         # 公司名称
            'title': '',                # 商品名称
            'link_name': '',            # 卖家姓名
            'price_info': [],           # 商品价格信息, 及其对应起批量
            'price': 0,
            'taobao_price': 0,
            'sku_props': [],            # 标签属性名称及其对应的值  (可能有图片(url), 无图(imageUrl=None))
            'sku_map': [],              # 每个规格对应价格, 及其库存量
            'all_img_url': [],          # 所有示例图片地址
            'property_info': [],        # 详细信息的标签名, 及其对应的值
            'detail_info': '',          # 下方详细div块
            'is_delete': is_delete,     # 判断是否下架
        }

        return result

    async def _get_someone_goods_page_html(self, **kwargs):
        '''
        获取主信息
        :param kwargs:
        :return:
        '''
        m_goods_url = kwargs.get('m_goods_url', '')
        goods_id:str = kwargs.get('goods_id', '')
        short_name = self.parser_obj['short_name']

        if short_name == 'al':
            return await self._get_al_goods_html(
                m_goods_url=m_goods_url,
                goods_id=goods_id)

        else:
            raise NotImplemented('获取goods_html没有实现!')

    async def _get_al_goods_html(self, m_goods_url, goods_id) -> str:
        '''
        获取al的goods的html
        :param m_goods_url:
        :param goods_id:
        :return:
        '''
        body = self.driver.get_url_body(
            url=m_goods_url,)
        # css_selector='div.d-content',)

        # 改用requests
        # body = Requests.get_url_body(
        #     url=m_goods_url,
        #     headers=self._get_phone_headers(),
        #     ip_pool_type=self.ip_pool_type,)
        # self.lg.info(str(body))

        return body

    async def _get_error_base_record(self, goods_id) -> str:
        '''
        得到异常是待记录的base参数
        :return:
        '''
        error_base_record = '出错goods_id:{0}'.format(goods_id)

        return error_base_record

    async def _get_m_goods_url(self, goods_id):
        '''
        获取对应m站url
        :param goods_id:
        :return:
        '''
        short_name = self.parser_obj['short_name']
        if short_name == 'al':
            m_goods_url = 'https://m.1688.com/offer/{}.html'.format(goods_id)

        else:
            raise NotImplemented('获取对应m_goods_url失败!')

        self.lg.info('------>>>| 待处理的{}地址为: {}'.format(short_name, m_goods_url))

        return m_goods_url

    async def _judge_goods_id_is_error(self, goods_id) -> bool:
        '''
        判断goods_id是否异常
        :param goods_id:
        :return:
        '''
        if (isinstance(goods_id, str) and goods_id == '') \
                or (isinstance(goods_id, tuple) and goods_id == ()) \
                or (isinstance(goods_id, list) and goods_id == []):
            return False
        else:
            return True

    async def _data_error_init(self) -> dict:
        self.result_data = {}

        return {}

    async def _get_goods_id_from_url(self, goods_url:str) -> (str, list, tuple):
        '''
        从goods_url获取goods_id
        :param goods_url:
        :return:
        '''
        goods_id_info = self.parser_obj['goods_id_info']
        is_first = True

        goods_id = await async_parse_field(
            parser=goods_id_info['goods_id'],
            target_obj=goods_url,
            is_first=is_first,
            logger=self.lg,)

        assert goods_id != '获取到的goods_id为空值!'

        return goods_id

    @staticmethod
    def _get_parser_obj(short_name) -> dict:
        '''
        得到解析对象
        :param short_name:
        :return:
        '''
        parser_obj = None
        for item in GOODS_ITEM_LIST:
            if item['short_name'] == short_name:
                parser_obj = item
        assert parser_obj is not None, 'parser_obj为None!'

        return parser_obj

    async def async_get_parser_obj(self, short_name):
        return self._get_parser_obj(short_name=short_name)

    def __del__(self):
        try:
            del self.driver
        except:
            pass
        try:
            del self.lg
        except:
            pass
        try:
            del self.result_data
        except:
            pass
        collect()

if __name__ == '__main__':
    _ = GoodsSpider(short_name='al')
    loop = get_event_loop()
    while True:
        url = input('请输入要爬取的商品界面地址(以英文分号结束): ').strip('\n').strip(';')
        res = loop.run_until_complete(_._parse_goods_data(goods_url=url))
