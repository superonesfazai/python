# coding:utf-8

'''
@author = super_fazai
@File    : cp_goods_info_monitor_spider.py
@connect : superonesfazai@gmail.com
'''

from sys import path as sys_path
sys_path.append('..')

from settings import (
    IP_POOL_TYPE,
    MY_SPIDER_LOGS_PATH,
)
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from fzutils.spider.selector import parse_field
from fzutils.spider.async_always import *

class YXGoodsInfoMonitorSpider(AsyncCrawler):
    """cp goods info monitor"""
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/cp/yx_goods_monitor/',
        )
        self.req_num_retries = 5
        self.concurrency = 100
        self.concurrent_type = 1
        self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        self.init_sql_str()

    async def _fck_run(self):
        while True:
            self.db_res = await self.get_db_res()
            await self.get_all_goods_info_and_handle_by_goods_id_list(
                goods_id_list=[item[0] for item in self.db_res],
            )
            await async_sleep(10.)

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

        return db_res

    async def get_all_goods_info_and_handle_by_goods_id_list(self, goods_id_list: list):
        """
        根据goods_id_list获取所有goods info并处理
        :return:
        """
        async def get_tasks_params_list() -> list:
            tasks_params_list = []
            for goods_id in goods_id_list:
                tasks_params_list.append({
                    'goods_id': goods_id
                })

            return tasks_params_list

        def get_create_task_msg(k) -> str:
            return 'create task[where goods_id: {}] ...'.format(
                k['goods_id'],
            )

        def get_now_args(k) -> list:
            return [
                k['goods_id'],
            ]

        assert goods_id_list != []
        all_res = await get_or_handle_target_data_by_task_params_list(
            loop=self.loop,
            tasks_params_list=await get_tasks_params_list(),
            func_name_where_get_create_task_msg=get_create_task_msg,
            func_name=self.get_goods_info_by_goods_id,
            func_name_where_get_now_args=get_now_args,
            func_name_where_handle_one_res=self.handle_one_res,
            func_name_where_add_one_res_2_all_res=default_add_one_res_2_all_res2,
            one_default_res={},
            step=self.concurrency,
            logger=self.lg,
            concurrent_type=self.concurrent_type,
        )

        return all_res

    def handle_one_res(self, one_res) -> None:
        """
        处理单个结果
        :return:
        """
        # 每次重连
        self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        if not self.sql_cli.is_connect_success:
            return

        # pprint(one_res)
        for item in one_res:
            try:
                goods_id = item.get('goods_id', '')
                assert goods_id != ''
                # 会员价
                tb_price0 = item.get('tb_price0', 0.)
                assert tb_price0 != 0.
                # 优点价
                tb_price1 = item.get('tb_price1', 0.)
            except AssertionError:
                continue

            for item in self.db_res:
                db_goods_id = item[0]
                db_tb_price = float(item[1]).__round__(2)
                site_id = item[3]
                modify_time = item[4]
                goods_url = item[5]
                if goods_id == db_goods_id:
                    if tb_price1 != db_tb_price:
                        # 先对比会员价
                        if tb_price0 != db_tb_price:
                            # 再对比优点价格, 两者都不同才进行修正, 否则pass(原因cp 部分会员价显示错误)
                            now_time = get_shanghai_time()
                            cp_url = 'https://m.yiuxiu.com/Product/Info/{}'.format(goods_id)
                            self.lg.info('goods_id: {}, 优点价格: {}, 会员价格: {}, db_tb_price: {}, site_id: {}, modify_time: {}, cp_url: {}, goods_url: {}'.format(
                                goods_id,
                                tb_price1,
                                tb_price0,
                                db_tb_price,
                                site_id,
                                modify_time,
                                cp_url,
                                goods_url,
                            ))
                            self.sql_cli._update_table_2(
                                sql_str=self.sql_tr1,
                                params=(
                                    now_time,
                                    now_time,
                                    now_time,
                                    goods_id,
                                ),
                                logger=self.lg,)
                        else:
                            pass
                        break
                    else:
                        continue

        return None

    @catch_exceptions_with_class_logger(default_res={})
    def get_goods_info_by_goods_id(self, goods_id: str) -> dict:
        """
        根据goods_id获取商品信息
        :param goods_id:
        :return:
        """
        def parse_body() -> dict:
            """
            解析
            :return:
            """
            nonlocal body

            # 多规格的最低价
            # 会员价yx 部分显示错误, 改用big 价格加上优点, 两个一起用
            tb_price_sel = {
                'method': 'css',
                'selector': 'div.goodsPriceTips span:nth-child(2) ::text',
            }
            big_price_sel = {
                'method': 'css',
                'selector': 'div.goodsPrice big ::text',
            }
            yd_sel = {
                'method': 're',
                'selector': '<span class=\"yiudianPrice\">\+(\d+)优点</span>'
            }
            tb_price0 = parse_field(
                parser=tb_price_sel,
                target_obj=body, )
            assert tb_price0 != ''
            big_price = parse_field(
                parser=big_price_sel,
                target_obj=body, )
            assert big_price != ''
            yd = parse_field(
                parser=yd_sel,
                target_obj=body,)
            assert yd != ''
            # 会员价
            tb_price0 = float(tb_price0).__round__(2)
            # 优点价
            tb_price1 = (float(big_price) + float(yd)/100).__round__(2)

            return {
                'goods_id': goods_id,
                'tb_price0': tb_price0,
                'tb_price1': tb_price1,
            }

        headers = get_random_headers(
            user_agent_type=1,
            connection_status_keep_alive=False,)
        headers.update({
            'authority': 'm.yiuxiu.com',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-site': 'none',
        })
        url = 'https://m.yiuxiu.com/Product/Info/{}'.format(goods_id)
        body = Requests.get_url_body(
            url=url,
            headers=headers,
            ip_pool_type=self.ip_pool_type,
            num_retries=self.req_num_retries,
            proxy_type=PROXY_TYPE_HTTPS,)
        assert body != ''
        # self.lg.info(body)

        res = parse_body()
        self.lg.info('[{}] goods_id: {}'.format(
            '+' if res != {} else '-',
            goods_id,
        ))

        return res

    def init_sql_str(self):
        self.sql_tr0 = '''
        select MainGoodsID, TaoBaoPrice, Price, SiteID, ModfiyTime, GoodsUrl
        from dbo.GoodsInfoAutoGet
        where MainGoodsID is not null
        and IsDelete=0
        '''
        self.sql_tr1 = '''
        update dbo.GoodsInfoAutoGet 
        set is_spec_change=1, 
        spec_trans_time=%s, 
        ModfiyTime=%s, 
        IsPriceChange=1, 
        sku_info_trans_time=%s, 
        PriceChangeInfo=SKUInfo
        where MainGoodsID=%s
        '''

    def __del__(self):
        try:
            del self.lg
            del self.loop
        except:
            pass
        collect()

if __name__ == '__main__':
    yx_goods_info_monitor_spider = YXGoodsInfoMonitorSpider()
    loop = get_event_loop()
    loop.run_until_complete(yx_goods_info_monitor_spider._fck_run())