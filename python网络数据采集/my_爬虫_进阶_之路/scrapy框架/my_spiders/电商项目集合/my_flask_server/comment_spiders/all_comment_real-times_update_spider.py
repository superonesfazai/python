# coding:utf-8

'''
@author = super_fazai
@File    : all_comment_real-times_update_spider.py
@connect : superonesfazai@gmail.com
'''

"""
分布式 comment update
"""

import sys
sys.path.append('..')

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from settings import (
    IS_BACKGROUND_RUNNING,
    MY_SPIDER_LOGS_PATH,
    IP_POOL_TYPE,)

from gc import collect

from multiplex_code import (
    _print_db_old_data,
    handle_and_save_goods_comment_info,
    get_goods_comment_async_one_res,
    record_goods_comment_modify_time,
)

from sql_str_controller import (
    cm_select_str_1,
)

from fzutils.spider.async_always import *

class CommentRealTimesUpdateSpider(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            ip_pool_type=IP_POOL_TYPE,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/all_comment/实时更新/',)
        # 并发量
        self.concurrency = 10
        self.debugging_api = self._init_debugging_api()
        # 设置并发obj
        self.conc_type_num = 0

    async def _fck_run(self):
        """
        main
        :return:
        """
        while True:
            result = await self._get_db_old_data()
            if result is None:
                pass
            else:
                tasks_params_list = await self._get_tasks_params_list(result=result)
                tasks_params_list = TasksParamsListObj(tasks_params_list=tasks_params_list, step=self.concurrency)
                while True:
                    try:
                        slice_params_list = tasks_params_list.__next__()
                        # self.lg.info(str(slice_params_list))
                    except AssertionError:
                        break

                    one_res = await get_goods_comment_async_one_res(
                        slice_params_list=slice_params_list,
                        now_loop=self.loop,
                        logger=self.lg,
                        conc_type_num=self.conc_type_num,)
                    # pprint(one_res)
                    now_goods_comment_list = one_res
                    await handle_and_save_goods_comment_info(
                        now_goods_comment_list=now_goods_comment_list,
                        logger=self.lg,)
                    await self._update_goods_comment_modify_time(now_goods_comment_list)
                    await async_sleep(1.2)

                collect()

    async def _update_goods_comment_modify_time(self, now_goods_comment_list) -> None:
        """
        更新comment_modify_time(遍历过即更新, 不管成功与否!)
        :param now_goods_comment_list:
        :return:
        """
        self.lg.info('Recoding ' + '.' * 50)
        for item in now_goods_comment_list:
            try:
                goods_id = item.get('goods_id', '')
                assert goods_id != '', 'goods_id不为空值!'
                res = await record_goods_comment_modify_time(
                    goods_id=goods_id,
                    logger=self.lg)
            except AssertionError:
                continue

        return None

    async def _get_tasks_params_list(self, result) -> list:
        """
        获取tasks_params_list
        :param result:
        :return:
        """
        tasks_params_list = []
        for index, item in enumerate(result):
            # item: ('xxxx':goods_id, 'y':site_id)
            goods_id, site_id = item
            if not self.debugging_api.get(site_id):
                self.lg.info('api为False, 跳过! 索引值[%s]' % str(index))
                continue

            tasks_params_list.append({
                'index': index,
                'goods_id': goods_id,
                'site_id': site_id,
            })

        return tasks_params_list

    async def _get_db_old_data(self) -> (list, None):
        """
        获取db 待采集的data
        :return:
        """
        tmp_sql_server = SqlServerMyPageInfoSaveItemPipeline()
        result = None
        try:
            result = list(tmp_sql_server._select_table(
                sql_str=cm_select_str_1,
                logger=self.lg))
        except TypeError:
            self.lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')
            await async_sleep(60)

        await _print_db_old_data(result=result, logger=self.lg)

        return result

    @staticmethod
    def _init_debugging_api():
        '''
        用于设置待抓取的商品的site_id
        :return: dict
        '''
        return {
            1: True,
            2: False,
            3: True,
            4: True,
            6: True,
            7: True,
            8: True,
            9: True,
            10: True,
            11: True,
            12: False,
            13: False,
            25: False,
        }

    def __del__(self):
        try:
            del self.lg
            del self.loop
            del self.debugging_api
        except:
            pass
        collect()

def just_fuck_run():
    while True:
        print('一次大抓取即将开始'.center(30, '-'))
        _ = CommentRealTimesUpdateSpider()
        loop = get_event_loop()
        res = loop.run_until_complete(_._fck_run())
        collect()
        print('一次大抓取完毕, 即将重新开始'.center(30, '-'))

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