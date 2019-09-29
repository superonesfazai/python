# coding:utf-8

'''
@author = super_fazai
@File    : db_timing_script.py
@connect : superonesfazai@gmail.com
'''

from sys import path as sys_path
sys_path.append('..')
from my_exceptions import (
    SqlServerConnectionException,
)
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from fzutils.memory_utils import get_current_func_info_by_traceback
from fzutils.spider.async_always import *

class DbTimingScript(AsyncCrawler):
    """数据库定时脚本"""
    def __init__(self):
        AsyncCrawler.__init__(
            self,
        )
        self.sleep_time = 3 * 60
        self.init_sql_str()

    def init_sql_str(self):
        # 删除下架又上架但是状态还是下架的异常数据(即下架状态但是delete_time<shelf_time)(原因后台无法更新)
        self.sql_str0 = '''
        select top 100 GoodsID, SiteID
        from dbo.GoodsInfoAutoGet
        where MainGoodsID is not NULL
        and IsDelete=1
        and delete_time < shelf_time
        '''
        self.sql_str1 = '''
        update dbo.GoodsInfoAutoGet
        set ModfiyTime=%s, delete_time=%s
        where GoodsID=%s
        '''
        # 更改原先下架但是delete_time为空的商品(原因后台无法由上架变下架)
        self.sql_str2 = '''
        select top 100 GoodsID, SiteID
        from dbo.GoodsInfoAutoGet
        where MainGoodsID is not null
        and IsDelete=1
        and delete_time is null
        '''
        self.sql_str3 = '''
        update dbo.GoodsInfoAutoGet 
        set delete_time=%s
        where GoodsID=%s
        '''
        # 更改上架状态但是delete_time>shelf_time的商品(原因后台无法更新下架变上架)
        self.sql_str4 = '''
        select top 100 GoodsID, SiteID
        from dbo.GoodsInfoAutoGet
        where MainGoodsID is not NUll
        and IsDelete=0
        and shelf_time < delete_time
        '''
        self.sql_str5 = '''
        update dbo.GoodsInfoAutoGet 
        set ModfiyTime=%s, shelf_time=%s
        where GoodsID=%s
        '''

    async def _fck_run(self):
        while True:
            try:
                print('now_time: {}'.format(get_shanghai_time()))
                self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
                if not self.sql_cli.is_connect_success:
                    raise SqlServerConnectionException
                else:
                    pass

                await self.db_script0(
                    select_sql_str=self.sql_str0,
                    update_sql_str=self.sql_str1,
                    func_get_params=self.get_params0,
                )
                await self.db_script0(
                    select_sql_str=self.sql_str2,
                    update_sql_str=self.sql_str3,
                    func_get_params=self.get_params1,
                )
                await self.db_script0(
                    select_sql_str=self.sql_str4,
                    update_sql_str=self.sql_str5,
                    func_get_params=self.get_params0,
                )
            except Exception as e:
                print(e)
            finally:
                print('休眠{}s ...'.format(self.sleep_time))
                await async_sleep(self.sleep_time)

    async def db_script0(self, select_sql_str: str, update_sql_str: str, func_get_params,):
        get_current_func_info_by_traceback(self=self)
        db_res = self.sql_cli._select_table(
            sql_str=select_sql_str,
        )
        db_res = [] if db_res is None else db_res
        if db_res == []:
            print('目标db_res为空list! 跳过此次!')
            return None

        for item in db_res:
            params = func_get_params(k=item)
            self.sql_cli._update_table(
                sql_str=update_sql_str,
                params=params,
            )

        try:
            del db_res
        except:
            pass

        return None

    def get_params0(self, k) -> tuple:
        now_time = str(get_shanghai_time())
        goods_id = k[0]
        site_id = k[1]
        print('goods_id: {}, site_id: {}'.format(goods_id, site_id))

        return tuple([
            now_time,
            now_time,
            goods_id,
        ])

    def get_params1(self, k) -> tuple:
        now_time = str(get_shanghai_time())
        goods_id = k[0]
        site_id = k[1]
        print('goods_id: {}, site_id: {}'.format(goods_id, site_id))

        return tuple([
            now_time,
            goods_id,
        ])

    def __del__(self):
        try:
            pass
        except:
            pass
        collect()

if __name__ == '__main__':
    loop = get_event_loop()
    db_timing_script = DbTimingScript()
    loop.run_until_complete(db_timing_script._fck_run())