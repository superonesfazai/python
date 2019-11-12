# coding:utf-8

'''
@author = super_fazai
@File    : goods_keywords_spider.py
@Time    : 2018/6/5 11:40
@connect : superonesfazai@gmail.com
'''
import sys
sys.path.append('..')

from urllib.parse import quote_plus

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from taobao_parse import TaoBaoLoginAndParse
from ali_1688_parse import ALi1688LoginAndParse
from tmall_parse_2 import TmallParse
from jd_parse import JdParse

from settings import (
    IS_BACKGROUND_RUNNING,
    MY_SPIDER_LOGS_PATH,
    TAOBAO_REAL_TIMES_SLEEP_TIME,
    IP_POOL_TYPE,
)

from sql_str_controller import (
    kw_insert_str_1,
    kw_select_str_1,
    kw_select_str_2,
    kw_select_str_3,
    kw_select_str_4,
    kw_insert_str_2,
)
from multiplex_code import _block_get_new_db_conn

from fzutils.spider.selector import parse_field
from fzutils.data.excel_utils import read_info_from_excel_file
from fzutils.spider.async_always import *

class GoodsKeywordsSpider(AsyncCrawler):
    def __init__(self):
        super(GoodsKeywordsSpider, self).__init__(
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            logger=None,
            log_save_path=MY_SPIDER_LOGS_PATH + '/goods_keywords/_/',
        )
        self.msg = ''
        self.debugging_api = self._init_debugging_api()
        self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        # 插入数据到goods_id_and_keyword_middle_table表
        self.add_keyword_id_for_goods_id_sql_str = kw_insert_str_1
        self.req_num_retries = 7

    def _init_debugging_api(self):
        '''
        用于设置crawl的关键字热销商品的site_id
        :return: dict
        '''
        return {
            1: True,   # 淘宝
            2: False,   # 阿里1688
            3: True,   # 天猫
            4: False,   # 京东
        }

    async def _fck_run(self):
        # 存入pc tb的主分类keywords
        # target_keywords_list = self.get_pc_tb_sort_keywords_list()
        # assert target_keywords_list != []
        # self.add_new_keywords_list_2_db(target_list=target_keywords_list)

        pass

    def _just_run(self):
        while True:
            result = None
            result_2 = None
            # 获取原先goods_db的所有已存在的goods_id
            try:
                result = list(self.sql_cli._select_table(sql_str=kw_select_str_1))
                self.lg.info('正在获取db中已存在的goods_id...')
                result_2 = list(self.sql_cli._select_table(sql_str=kw_select_str_2))
                self.lg.info('db中已存在的goods_id获取成功!')
            except TypeError:
                self.lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')

            if result is None or result_2 is None:
                sleep(15)
                continue

            self.lg.info('db 已存在的goods_id_num: {}'.format(len(result_2)))
            # 用于定位增加商品的个数
            self.add_goods_index = 0
            self.db_existed_goods_id_list = [item[0] for item in result_2]
            # 即时释放资源
            try:
                del result_2
            except:
                pass
            collect()

            for item in result:
                keyword_id = item[0]
                keyword = item[1]
                # 每个关键字在True的接口都抓完, 再进行下一次
                self.lg.info('正在处理id为{0}, 关键字为 {1} ...'.format(keyword_id, keyword))
                # 筛选
                if int(keyword_id) < 43:
                    if int(keyword_id) not in (25, 26):
                        self.lg.info('不在处理的keyword_id范围内, keyword_id: {}, keyword: {}'.format(
                            keyword_id,
                            keyword))
                        continue
                    else:
                        pass
                else:
                    pass

                for type, type_value in self.debugging_api.items():
                    # 遍历待抓取的电商分类
                    if type_value is False:
                        self.lg.info('api为False, 跳过!')
                        continue

                    self.sql_cli = _block_get_new_db_conn(
                        db_obj=self.sql_cli,
                        index=self.add_goods_index,
                        logger=self.lg,
                        remainder=20,)
                    goods_id_list = self._get_keywords_goods_id_list(
                        type=type,
                        keyword=item)
                    # pprint(goods_id_list)
                    self.lg.info('关键字为{0}, 获取到的goods_id_list_num: {1}'.format(keyword, len(goods_id_list)))
                    '''处理goods_id_list'''
                    self._deal_with_goods_id_list(
                        type=type,
                        goods_id_list=goods_id_list,
                        keyword_id=keyword_id)
                    sleep(3)

    @catch_exceptions_with_class_logger(default_res=[])
    def get_pc_tb_sort_keywords_list(self) -> list:
        """
        获取pc tb 关键字
        :return:
        """
        # 存入数量较小, 避免长期增量导致后期更新量大
        headers = get_random_headers(
            connection_status_keep_alive=False,
            cache_control='',
        )
        body = Requests.get_url_body(
            url='https://www.taobao.com/',
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.req_num_retries,
            proxy_type=PROXY_TYPE_HTTPS,)
        assert body != ''
        # self.lg.info(body)

        # 只获取主分类的关键字
        main_sort_key_list_sel = {
            'method': 'css',
            'selector': 'ul.service-bd li a ::text',
        }
        main_sort_list_key = parse_field(
            parser=main_sort_key_list_sel,
            target_obj=body,
            is_first=False,
            logger=self.lg,
        )
        # pprint(main_sort_list_key)

        # 不需要的
        not_need_main_sort_key_tuple = (
            '卡券',
            '本地服务',
            'DIY',
            '二手车',
            '生鲜',
            '鲜花',
        )
        main_sort_list_key = list(tuple([item for item in main_sort_list_key if item not in not_need_main_sort_key_tuple]))
        # pprint(main_sort_list_key)

        return main_sort_list_key

    @catch_exceptions_with_class_logger(default_res=[])
    def get_db_keywords_list(self) -> list:
        """
        获取db keyword
        :return:
        """
        self.lg.info('正在读取db中原先的keyword...')
        db_res = self.sql_cli._select_table(sql_str=kw_select_str_4)
        res = [i[0] for i in db_res]
        self.lg.info('db keywords 读取完毕!')

        return res

    def add_new_keywords_list_2_db(self, target_list: list):
        """
        往db插入新的key
        :param target_list:
        :return:
        """
        db_keywords_List = self.get_db_keywords_list()
        for keyword in target_list:
            if keyword in db_keywords_List:
                self.lg.info('该关键字{0}已经存在于db中...'.format(keyword))
                continue

            self.lg.info('------>>>| 正在存储关键字 {0}'.format(keyword))
            self.sql_cli._insert_into_table_2(
                sql_str=kw_insert_str_2,
                params=(
                    str(keyword),
                    0
                ),
                logger=self.lg,)

        self.lg.info('全部写入完毕!')

    def _get_keywords_goods_id_list(self, type, keyword):
        '''
        获取goods_id_list
        :param type: 电商种类
        :param keyword:
        :return:
        '''
        if type == 1:
            self.lg.info('下面是淘宝的关键字采集...')
            goods_id_list_0 = self._get_taobao_goods_keywords_goods_id_list(
                keyword=keyword,
                sort_order=0,)
            goods_id_list_1 = self._get_taobao_goods_keywords_goods_id_list(
                keyword=keyword,
                sort_order=1,)
            # 理论不重复
            goods_id_list = goods_id_list_0 + goods_id_list_1

        elif type == 2:
            self.lg.info('下面是阿里1688的关键字采集...')
            goods_id_list = self._get_1688_goods_keywords_goods_id_list(keyword=keyword)
        elif type == 3:
            self.lg.info('下面是天猫的关键字采集...')
            # goods_id_list_0 = []
            goods_id_list_0 = self._get_tmall_goods_keywords_goods_id_list(
                keyword=keyword,
                sort_order=0)
            goods_id_list_1 = self._get_tmall_goods_keywords_goods_id_list(
                keyword=keyword,
                sort_order=1)
            # 理论不重复
            goods_id_list = goods_id_list_0 + goods_id_list_1

        elif type == 4:
            self.lg.info('下面是京东的关键字采集...')
            goods_id_list = self._get_jd_goods_keywords_goods_id_list(keyword=keyword)

        else:
            goods_id_list = []

        return goods_id_list

    def _deal_with_goods_id_list(self, **kwargs):
        '''
        分类执行代码
        :param kwargs:
        :return:
        '''
        type = kwargs.get('type', '')
        goods_id_list = kwargs.get('goods_id_list', [])
        keyword_id = kwargs.get('keyword_id', '')

        if type == 1:
            self._taobao_keywords_spider(goods_id_list=goods_id_list, keyword_id=keyword_id)
        elif type == 2:
            self._1688_keywords_spider(goods_id_list=goods_id_list, keyword_id=keyword_id)
        elif type == 3:
            self._tmall_keywords_spider(goods_id_list=goods_id_list, keyword_id=keyword_id)
        elif type == 4:
            self._jd_keywords_spider(goods_id_list=goods_id_list, keyword_id=keyword_id)
        else:
            pass

        return None

    @catch_exceptions_with_class_logger(default_res=[])
    def _get_taobao_goods_keywords_goods_id_list(self, keyword, sort_order=0) -> list:
        '''
        获取该keywords的商品的goods_id_list
        :param keyword: (id, keyword)
        :param sort_order: 排序方式 0 销量排序 | 1 升序排序(低到高)
        :return: a list
        '''
        # headers = get_random_headers(
        #     connection_status_keep_alive=False,
        # )
        # headers.update({
        #     'authority': 's.taobao.com',
        # })
        # # todo cookie必须, 且一会就失效, pass, 利用滑块, 发现selenium被封, 原因被检测是爬虫, 可尝试puppeteer, 据说可过, 未尝试!
        # cookie_str = '_cc_=VT5L2FSpdA%3D%3D;_fbp=fb.1.1569654479622.763934285;_l_g_=Ug%3D%3D;_m_h5_tk=a4c9f506a939350748c4e25bf29c8128_1572415413630;_m_h5_tk_enc=e1f102c6dddbcf0449ee462808f953f3;_nk_=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA;_tb_token_=fdeefbbf3de98;cna=wRsVFTj6JEoCAXHXtCqXOzC7;cookie1=UR3Wq2iKhDJHTTOd%2FGn4oh0oxwBK8EUqK%2Bm%2Bxv62FEM%3D;cookie17=UUplY9Ft9xwldQ%3D%3D;cookie2=192786d411defc9125f286b621cdac13;csg=d4dcf16f;dnk=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA;enc=NMn7zFLrgU6nMXwgPWND42Y2H3tmKu0Iel59hu%2B7DFx27uPqGw349h4yvXidY3xuFC6%2FjozpnaTic5LC7jv8CA%3D%3D;existShop=MTU3MjQwNjk5Ng%3D%3D;hng=CN%7Czh-CN%7CCNY%7C156;isg=BIGB_l_6uGmc9tV022IPFHRhkMtbBvfIVeEd8OPWKgjNyqCcK_6NcSJIrH4pQo3Y;l=dBxRISnmvA2VASB2BOCi5uI8Us7tLIRfguPRwd0Xi_5wE6b91J7OkNsNfFv6cjWciGLB44YRE82TreEg8PwjJ0YEae1VivepCef..;lgc=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA;mt=ci=95_1;munb=2242024317;sg=%E4%BA%BA73;skt=d1bfc909e6c0d05f;t=593a350382a4f28aa3e06c16c39febf2;tg=0;thw=cn;tracknick=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA;uc1=cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&tag=8&cookie15=W5iHLLyFOGW7aA%3D%3D&existShop=false&lng=zh_CN&cookie14=UoTbnxzMUEsTqw%3D%3D&cookie21=U%2BGCWk%2F7ow0zmglPa33heg%3D%3D&pas=0;uc3=id2=UUplY9Ft9xwldQ%3D%3D&vt3=F8dByua36wqvCAMolFQ%3D&lg2=VT5L2FSpMGV7TQ%3D%3D&nk2=rUtEoY7x%2Bk8Rxyx1ZtN%2FAg%3D%3D;uc4=nk4=0%40r7rCNeQ4%2Bj7fAj%2BMcdPH4%2B0X9xH9JxJM8Qbr&id4=0%40U2gvLJ3%2BK6kqeorNX%2BPTq0q5%2BuB6;UM_distinctid=16a81fdddac71f-0115562d66ef2c-37667603-1fa400-16a81fdddad713;unb=2242024317;v=0;alitrackid=www.taobao.com;JSESSIONID=5ADA55015D51399ADAC375C30564AA33;lastalitrackid=www.taobao.com;x5sec=7b227365617263686170703b32223a22366330383530303265666535356132316162373131613863623535326462396143503274354f3046454d6974676669703150696638514561444449794e4449774d6a517a4d5463374d673d3d227d;'
        # headers.update({
        #     'cookie': cookie_str,
        # })
        # # 获取到的为淘宝关键字搜索按销量排名
        # params = (
        #     ('data-key', 'sort'),
        #     ('data-value', 'sale-desc'),
        #     ('ajax', 'true'),
        #     # ('_ksTS', '1528171408340_395'),
        #     ('callback', 'jsonp396'),
        #     ('q', keyword[1]),
        #     ('imgfile', ''),
        #     ('commend', 'all'),
        #     ('ssid', 's5-e'),
        #     ('search_type', 'item'),
        #     ('sourceId', 'tb.index'),
        #     # ('spm', 'a21bo.2017.201856-taobao-item.1'),
        #     ('ie', 'utf8'),
        #     # ('initiative_id', 'tbindexz_20170306'),
        # )
        # s_url = 'https://s.taobao.com/search'
        # body = Requests.get_url_body(
        #     url=s_url,
        #     headers=headers,
        #     params=params,
        #     ip_pool_type=self.ip_pool_type,
        #     proxy_type=PROXY_TYPE_HTTPS,
        #     num_retries=self.req_num_retries,)
        # assert body != ''
        #
        # try:
        #     data = re.compile('\((.*)\)').findall(body)[0]
        # except IndexError:
        #     self.lg.error('re获取淘宝data时出错, 出错关键字为{0}'.format(keyword[1]))
        #     return []
        #
        # data = json_2_dict(json_str=data, logger=self.lg)
        # if data == {}:
        #     self.lg.error('获取到的淘宝搜索data为空dict! 出错关键字为{0}'.format(keyword[1]))
        #     return []
        # else:
        #     slider_url = data.get('url', '')
        #     if 'search/_____tmd_____/punish' in slider_url:
        #         # 表明需要去滑动滑块
        #         print('需滑动滑块!')
        #         print('滑块地址: {}'.format(slider_url))
        #     else:
        #         print('无滑块')
        #
        #     goods_id_list = data\
        #         .get('mainInfo', {})\
        #         .get('traceInfo', {})\
        #         .get('traceData', {})\
        #         .get('allNids', [])
        #     if goods_id_list is None or goods_id_list == []:
        #         self.lg.error('获取淘宝搜索goods_id_list为空list! 出错关键字{0}'.format(keyword[1]))
        #         return []
        #     else:
        #         return goods_id_list[0:20]

        # m站搜索也得登录, 且只有第一页, cookies中的令牌1分钟内就失效

        # # 故采用三方领券网站的搜索
        # # 全优惠(https://www.quanyoubuy.com/)
        # headers = get_random_headers(
        #     connection_status_keep_alive=False,
        #     cache_control='',
        # )
        # headers.update({
        #     'authority': 'www.quanyoubuy.com',
        #     # 'referer': 'https://www.quanyoubuy.com/?m=search&a=index&k=%E5%A5%B3%E8%A3%85',
        # })
        # url = 'https://www.quanyoubuy.com/search/index/sort/hot/k/{}.html'.format(keyword[1])
        # body = Requests.get_url_body(
        #     url=url,
        #     headers=headers,
        #     ip_pool_type=self.ip_pool_type,
        #     proxy_type=PROXY_TYPE_HTTPS,
        #     num_retries=self.req_num_retries,)
        # assert body != ''
        # # self.lg.info(body)
        #
        # title_div_list_sel = {
        #     'method': 'css',
        #     'selector': 'h3.good-title a',
        # }
        # goods_url_sel = {
        #     'method': 'css',
        #     'selector': 'a ::attr("href")',
        # }
        # title_div_List = parse_field(
        #     parser=title_div_list_sel,
        #     target_obj=body,
        #     is_first=False,
        #     logger=self.lg,
        # )
        # goods_url_list = []
        # for item in title_div_List:
        #     try:
        #         if '<em class=\"d-icon\"></em>' in item:
        #             # 跳过京东优惠券
        #             continue
        #
        #         goods_url = parse_field(
        #             parser=goods_url_sel,
        #             target_obj=item,
        #             logger=self.lg,
        #         )
        #         assert goods_url != ''
        #         goods_url_list.append(goods_url)
        #     except AssertionError:
        #         continue
        #
        # assert goods_url_list != []
        # # pprint(goods_url_list)
        # goods_id_sel = {
        #     'method': 're',
        #     'selector': '/iid/(\d+)\.html',
        # }
        # res = []
        # for goods_url in goods_url_list:
        #     try:
        #         goods_id = parse_field(
        #             parser=goods_id_sel,
        #             target_obj=goods_url,
        #             logger=self.lg,
        #         )
        #         assert goods_id != ''
        #         if goods_id in self.db_existed_goods_id_list:
        #             self.lg.info('该goods_id[{}]已存在于db'.format(goods_id))
        #             continue
        #     except AssertionError:
        #         continue
        #
        #     res.append(goods_id)
        #
        # new_res = []
        # # 控制量只需要前25个(慢点 无所谓 太快 平台员工来不及操作 后期更新量也太大)(有部分主图不能用)
        # for goods_id in res[:25]:
        #     self.lg.info('判断goods_id[{}]是否为tb商品ing...'.format(goods_id))
        #     if self.judge_qyh_is_tb_by_goods_id(goods_id=goods_id) != 0:
        #         continue
        #
        #     new_res.append(goods_id)
        #
        # self.lg.info('其中tb goods num: {}'.format(len(new_res)))
        # collect()

        # 爱淘宝pc 版搜索页(https://ai.taobao.com/)
        headers = get_random_headers(
            connection_status_keep_alive=False,
            cache_control='',
        )
        headers.update({
            'authority': 'ai.taobao.com',
            # ori
            # 'referer': 'https://ai.taobao.com/search/index.htm?key=%E9%A3%9F%E5%93%81&pid=mm_10011550_0_0&union_lens=recoveryid%3A201_11.131.193.65_881154_1572572691432%3Bprepvid%3A201_11.131.193.65_881154_1572572691432&prepvid=200_11.27.75.93_347_1572572705164&sort=biz30day&spm=a231o.7712113%2Fj.1003.d2',
            'referer': 'https://ai.taobao.com/search/index.htm?key={}&sort=biz30day',
        })
        if sort_order == 0:
            self.lg.info('按销量排序')
            # 销量
            params = (
                ('key', keyword[1]),
                # ('pid', 'mm_10011550_0_0'),
                # ('union_lens', 'recoveryid:201_11.131.193.65_881154_1572572691432;prepvid:201_11.131.193.65_881154_1572572691432'),
                # ('prepvid', '200_11.27.75.94_1585_1572572718183'),
                ('sort', 'biz30day'),
                # ('spm', 'a231o.7712113/j.1003.d11'),
                ('taobao', 'true'),  # 勾选仅搜索tb
            )
        elif sort_order == 1:
            # 升序
            self.lg.info('按升序排序')
            params = (
                ('key', keyword[1]),
                ('taobao', 'true'),  # 勾选仅搜索tb
                ('sort', 'discount_price_incr'),
            )
        else:
            raise NotImplemented

        body = Requests.get_url_body(
            url='https://ai.taobao.com/search/index.htm',
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.req_num_retries,
            proxy_type=PROXY_TYPE_HTTPS, )
        assert body != ''
        # self.lg.info(body)

        page_res = re.compile('var _pageResult = (.*?);</script>').findall(body)[0]
        # self.lg.info(page_res)
        data = json_2_dict(
            json_str=page_res,
            default_res={},
            logger=self.lg,).get('result', {}).get('auction', [])
        # pprint(data)

        new_res = []
        for item in data:
            item_id = str(item.get('itemId', ''))
            if item_id != '':
                try:
                    this_price = float(item.get('realPrice', '0'))
                    if this_price < 8.8:
                        self.lg.info('该goods_id: {}, this_price: {}, 售价小于9元, pass'.format(item_id, this_price))
                        continue

                except Exception:
                    self.lg.error('遇到错误:', exc_info=True)
                    continue

                new_res.append(item_id)

        # boss说同一关键字重复太多, 取10个 此处取15个

        return new_res[:15]

    @catch_exceptions_with_class_logger(default_res=-1)
    def judge_qyh_is_tb_by_goods_id(self, goods_id):
        """
        根据商品id 判断是否是tb商品
        :param goods_id:
        :return: 0 tb|1 tm | -1 未知
        """
        headers = get_random_headers(
            connection_status_keep_alive=False,
            cache_control='',
        )
        headers.update({
            'authority': 'www.quanyoubuy.com',
        })
        url = 'https://www.quanyoubuy.com/item/index/iid/{}.html'.format(goods_id)
        body = Requests.get_url_body(
            url=url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            proxy_type=PROXY_TYPE_HTTPS,
            num_retries=7,)
        assert body != ''

        btn_text_sel = {
            'method': 'css',
            'selector': 'div.product-info a.go_btn span ::text',
        }
        btn_text = parse_field(
            parser=btn_text_sel,
            target_obj=body,
            is_print_error=False,
            logger=self.lg,
        )
        # self.lg.info(btn_text)
        assert btn_text != ''

        res = -1
        if '天猫' in btn_text:
            self.lg.info('goods_id: {}, tm good'.format(goods_id))
            res = 1
        elif '淘宝' in btn_text:
            self.lg.info('goods_id: {}, tb good'.format(goods_id))
            res = 0
        else:
            self.lg.info('goods_id: {}, 未知 good'.format(goods_id))
            pass

        return res

    def _get_1688_goods_keywords_goods_id_list(self, keyword):
        '''
        根据keyword获取1688销量靠前的商品信息
        :param keyword:
        :return: a list eg: ['11111', ...]
        '''
        '''方案1: 从m.1688.com搜索页面进行抓取, 只取第一页的销量排名靠前的商品'''
        headers = {
            'authority': 'm.1688.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': get_random_pc_ua(),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        }
        params = (
            ('sortType', 'booked'),
            ('filtId', ''),
            ('keywords', keyword[1]),
            ('descendOrder', 'true'),
        )
        url = 'https://m.1688.com/offer_search/-6161.html'
        body = Requests.get_url_body(url=url, headers=headers, params=params, ip_pool_type=self.ip_pool_type)
        # self.lg.info(str(body))
        if body == '':
            return []
        else:
            try:
                goods_id_list = Selector(text=body).css('div.list_group-item::attr("data-offer-id")').extract()
                # pprint(goods_id_list)
            except Exception as e:
                self.lg.exception(e)
                self.lg.error('获取1688搜索goods_id_list为空list! 出错关键字{0}'.format(keyword[1]))
                goods_id_list = []

        return goods_id_list

    @catch_exceptions_with_class_logger(default_res=[])
    def _get_tmall_goods_keywords_goods_id_list(self, keyword, sort_order=0) -> list:
        '''
        根据keyword获取tmall销量靠前的商品
        :param keyword:
        :param sort_order: 排序方式 0 销量 | 1 升序排序(低到高)
        :return: list eg: ['//detail.tmall.com/item.htm?id=566978017832&skuId=3606684772412', ...] 不是返回goods_id
        '''
        '''方案: tmall m站的搜索'''   # 搜索: 偶尔不稳定但是还是能用
        headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'user-agent': get_random_pc_ua(),
            'user-agent': get_random_phone_ua(),
            'accept': '*/*',
            # 'referer': 'https://list.tmall.com/search_product.htm?q=%B0%A2%B5%CF%B4%EF%CB%B9&type=p&spm=a220m.6910245.a2227oh.d100&from=mallfp..m_1_suggest&sort=d',
            'authority': 'list.tmall.com',
        }
        if sort_order == 0:
            self.lg.info('按销量排序')
            # 必须
            # 'referer': 'https://list.tmall.com/search_product.htm?q=%B0%A2%B5%CF%B4%EF%CB%B9&type=p&spm=a220m.6910245.a2227oh.d100&from=mallfp..m_1_suggest&sort=d',
            referer = 'https://list.tmall.com/search_product.htm?q={}&type=p&spm=a220m.6910245.a2227oh.d100&from=mallfp..m_1_suggest&sort=d'.format(
                quote_plus(keyword[1]))
            # print(referer)
            params = {
                'page_size': '20',
                'page_no': '1',
                'q': str(keyword[1]),
                'type': 'p',
                'spm': 'a220m.6910245.a2227oh.d100',
                'from': 'mallfp..m_1_suggest',
                'sort': 'd',
            }

        elif sort_order == 1:
            self.lg.info('按升序排序')
            # 必须
            referer = 'https://list.tmall.com/search_product.htm?q={}&type=p&spm=a220m.8599659.a2227oh.d100&from=mallfp..m_1_searchbutton&searchType=default&sort=p'.format(
                quote_plus(keyword[1]))
            # print(referer)
            params = (
                ('page_size', '20'),
                ('page_no', '1'),
                ('q', keyword[1]),
                ('type', 'p'),
                ('spm', 'a220m.8599659.a2227oh.d100'),
                ('from', 'mallfp..m_1_searchbutton'),
                ('searchType', 'default'),
                ('sort', 'p'),
            )

        else:
            raise NotImplemented

        headers.update({
            'referer': referer
        })

        s_url = 'https://list.tmall.com/m/search_items.htm'
        body = Requests.get_url_body(
            url=s_url,
            headers=headers,
            params=params,
            ip_pool_type=self.ip_pool_type,
            proxy_type=PROXY_TYPE_HTTPS,
            num_retries=self.req_num_retries,)
        assert body != ''
        # self.lg.info(str(body))

        data = json_2_dict(
            json_str=body,
            default_res={},
            logger=self.lg)
        assert data != {}, '获取到的天猫搜索data为空dict! 出错关键字为{0}'.format(keyword[1])

        _ = data.get('item', [])
        assert _ != [], '获取天猫搜索goods_id_list为空list! 出错关键字{0}'.format(keyword[1])
        assert _ is not None, '获取天猫搜索goods_id_list为空list! 出错关键字{0}'.format(keyword[1])
        # pprint(_)

        res = []
        for item in _:
            try:
                item_url = str(item.get('url', ''))
                assert item_url != ''

                item_id = str(item.get('item_id', ''))
                this_price = float(item.get('price', '0'))
                if this_price < 8.8:
                    self.lg.info('该goods_id: {}, this_price: {}, 售价小于9元, pass'.format(item_id, this_price))
                    continue

                post_fee = float(item.get('post_fee', '0'))
                if post_fee > 0:
                    self.lg.info('该goods_id: {}不包邮, 邮费: {}, pass'.format(item_id, post_fee))
                    continue

            except Exception:
                self.lg.error('遇到错误[出错关键字:{}]:'.format(keyword[1]), exc_info=True)
                continue

            res.append(item_url)

        # boss说同一关键字重复太多, 取10个 此处取15个

        return res[:15]

    def _get_jd_goods_keywords_goods_id_list(self, keyword):
        '''
        根据keyword获取京东销量靠前的商品
        :param keyword:
        :return: [] or ['xxxx', ....]
        '''
        # 方案1: jd m站的搜索(基于搜索接口)
        headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': get_random_pc_ua(),
            'accept': '*/*',
            # 'referer': 'https://so.m.jd.com/ware/search.action?keyword=b&area_ids=1,72,2819&sort_type=sort_totalsales15_desc&qp_disable=no&fdesc=%E5%8C%97%E4%BA%AC&t1=1529934870416',
            'authority': 'so.m.jd.com',
        }
        params = (
            ('keyword', keyword[1]),
            ('datatype', '1'),
            ('callback', 'jdSearchResultBkCbA'),
            ('page', '1'),
            ('pagesize', '10'),
            ('ext_attr', 'no'),
            ('brand_col', 'no'),
            ('price_col', 'no'),
            ('color_col', 'no'),
            ('size_col', 'no'),
            ('ext_attr_sort', 'no'),
            ('merge_sku', 'yes'),
            ('multi_suppliers', 'yes'),
            ('area_ids', '1,72,2819'),
            ('sort_type', 'sort_totalsales15_desc'),
            ('qp_disable', 'no'),
            ('fdesc', '\u5317\u4EAC'),
            # ('t1', '1529934992189'),
        )

        s_url = 'https://so.m.jd.com/ware/search._m2wq_list'
        body = Requests.get_url_body(url=s_url, headers=headers, params=params, ip_pool_type=self.ip_pool_type)
        # self.lg.info(str(body))
        if body == '':
            return []
        else:
            try:
                data = re.compile('jdSearchResultBkCbA\((.*)\)').findall(body)[0]
            except IndexError:
                self.lg.error('获取jd的关键字数据时, IndexError! 出错关键字为{0}'.format((keyword[1])))
                return []

            '''问题在于编码中是\xa0之类的，当遇到有些 不用转义的\http之类的，则会出现以上错误。'''
            data = deal_with_JSONDecodeError_about_value_invalid_escape(json_str=data)
            data = json_2_dict(json_str=data, logger=self.lg)
            if data == {}:
                self.lg.error('获取到的天猫搜索data为空dict! 出错关键字为{0}'.format(keyword[1]))
                return []
            else:
                # 注意拿到的数据如果是京东拼购则跳过
                # pprint(data)
                data = data.get('data', {}).get('searchm', {}).get('Paragraph', [])
                # pingou中字段'bp'不为空即为拼购商品，抓取时不抓取拼购商品, 即'pingou_price': item.get('pinGou', {}).get('bp', '') == ''
                if data is not None and data != []:
                    goods_id_list = [item.get('wareid', '') for item in data if item.get('pinGou', {}).get('bp', '') == '']

                    return goods_id_list

                else:
                    self.lg.error('获取到的data为空list, 请检查!')
                    return []

    def _taobao_keywords_spider(self, **kwargs):
        '''
        抓取goods_id_list的数据，并存储
        :param kwargs:
        :return:
        '''
        goods_id_list = kwargs.get('goods_id_list')
        keyword_id = kwargs.get('keyword_id')
        goods_url_list = ['https://item.taobao.com/item.htm?id=' + item for item in goods_id_list]

        self.lg.info('即将开始抓取该关键字的goods, 请耐心等待...')
        for item in goods_url_list:     # item为goods_url
            # 用于判断某个goods是否被插入的参数
            result = False
            try:
                goods_id = re.compile(r'id=(\d+)').findall(item)[0]
            except IndexError:
                self.lg.error('re获取goods_id时出错, 请检查!')
                continue

            if goods_id in self.db_existed_goods_id_list:
                self.lg.info('该goods_id[{0}]已存在于db中!'.format(goods_id))
                result = True   # 原先存在的情况
                pass

            else:
                taobao = TaoBaoLoginAndParse(logger=self.lg, is_real_times_update_call=True)
                self.sql_cli = _block_get_new_db_conn(
                    db_obj=self.sql_cli,
                    index=self.add_goods_index,
                    logger=self.lg,
                    remainder=20,)
                if self.sql_cli.is_connect_success:
                    goods_id = taobao.get_goods_id_from_url(item)
                    if goods_id == '':
                        self.lg.error('@@@ 原商品的地址为: {0}'.format(item))
                        continue

                    else:
                        self.lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (goods_id, str(self.add_goods_index)))
                        tt = taobao.get_goods_data(goods_id)
                        data = taobao.deal_with_data(goods_id=goods_id)
                        if data != {}:
                            data['goods_id'] = goods_id
                            data['goods_url'] = 'https://item.taobao.com/item.htm?id=' + str(goods_id)
                            data['username'] = '18698570079'
                            data['main_goods_id'] = None
                            if not self.check_target_data_is_legal(target_data=data):
                                return False

                            result = taobao.old_taobao_goods_insert_into_new_table(data, pipeline=self.sql_cli)

                        else:
                            pass

                else:  # 表示返回的data值为空值
                    self.lg.info('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                self.add_goods_index += 1
                collect()
                sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)
            if result:
                # 仅处理goods_id被插入或者原先已存在于db中
                self._insert_into_goods_id_and_keyword_middle_table(goods_id=goods_id, keyword_id=keyword_id)
            else:
                pass

        self.lg.info('该关键字的商品已经抓取完毕!')

        return True

    def _1688_keywords_spider(self, **kwargs):
        '''
        1688对应关键字的商品信息抓取存储
        :param kwargs:
        :return:
        '''
        goods_id_list = kwargs.get('goods_id_list')
        keyword_id = kwargs.get('keyword_id')
        goods_url_list = ['https://detail.1688.com/offer/{0}.html'.format(item) for item in goods_id_list]

        self.lg.info('即将开始抓取该关键字的goods, 请耐心等待...')

        for item in goods_url_list:
            result = False  # 每次重置
            try:
                goods_id = re.compile('offer/(.*?).html').findall(item)[0]
            except IndexError:
                self.lg.error('re获取goods_id时出错, 请检查!')
                continue
            if goods_id in self.db_existed_goods_id_list:
                self.lg.info('该goods_id[{0}]已存在于db中!'.format(goods_id))
                result = True   # 原先存在的情况
                pass
            else:
                ali_1688 = ALi1688LoginAndParse(logger=self.lg)
                if self.add_goods_index % 20 == 0:  # 每50次重连一次，避免单次长连无响应报错
                    self.lg.info('正在重置，并与数据库建立新连接中...')
                    self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
                    self.lg.info('与数据库的新连接成功建立...')

                if self.sql_cli.is_connect_success:
                    goods_id = ali_1688.get_goods_id_from_url(item)
                    if goods_id == '':
                        self.lg.error('@@@ 原商品的地址为: {0}'.format(item))
                        continue
                    else:
                        self.lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (goods_id, str(self.add_goods_index)))
                        tt = ali_1688.get_ali_1688_data(goods_id)
                        if tt.get('is_delete') == 1 and tt.get('before') is False:    # 处理已下架的但是还是要插入的
                            # 下架的商品就pass
                            continue

                        data = ali_1688.deal_with_data()
                        if data != {}:
                            data['goods_id'] = goods_id
                            data['goods_url'] = 'https://detail.1688.com/offer/' + goods_id + '.html'
                            data['username'] = '18698570079'
                            data['main_goods_id'] = None

                            result = ali_1688.old_ali_1688_goods_insert_into_new_table(data=data, pipeline=self.sql_cli)
                        else:
                            pass

                else:  # 表示返回的data值为空值
                    self.lg.info('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                self.add_goods_index += 1
                try: del ali_1688
                except: pass
                collect()
                sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)
            if result:      # 仅处理goods_id被插入或者原先已存在于db中
                self._insert_into_goods_id_and_keyword_middle_table(goods_id=goods_id, keyword_id=keyword_id)
            else:
                pass

        self.lg.info('该关键字的商品已经抓取完毕!')

        return True

    def _tmall_keywords_spider(self, **kwargs):
        """
        tmall对应关键字采集
        :param kwargs:
        :return:
        """
        goods_id_list = kwargs.get('goods_id_list')
        keyword_id = kwargs.get('keyword_id')
        goods_url_list = ['https:' + re.compile('&skuId=.*').sub('', item) for item in goods_id_list]

        self.lg.info('即将开始抓取该关键字的goods, 请耐心等待...')
        for item in goods_url_list:
            # item为goods_url
            # 用于判断某个goods是否被插入的参数
            result = False
            try:
                goods_id = re.compile(r'id=(\d+)').findall(item)[0]
            except IndexError:
                self.lg.error('re获取goods_id时出错, 请检查!')
                continue

            if goods_id in self.db_existed_goods_id_list:
                self.lg.info('该goods_id[{0}]已存在于db中!'.format(goods_id))
                result = True   # 原先存在的情况
                pass
            else:
                tmall = TmallParse(logger=self.lg, is_real_times_update_call=True)
                self.sql_cli = _block_get_new_db_conn(
                    db_obj=self.sql_cli,
                    index=self.add_goods_index,
                    logger=self.lg,
                    remainder=20, )
                if self.sql_cli.is_connect_success:
                    goods_id = tmall.get_goods_id_from_url(item)
                    if goods_id == []:
                        self.lg.error('@@@ 原商品的地址为: {0}'.format(item))
                        continue
                    else:
                        self.lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (goods_id[1], str(self.add_goods_index)))
                        tt = tmall.get_goods_data(goods_id)
                        data = tmall.deal_with_data()
                        goods_id = goods_id[1]
                        if data != {}:
                            data['goods_id'] = goods_id
                            data['username'] = '18698570079'
                            data['main_goods_id'] = None
                            data['goods_url'] = tmall._from_tmall_type_get_tmall_url(type=data['type'], goods_id=goods_id)
                            if data['goods_url'] == '':
                                self.lg.error('该goods_url为空值! 此处跳过!')
                                continue

                            if not self.check_target_data_is_legal(target_data=data):
                                return False

                            result = tmall.old_tmall_goods_insert_into_new_table(data, pipeline=self.sql_cli)
                        else:
                            pass

                else:
                    self.lg.info('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                self.add_goods_index += 1
                collect()
                sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)
            if result:
                # 仅处理goods_id被插入或者原先已存在于db中
                self._insert_into_goods_id_and_keyword_middle_table(
                    goods_id=goods_id,
                    keyword_id=keyword_id)
            else:
                pass

        self.lg.info('该关键字的商品已经抓取完毕!')

        return True

    def _jd_keywords_spider(self, **kwargs):
        '''
        jd对应关键字采集
        :param kwargs:
        :return:
        '''
        goods_id_list = kwargs.get('goods_id_list')
        keyword_id = kwargs.get('keyword_id')
        '''初始地址可以直接用这个[https://item.jd.com/xxxxx.html]因为jd会给你重定向到正确地址, 存也可以存这个地址'''
        # 所以这边jd就不分类存，一律存为常规商品site_id = 7
        goods_url_list = ['https://item.jd.com/{0}.html'.format(str(item)) for item in goods_id_list]

        self.lg.info('即将开始抓取该关键字的goods, 请耐心等待...')

        for item in goods_url_list:     # item为goods_url
            result = False  # 用于判断某个goods是否被插入db的参数
            try:
                goods_id = re.compile('/(\d+)\.html').findall(item)[0]
            except IndexError:
                self.lg.error('re获取goods_id时出错, 请检查!')
                continue

            if goods_id in self.db_existed_goods_id_list:
                self.lg.info('该goods_id[{0}]已存在于db中!'.format(goods_id))
                result = True   # 原先存在的情况
                pass
            else:
                jd = JdParse(logger=self.lg)
                if self.add_goods_index % 20 == 0:  # 每20次重连一次，避免单次长连无响应报错
                    self.lg.info('正在重置，并与数据库建立新连接中...')
                    self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
                    self.lg.info('与数据库的新连接成功建立...')

                if self.sql_cli.is_connect_success:
                    goods_id = jd.get_goods_id_from_url(item)
                    if goods_id == []:
                        self.lg.error('@@@ 原商品的地址为: {0}'.format(item))
                        continue
                    else:
                        self.lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (goods_id[1], str(self.add_goods_index)))
                        tt = jd.get_goods_data(goods_id)
                        data = jd.deal_with_data(goods_id)
                        goods_id = goods_id[1]
                        if data != {}:
                            data['goods_id'] = goods_id
                            data['username'] = '18698570079'
                            data['main_goods_id'] = None
                            data['goods_url'] = item

                            result = jd.old_jd_goods_insert_into_new_table(data, self.sql_cli)
                        else:
                            pass
                else:
                    self.lg.info('数据库连接失败，数据库可能关闭或者维护中')
                    pass
                self.add_goods_index += 1
                sleep(1)
                try:
                    del jd
                except: pass
                collect()

            if result:      # 仅处理goods_id被插入或者原先已存在于db中
                self._insert_into_goods_id_and_keyword_middle_table(goods_id=goods_id, keyword_id=keyword_id)
            else:
                pass

        self.lg.info('该关键字的商品已经抓取完毕!')

        return True

    @catch_exceptions_with_class_logger(default_res=False)
    def check_target_data_is_legal(self, target_data: dict) -> bool:
        """
        检查被采集的数据是否合法
        :return:
        """
        res = True
        if int(target_data['sell_count']) < 50:
            self.lg.info('该商品销量小于50, pass')
            res = False

        if float(target_data['taobao_price']) < 8.8:
            self.lg.info('最低价小于9元不采集, pass')
            res = False

        return res

    def _insert_into_goods_id_and_keyword_middle_table(self, **kwargs):
        '''
        数据插入goods_id_and_keyword_middle_table
        :param kwargs:
        :return:
        '''
        goods_id = str(kwargs['goods_id'])
        keyword_id = int(kwargs['keyword_id'])
        # self.lg.info(goods_id)
        # self.lg.info(keyword_id)
        result = False

        '''先判断中间表goods_id_and_keyword_middle_table是否已新增该关键字的id'''
        # 注意非完整sql语句不用r'', 而直接''
        try:
            _ = self.sql_cli._select_table(sql_str=kw_select_str_3, params=(goods_id,))
            _ = [i[0] for i in _]
            # pprint(_)
        except Exception:
            self.lg.error('执行中间表goods_id_and_keyword_middle_table是否已新增该关键字的id的sql语句时出错, 跳过给商品加keyword_id')
            return result

        if keyword_id not in _:
            params = (
                goods_id,
                keyword_id,)
            self.lg.info('------>>>| 正在插入keyword_id为{0}, goods_id为{1}'.format(params[1], params[0]))
            result = self.sql_cli._insert_into_table_2(sql_str=self.add_keyword_id_for_goods_id_sql_str, params=params, logger=self.lg)

        return result

    def _add_keyword_2_db_from_excel_file(self):
        '''
        从excel插入新关键字到db
        :return:
        '''
        excel_file_path = '/Users/afa/Desktop/2018-07-18-淘宝phone-top20万.xlsx'
        self.lg.info('正在读取{0}, 请耐心等待...'.format(excel_file_path))
        try:
            excel_result = read_info_from_excel_file(excel_file_path=excel_file_path)
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)
            return False

        self.lg.info('读取完毕!!')
        self.lg.info('正在读取db中原先的keyword...')
        db_keywords = self.sql_cli._select_table(sql_str=kw_select_str_4)
        db_keywords = [i[0] for i in db_keywords]
        self.lg.info('db keywords 读取完毕!')

        for item in excel_result:
            keyword = item.get('关键词', None)
            if not keyword:
                continue

            if keyword in db_keywords:
                self.lg.info('该关键字{0}已经存在于db中...'.format(keyword))
                continue

            self.lg.info('------>>>| 正在存储关键字 {0}'.format(keyword))
            self.sql_cli._insert_into_table_2(sql_str=kw_insert_str_2, params=(str(keyword), 0), logger=self.lg)

        self.lg.info('全部写入完毕!')

        return True

    def __del__(self):
        try:
            del self.lg
            del self.msg
            del self.sql_cli
        except:
            pass
        try:
            del self.db_existed_goods_id_list
        except:
            pass
        collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        _tmp = GoodsKeywordsSpider()
        # _tmp._add_keyword_2_db_from_excel_file()
        _tmp._just_run()
        collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))
        sleep(60*5)

        # goods_keywords_spider = GoodsKeywordsSpider()
        # loop = get_event_loop()
        # loop.run_until_complete(goods_keywords_spider._fck_run())
        # break

def main():
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    just_fuck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        just_fuck_run()