# coding:utf-8

'''
@author = super_fazai
@File    : goods_sort_by_shop_type_spider2.py
@connect : superonesfazai@gmail.com
'''

from settings import (
    IP_POOL_TYPE,
    MY_SPIDER_LOGS_PATH,
)
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from fzutils.spider.fz_driver import PHONE
from fzutils.cp_utils import (
    get_taobao_sign_and_body,
    block_calculate_tb_right_sign,
)
from fzutils.spider.async_always import *

class GoodsSortByShopTypeSpider2(AsyncCrawler):
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
        self.req_num_retries = 6
        # 必须是新开m站超市页面来获取
        # tm m站超市分类 url: https://chaoshi.m.tmall.com/
        # tm每次使用请先更换
        # 直接复制对应接口得新cookies
        # 并修改cp_utils中的block_calculate_tb_right_sign中的t(该t为params参数中的t), _m_h5_tk为最新请求对应的值即可
        # eg:
        # 天猫超市入口的t, _m_h5_tk
        # t = '1590387891307'
        # _m_h5_tk = '6f594c22870353cede88c2796cc28ee9'
        self.tm_new_chrome_t = '1590462144500'
        self.tm_new_chrome_sign = '30077eac29271c210646bfdea87f3990'
        self.tm_new_chrome_cookies_str = 'hng=CN%7Czh-CN%7CCNY%7C156; cna=wRsVFTj6JEoCAXHXtCqXOzC7; lid=%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA; enc=MXX6theE39REQu4vFae7f5vi8A8GAdt5pdcQAJY7eR3zuOxwTSUu0zQGRWpBLbzxbJUsLvdHk4vB8ZWvQR%2BjQg%3D%3D; l=eB_zn817vA2VK0x_BOfZnurza779_IRAguPzaNbMiOCPOdfH5H0fWZAGqqTMCnGVh6uk83JDb3ZQBeYBcBdKnxvOnrZgURDmn; sm4=330100; csa=0_0_0_0_0_0_0_0_0_0_0_0_0; sgcookie=EbIdqdSy36jBPHKaO%2FPZS; uc3=id2=UUplY9Ft9xwldQ%3D%3D&lg2=W5iHLLyFOGW7aA%3D%3D&vt3=F8dBxGZjLZslLqBqC3E%3D&nk2=rUtEoY7x%2Bk8Rxyx1ZtN%2FAg%3D%3D; t=44ba880282155f09837da199e9503ac5; tracknick=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; uc4=id4=0%40U2gvLJ3%2BK6kqeorNX%2B21sXN8x3lW&nk4=0%40r7rCNeQ4%2Bj7fAj%2BMcdPH4%2B0X9x%2FwQLp0Sd4%2F; lgc=%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA; _tb_token_=6f560ee758b7; cookie2=149dda2bafcaebd274a743d5320acc65; _m_h5_tk=1942ee9b8bc4f3c4ef06951534bda043_1590471490706; _m_h5_tk_enc=ccaf144e114b061308be53c18731a2fd; isg=BJeXuGUrhSKzIAPyU_A77fAQJg3h3Gs-yAsChunEs2bNGLda8az7jlU-fv6j8EO2'
        self.tm_first_sort_list = [
            {
                'name': '休闲零食',
                'icon_type': 'categoryxiuxianlingshi',
                'level1_id': 78,
            },
            {
                'name': '粮油米面',
                'icon_type': 'categoryliangyoumimian',
                'level1_id': 80,
            },
            {
                'name': '乳饮酒水',
                'icon_type': 'categorynaipinshuiyin',
                'level1_id': 79,
            },
            {
                'name': '日用百货',
                'icon_type': 'categorychufangriyong',
                'level1_id': 81,
            },
            {
                'name': '母婴用品',
                'icon_type': 'categorymuyingyongping',
                'level1_id': 82,
            },
            {
                'name': '个人护理',
                'icon_type': 'categorygerenhuli',
                'level1_id': 83,
            },
            {
                'name': '纸品家清',
                'icon_type': 'categoryjiaqingjiaju',
                'level1_id': 84,
            },
            {
                'name': '美容护肤',
                'icon_type': 'categorymeironghufu',
                'level1_id': 94,
            },
            {
                'name': '方便速食',
                'icon_type': 'categoryfangbiansushi',
                'level1_id': 92,
            },
            {
                'name': '中外名酒',
                'icon_type': 'categoryzhongwaimingjiu',
                'level1_id': 87,
            },
            {
                'name': '童装童鞋',
                'icon_type': 'categorytongzhuang',
                'level1_id': 138,
            },
            {
                'name': '成人用品',
                'icon_type': 'categorychengrenyongpin',
                'level1_id': 93,
            },
            {
                'name': '家纺内衣',
                'icon_type': 'categoryjiafangneiyi',
                'level1_id': 90,
            },
            {
                'name': '宠物生活',
                'icon_type': 'categorychongwuyongpin',
                'level1_id': 91,
            },
            {
                'name': '电器数码',
                'icon_type': 'category3cqipei',
                'level1_id': 95,
            },
            {
                'name': '进口好货',
                'icon_type': 'categoryjinkouhaohuo',
                'level1_id': 85,
            },
            {
                'name': '医疗保健',
                'icon_type': 'categoryzibubaojian',
                'level1_id': 89,
            },
        ]
        self.tm_skip_name_tuple = (
            '好货',
            '为你推荐',
            '热销榜单',
            '每日特惠',
            '一件包邮',
            '新品尝鲜',
            '年中大赏',
            '喵九八',
            '新品推荐',
            '特惠',
            '尝新',
            '精致好货',
            '超值爆款',
            '包邮',
            '优选',
            '直播',
            '尖叫单品',
            '品牌专区',
            '大牌',
            '网红爆款',
            '新品',
            '清凉一夏',
            '热销',
            '推荐',
            '国家馆',
            '优惠',
            '折',
            '送',        # eg: 买一送一
            '精选',
            '爆款',
            '上新',
            '秒杀',
            '热门',
        )
        self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        self.sql_str0 = 'insert into dbo.common_shop_sort_level_table(unique_id, sort_level1_id, sort_level1_name, sort_level2_id, sort_level2_name, sort_level3_id, sort_level3_name) values(%s, %s, %s, %s, %s, %s, %s)'

    async def _fck_run(self):
        await self.get_tm_sort_info()

    def get_common_shop_sort_level_table_unique_id(self,
                                                   shop_id,
                                                   sort_level1_id='',
                                                   sort_level2_id='',
                                                   sort_level3_id='') -> str:
        """
        生成common_shop_sort_level_table唯一的unique_id 以避免记录重复
        :param shop_id:
        :param sort_level1_id:
        :param sort_level2_id:
        :param sort_level3_id:
        :return:
        """
        # 拼接成类似于'{}::{}::{}::{}'结构
        target_str = shop_id
        if sort_level1_id != '':
            target_str = target_str + '::' + str(sort_level1_id)

        if sort_level2_id != '':
            target_str = target_str + '::' + str(sort_level2_id)

        if sort_level3_id != '':
            target_str = target_str + '::' + str(sort_level3_id)

        self.lg.info(target_str)

        return get_uuid3(target_str=target_str)

    async def get_tm_sort_info(self):
        """
        获取天猫的分类信息
        :return:
        """
        # 插入tmcs 第一分类的数据到db
        # await self._tmcs_insert_into_sort_level1_2_db()

        # 获取第二分类的id信息
        for item in self.tm_first_sort_list:
            sort_level1_id = item.get('level1_id', 0)
            sort_level1_name = item.get('name', '')
            icon_type = item.get('icon_type', '')
            is_success = False
            target_data = {}
            try:
                self.lg.info('Get sort_level1_name: {}, sort_level1_id: {} ing ...'.format(
                    sort_level1_name,
                    sort_level1_id))
                target_data = await self.get_tm_second_sort_info_by_first_sort_name(
                    first_sort_name=sort_level1_name,
                    icon_type=icon_type,
                    level1_id=sort_level1_id,)
                if target_data != {}:
                    is_success = True
                else:
                    pass
                assert target_data != {}
                # 插入db
                await self._tmcs_insert_into_sort_level2_2_db(data=target_data)
            except Exception:
                self.lg.error('遇到错误:', exc_info=True)

            self.lg.info('[{}] sort_level1_name: {}, sort_level1_id: {}'.format(
                '+' if is_success else '-',
                sort_level1_name,
                sort_level1_id,
            ))

            # 再获取其第三类的分类信息

            # 测试
            # 获取第三分类的信息
            # 即上面的second_list中item的id
            # second_id = 298
            # icon_type = 'categoryxiuxianlingshi'
            # business = 'B2C'
            # await self.get_tm_third_sort_info_by_second_id(
            #     second_id=second_id,
            #     icon_type=icon_type,
            #     business=business
            # )

            if target_data == {}:
                continue

            for i in target_data.get('second_list', []):
                is_success2 = False
                try:
                    sort_level2_id = i.get('id', -1)
                    assert sort_level2_id != -1
                    sort_level2_name = i.get('name', '')
                    assert sort_level2_name != ''
                    business = i.get('business', '')
                    assert business != ''

                    self.lg.info('Get sort_level2_name: {}, sort_level2_id: {} ing ...'.format(
                        sort_level2_name,
                        sort_level2_id))
                    target_data2 = await self.get_tm_third_sort_info_by_second_id(
                        second_id=sort_level2_id,
                        icon_type=icon_type,
                        business=business,)
                    if target_data2 != {}:
                        is_success2 = True
                    else:
                        pass
                    assert target_data2 != {}
                    # 插入db
                    await self._tmcs_insert_into_sort_level3_2_db(
                        sort_level1_id=sort_level1_id,
                        sort_level1_name=sort_level1_name,
                        sort_level2_name=sort_level2_name,
                        data=target_data2)
                except Exception:
                    self.lg.error('遇到错误:', exc_info=True)
                    continue

                self.lg.info('[{}] sort_level2_name: {}, sort_level2_id: {}'.format(
                    '+' if is_success2 else '-',
                    sort_level2_name,
                    sort_level2_id,
                ))

        # 测试
        # 获取第四分类, 即直接获取最后一级分类对应的goods_id_list
        # second_id = 298
        # third_id = 0
        # icon_type = 'categoryxiuxianlingshi'
        # business = 'B2C'
        # await self.get_tm_fourth_sort_info_by_second_id_and_third_id(
        #     second_id=second_id,
        #     third_id=third_id,
        #     icon_type=icon_type,
        #     business=business
        # )

    async def _tmcs_insert_into_sort_level3_2_db(self,
                                                 sort_level1_id,
                                                 sort_level1_name,
                                                 sort_level2_name,
                                                 data: dict,):
        """
        tmcs插入第三分类等级数据
        :param sort_level1_id:
        :param sort_level1_name:
        :param sort_level2_name:
        :param data:
        :return:
        """
        try:
            sort_level2_id = data.get('second_id', -1)
            assert sort_level2_id != -1
            # 转换为该等级唯一的tmcs的id
            sort_level1_id = self._get_unique_tmcs_sort_level_id(
                sort_level_id=sort_level1_id,)
            sort_level2_id = self._get_unique_tmcs_sort_level_id(
                sort_level_id=sort_level2_id,)
            assert sort_level1_name != ''
            assert sort_level2_name != ''

            for item in data.get('third_list', []):
                try:
                    sort_level3_id = item.get('id', -1)
                    assert sort_level3_id != -1
                    # 转换为该等级唯一的tmcs的id
                    sort_level3_id = self._get_unique_tmcs_sort_level_id(
                        sort_level_id=sort_level3_id,)
                    sort_level3_name = item.get('name', '')
                    assert sort_level3_name != ''

                    self.lg.info('sort_level3_id: {}, sort_level3_name: {}'.format(
                        sort_level3_id,
                        sort_level3_name,
                    ))
                    unique_id = self.get_common_shop_sort_level_table_unique_id(
                        shop_id='tmcs',
                        sort_level1_id=sort_level1_id,
                        sort_level2_id=sort_level2_id,
                        sort_level3_id=sort_level3_id,)
                    self.sql_cli._insert_into_table_2(
                        sql_str=self.sql_str0,
                        params=(
                            unique_id,
                            sort_level1_id,
                            sort_level1_name,
                            sort_level2_id,
                            sort_level2_name,
                            sort_level3_id,
                            sort_level3_name,
                        ),
                        logger=self.lg,)
                except Exception:
                    continue

        except Exception:
            self.lg.error('遇到错误:', exc_info=True)

        return

    async def _tmcs_insert_into_sort_level2_2_db(self, data: dict):
        """
        tmcs插入第二分类等级数据
        :return:
        """
        try:
            sort_level1_id = data.get('level1_id', -1)
            assert sort_level1_id != -1
            # 转换为该等级唯一的tmcs的id
            sort_level1_id = self._get_unique_tmcs_sort_level_id(
                sort_level_id=sort_level1_id,)
            sort_level1_name = data.get('first_sort_name', '')
            assert sort_level1_name != ''

            for item in data.get('second_list', []):
                try:
                    sort_level2_id = item.get('id', -1)
                    assert sort_level2_id != -1
                    # 转换为该等级唯一的tmcs的id
                    sort_level2_id = self._get_unique_tmcs_sort_level_id(
                        sort_level_id=sort_level2_id,)
                    sort_level2_name = item.get('name', '')
                    assert sort_level2_name != ''

                    self.lg.info('sort_level2_id: {}, sort_level2_name: {}'.format(
                        sort_level2_id,
                        sort_level2_name,
                    ))
                    unique_id = self.get_common_shop_sort_level_table_unique_id(
                        shop_id='tmcs',
                        sort_level1_id=sort_level1_id,
                        sort_level2_id=sort_level2_id,)
                    self.sql_cli._insert_into_table_2(
                        sql_str=self.sql_str0,
                        params=(
                            unique_id,
                            sort_level1_id,
                            sort_level1_name,
                            sort_level2_id,
                            sort_level2_name,
                            '',
                            '',
                        ),
                        logger=self.lg,)
                except Exception:
                    continue

        except Exception:
            self.lg.error('遇到错误:', exc_info=True)

        return

    async def _tmcs_insert_into_sort_level1_2_db(self):
        """
        tmcs插入第一分类等级数据
        :return:
        """
        for item in self.tm_first_sort_list:
            sort_level1_id = item.get('level1_id', '')
            # 转换为该等级唯一的tmcs的id
            sort_level1_id = self._get_unique_tmcs_sort_level_id(
                sort_level_id=sort_level1_id)
            sort_level1_name = item.get('name', '')
            self.lg.info('sort_level1_id: {}, sort_level1_name: {}'.format(
                sort_level1_id,
                sort_level1_name,
            ))
            unique_id = self.get_common_shop_sort_level_table_unique_id(
                shop_id='tmcs',
                sort_level1_id=sort_level1_id,)
            try:
                self.sql_cli._insert_into_table_2(
                    sql_str=self.sql_str0,
                    params=(
                        unique_id,
                        sort_level1_id,
                        sort_level1_name,
                        '',
                        '',
                        '',
                        '',
                    ),
                    logger=self.lg,)
            except Exception:
                self.lg.error('遇到错误:', exc_info=True)
                continue

        return

    def _get_unique_tmcs_sort_level_id(self, sort_level_id) -> str:
        """
        获取tmcs的唯一分类id 标识
        :param sort_level_id:
        :return:
        """
        return 'tmcs' + str(sort_level_id)

    async def get_tm_second_sort_info_by_first_sort_name(self,
                                                         first_sort_name,
                                                         icon_type: str,
                                                         level1_id: int):
        """
        根据first_sort_name来获取second分类信息
        :param first_sort_name:
        :param icon_type:
        :param level1_id:
        :return:
        """
        # pc 分类需登录cookies, 且老失效, pass
        # tm m站超市分类 url: https://chaoshi.m.tmall.com/
        # 每次使用请先
        headers = {
            'authority': 'h5api.m.tmall.com',
            'user-agent': get_random_phone_ua(),
            'accept': '*/*',
            # 'referer': 'https://pages.tmall.com/wow/chaoshi/act/chaoshi-category?spm=a3204.12691414.201609072.d78&wh_biz=tm&wh_showError=true&iconType=categoryxiuxianlingshi&name=%E4%BC%91%E9%97%B2%E9%9B%B6%E9%A3%9F&cateId=78&version=newIcon&storeId=&disableNav=YES',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

        # 每次使用请先
        # ** 必传cookies(测试发现无敏感cookie可直接从chrome中复制)
        # 方法(推荐):
        # 直接复制对应接口得新cookies, 并修改cp_utils中的block_calculate_tb_right_sign中的t(该t为params参数中的t), _m_h5_tk为最新请求对应的值即可
        # cookies = {
        #     # '_l_g_': 'Ug%3D%3D',
        #     # 令牌得官方服务器返回, 自己无法伪造
        #     # '_m_h5_tk': 'd7ad6d69cf119b053cf88936309cfc96_1590377299017',
        #     # '_m_h5_tk_enc': '7723c851b571ed56b57a314a8446ea99',
        #     '_m_h5_tk': '9d2d854027bf7cb19b47642e47e83e6c_1590382583798',
        #     '_m_h5_tk_enc': '01ac5d6c8604ff0413af5c0ddcbfc1f3',
        #     '_tb_token_': 'e5339a70ef7f4',
        #     'cookie17': 'UUplY9Ft9xwldQ%3D%3D',
        #     'cookie2': '169a1fd5707fc53066e20184c77dd949',
        #     't': '49edda27be5a68434c5899c297529ebb',
        #     # '_nk_': '%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA',
        #     # 'cna': 'wRsVFTj6JEoCAXHXtCqXOzC7',
        #     # 'cookie1': 'UR3Wq2iKhDJHTTOd%2FGn4oh0oxwBK8EUqK%2Bm%2Bxv62FEM%3D',
        #     # 'csa': '7870450516_0_30.180482.120.21383_0_0_0_330108_107_110_0_236686073_330108001_0',
        #     # 'csg': '0cc7d64f',
        #     # 'dnk': '%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA',
        #     # 'enc': 'MXX6theE39REQu4vFae7f5vi8A8GAdt5pdcQAJY7eR3zuOxwTSUu0zQGRWpBLbzxbJUsLvdHk4vB8ZWvQR%2BjQg%3D%3D',
        #     # 'hng': 'CN%7Czh-CN%7CCNY%7C156',
        #     # 'isg': 'BEZGL3omZJqhYDIl6tv6ojn7lzrIp4ph0VBT8TBvMmlEM-ZNmDfacSzFDylam4J5',
        #     # 'l': 'eB_zn817vA2VKUQxBOfwourza77OSIRAguPzaNbMiOCPOd5B5-j1WZAMqxL6C3GVh649R3JDb3ZQBeYBc3K-nxvtpdcXq3Dmn',
        #     # 'lgc': '%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA',
        #     # 'lid': '%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA',
        #     # 'login': 'true',
        #     # 'sg': '%E4%BA%BA73',
        #     # 'sm4': '330108',
        #     # 'tracknick': '%5Cu6211%5Cu662F%5Cu5DE5%5Cu53F79527%5Cu672C%5Cu4EBA',
        #     # 'uc1': 'pas',
        #     # 'uc3': 'id2',
        #     # 'uc4': 'id4',
        #     # 'unb': '2242024317',
        # }
        headers.update({
            # 'cookie': dict_cookies_2_str(cookies),
            # 测试发现无敏感cookie可直接从chrome中复制
            'cookie': self.tm_new_chrome_cookies_str,
        })

        data = dumps({
            "smAreaId": 330100,
            "csaInfo": "0_0_0_0_0_0_0_0_0_0_0_0_0",
            "csa": "0_0_0_0_0_0_0_0_0_0_0_0_0",
            "iconType": icon_type,
            "level1Id": str(level1_id),
        })

        params = (
            ('jsv', '2.5.1'),
            ('appKey', '12574478'),
            ('t', self.tm_new_chrome_t),        # eg: '1590379653365'
            ('sign', self.tm_new_chrome_sign),  # eg: 'f0e252789605777cb36b6d99ce41ee7c'
            ('api', 'mtop.chaoshi.aselfshoppingguide.category.level1'),
            ('v', '1.0'),
            ('type', 'jsonp'),
            ('dataType', 'jsonp'),
            ('callback', 'mtopjsonp2'),
            # ('data', '{"smAreaId":330108,"csaInfo":"7870450516_0_30.180482.120.21383_0_0_0_330108_107_110_0_236686073_330108001_0","csa":"7870450516_0_30.180482.120.21383_0_0_0_330108_107_110_0_236686073_330108001_0","iconType":"categoryxiuxianlingshi","level1Id":"78"}'),
            ('data', data),
        )

        base_url = 'https://h5api.m.tmall.com/h5/mtop.chaoshi.aselfshoppingguide.category.level1/1.0/'
        # 测试发现只需请求第一次即可获取到数据
        result0 = await get_taobao_sign_and_body(
            base_url=base_url,
            headers=headers,
            params=tuple_or_list_params_2_dict_params(params=params),
            data=data,
            ip_pool_type=self.ip_pool_type,
            proxy_type=PROXY_TYPE_HTTPS,
            logger=self.lg,
        )
        # self.lg.info(str(result0))
        _m_h5_tk, body = result0[0], result0[2]
        assert body != ''
        # self.lg.info(_m_h5_tk)
        # self.lg.info(body)
        # assert _m_h5_tk != ''
        # _m_h5_tk, _session1, body = block_get_tb_sign_and_body(
        #     base_url=base_url,
        #     headers=headers,
        #     params=tuple_or_list_params_2_dict_params(params=params),
        #     data=data,
        #     _m_h5_tk=_m_h5_tk,
        #     session=result0[1],
        #     ip_pool_type=tri_ip_pool,
        #     # proxy_type=PROXY_TYPE_HTTPS,
        # )
        # self.lg.info(body)

        data = json_2_dict(
            json_str=re.compile('\((.*)\)').findall(body)[0],
            default_res={},
            logger=self.lg, ).get('data', {}).get('data', {})
        assert data != {}
        # pprint(data)

        try:
            data['banner'] = []
        except Exception:
            pass

        second_list = []

        for item in data.get('secondList', []):
            # self.lg.info(item)
            try:
                _id = item.get('id', '')
                assert _id != ''
                name = item.get('text', '')
                assert name != ''
                # 过滤非通用分类
                assert name not in self.tm_skip_name_tuple
                for i in self.tm_skip_name_tuple:
                    if i in name:
                        # 处理eg: '特惠', '尝新' 字眼
                        raise ValueError('出现跳过字眼, pass')
                    else:
                        pass
                business = item.get('business', '')
                assert business != ''
            except Exception:
                continue
            second_list.append({
                'id': _id,
                'name': name,
                'business': business,
            })

        res = {
            'first_sort_name': first_sort_name,
            'icon_type': icon_type,
            'level1_id': level1_id,
            'second_list': second_list,
        }
        pprint(res)

        return res

    async def get_tm_third_sort_info_by_second_id(self,
                                                  second_id: int,
                                                  icon_type: str,
                                                  business: str='B2C',):
        """
        根据second_sort_id来获取third分类信息
        :param second_id:
        :param icon_type:
        :param business:
        :return:
        """
        headers = {
            'authority': 'h5api.m.tmall.com',
            'user-agent': get_random_phone_ua(),
            'accept': '*/*',
            # 'referer': 'https://pages.tmall.com/wow/chaoshi/act/chaoshi-category?spm=a3204.12691414.201609072.d78&wh_biz=tm&wh_showError=true&iconType=categoryxiuxianlingshi&name=%E4%BC%91%E9%97%B2%E9%9B%B6%E9%A3%9F&cateId=78&version=newIcon&storeId=&disableNav=YES',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            # 测试发现无敏感cookie可直接从chrome中复制
            'cookie': self.tm_new_chrome_cookies_str,
        }

        data = dumps({
            "smAreaId": 330100,
            "csaInfo": "0_0_0_0_0_0_0_0_0_0_0_0_0",
            "csa": "0_0_0_0_0_0_0_0_0_0_0_0_0",
            "iconType": icon_type,
            "level2Id": str(second_id),
            "business": business,
        })

        params = (
            ('jsv', '2.5.1'),
            ('appKey', '12574478'),
            ('t', self.tm_new_chrome_t),        # eg: '1590379653365'
            ('sign', self.tm_new_chrome_sign),  # eg: 'f0e252789605777cb36b6d99ce41ee7c'
            ('api', 'mtop.chaoshi.aselfshoppingguide.category.level2'),
            ('v', '1.0'),
            ('type', 'jsonp'),
            ('dataType', 'jsonp'),
            ('callback', 'mtopjsonp7'),
            # ('data', '{"smAreaId":330108,"csaInfo":"7870450516_0_30.180482.120.21383_0_0_0_330108_107_110_0_236686073_330108001_0","csa":"7870450516_0_30.180482.120.21383_0_0_0_330108_107_110_0_236686073_330108001_0","iconType":"categoryxiuxianlingshi","level1Id":"78"}'),
            ('data', data),
        )

        base_url = 'https://h5api.m.tmall.com/h5/mtop.chaoshi.aselfshoppingguide.category.level2/1.0/'
        # 测试发现只需请求第一次即可获取到数据
        result0 = await get_taobao_sign_and_body(
            base_url=base_url,
            headers=headers,
            params=tuple_or_list_params_2_dict_params(params=params),
            data=data,
            ip_pool_type=self.ip_pool_type,
            proxy_type=PROXY_TYPE_HTTPS,
            logger=self.lg,
        )
        # self.lg.info(str(result0))
        _m_h5_tk, body = result0[0], result0[2]
        assert body != ''
        # self.lg.info(_m_h5_tk)
        # self.lg.info(body)
        # assert _m_h5_tk != ''
        # _m_h5_tk, _session1, body = block_get_tb_sign_and_body(
        #     base_url=base_url,
        #     headers=headers,
        #     params=tuple_or_list_params_2_dict_params(params=params),
        #     data=data,
        #     _m_h5_tk=_m_h5_tk,
        #     session=result0[1],
        #     ip_pool_type=tri_ip_pool,
        #     # proxy_type=PROXY_TYPE_HTTPS,
        # )
        # self.lg.info(body)

        data = json_2_dict(
            json_str=re.compile('\((.*)\)').findall(body)[0],
            default_res={},
            logger=self.lg, ).get('data', {}).get('data', {})
        assert data != {}
        # pprint(data)

        try:
            data['banner'] = []
        except Exception:
            pass

        third_list = []
        for item in data.get('thrirdList', []):
            # self.lg.info(item)
            try:
                _id = item.get('id', '')
                assert _id != ''
                name = item.get('text', '')
                assert name != ''
                # 过滤非通用分类
                assert name not in self.tm_skip_name_tuple
                for i in self.tm_skip_name_tuple:
                    # self.lg.info(name)
                    if i in name:
                        # 处理eg: '特惠', '尝新' 字眼
                        raise ValueError('出现跳过字眼, pass')
                    else:
                        pass
            except Exception:
                continue
            third_list.append({
                'id': _id,
                'name': name,
            })

        res = {
            'second_id': second_id,
            'third_list': third_list,
        }
        pprint(res)

        return res

    async def get_tm_fourth_sort_info_by_second_id_and_third_id(self,
                                                                second_id: int,
                                                                third_id: int,
                                                                icon_type: str,
                                                                business: str='B2C',):
        """
        根据second_sort_id来获取third分类信息
        :param second_id:
        :param third_id:
        :param icon_type:
        :param business:
        :return:
        """
        headers = {
            'authority': 'h5api.m.tmall.com',
            'user-agent': get_random_phone_ua(),
            'accept': '*/*',
            # 'referer': 'https://pages.tmall.com/wow/chaoshi/act/chaoshi-category?spm=a3204.12691414.201609072.d78&wh_biz=tm&wh_showError=true&iconType=categoryxiuxianlingshi&name=%E4%BC%91%E9%97%B2%E9%9B%B6%E9%A3%9F&cateId=78&version=newIcon&storeId=&disableNav=YES',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            # 测试发现无敏感cookie可直接从chrome中复制
            'cookie': self.tm_new_chrome_cookies_str,
        }

        data = dumps({
            "smAreaId": 330100,
            "csaInfo": "0_0_0_0_0_0_0_0_0_0_0_0_0",
            "csa": "0_0_0_0_0_0_0_0_0_0_0_0_0",
            "iconType": icon_type,
            "level2Id": str(second_id),
            'level3Id': str(third_id),
            'index': 50,
            'pageSize': 20,
            "business": business,
        })

        params = (
            ('jsv', '2.5.1'),
            ('appKey', '12574478'),
            ('t', self.tm_new_chrome_t),        # eg: '1590379653365'
            ('sign', self.tm_new_chrome_sign),  # eg: 'f0e252789605777cb36b6d99ce41ee7c'
            ('api', 'mtop.chaoshi.aselfshoppingguide.category.level3'),
            ('v', '1.0'),
            ('type', 'jsonp'),
            ('dataType', 'jsonp'),
            ('callback', 'mtopjsonp7'),
            # ('data', '{"smAreaId":330108,"csaInfo":"7870450516_0_30.180482.120.21383_0_0_0_330108_107_110_0_236686073_330108001_0","csa":"7870450516_0_30.180482.120.21383_0_0_0_330108_107_110_0_236686073_330108001_0","iconType":"categoryxiuxianlingshi","level1Id":"78"}'),
            ('data', data),
        )

        base_url = 'https://h5api.m.tmall.com/h5/mtop.chaoshi.aselfshoppingguide.category.level3/1.0/'
        # 测试发现只需请求第一次即可获取到数据
        result0 = await get_taobao_sign_and_body(
            base_url=base_url,
            headers=headers,
            params=tuple_or_list_params_2_dict_params(params=params),
            data=data,
            ip_pool_type=self.ip_pool_type,
            proxy_type=PROXY_TYPE_HTTPS,
            logger=self.lg,
        )
        # self.lg.info(str(result0))
        _m_h5_tk, body = result0[0], result0[2]
        assert body != ''
        # self.lg.info(_m_h5_tk)
        # self.lg.info(body)
        # assert _m_h5_tk != ''
        # _m_h5_tk, _session1, body = block_get_tb_sign_and_body(
        #     base_url=base_url,
        #     headers=headers,
        #     params=tuple_or_list_params_2_dict_params(params=params),
        #     data=data,
        #     _m_h5_tk=_m_h5_tk,
        #     session=result0[1],
        #     ip_pool_type=tri_ip_pool,
        #     # proxy_type=PROXY_TYPE_HTTPS,
        # )
        # self.lg.info(body)

        data = json_2_dict(
            json_str=re.compile('\((.*)\)').findall(body)[0],
            default_res={},
            logger=self.lg, ).get('data', {}).get('data', {})
        assert data != {}
        # pprint(data)

        try:
            data['banner'] = []
        except Exception:
            pass

        goods_list = []
        for item in data.get('itemList', {}).get('itemAndContentList', []):
            # self.lg.info(item)
            try:
                goods_id = item.get('itemId', '')
                assert goods_id != ''
                title = item.get('shortTitle', '')
                assert title != ''
            except Exception:
                continue
            goods_list.append({
                'goods_id': str(goods_id),
                'title': title,
            })

        res = {
            'second_id': second_id,
            'third_id': third_id,
            'goods_list': goods_list,
        }
        pprint(res)

        return res

    def __del__(self):
        try:
            del self.lg
            del self.sql_cli
        except:
            pass
        collect()

if __name__ == '__main__':
    goods_sort_by_shop_type_spider = GoodsSortByShopTypeSpider2()
    loop = get_event_loop()
    loop.run_until_complete(goods_sort_by_shop_type_spider._fck_run())