# coding:utf-8

'''
@author = super_fazai
@File    : zhe_800_real-times_update.py
@Time    : 2017/11/18 16:00
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from zhe_800_parse import Zhe800Parse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from settings import (
    IS_BACKGROUND_RUNNING,
    MY_SPIDER_LOGS_PATH,)

from sql_str_controller import z8_select_str_3
from multiplex_code import (
    _get_async_task_result,
    _get_new_db_conn,
    _print_db_old_data,
    get_goods_info_change_data,
    Z8DbGoodsInfoObj,
)
from fzutils.spider.async_always import *

class Z8Updater(AsyncCrawler):
    """折800常规商品实时更新"""
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/折800/实时更新/')
        self.sql_cli = None
        self.goods_index = 1
        # 并发量
        self.concurrency = 10       

    async def _get_db_old_data(self):
        self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        result = None
        try:
            result = list(self.sql_cli._select_table(sql_str=z8_select_str_3))
        except TypeError:
            self.lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')

        await _print_db_old_data(logger=self.lg, result=result)

        return result

    async def _get_new_ali_obj(self, index) -> None:
        if index % 10 == 0:
            try:
                del self.zhe_800
            except:
                try:
                    del self.zhe_800
                except:
                    pass
            collect()
            self.zhe_800 = Zhe800Parse()

    async def _update_one_goods_info(self, db_goods_info_obj, index):
        '''
        更新一个goods的信息
        :param db_goods_info_obj:
        :param index:
        :return: ['goods_id', bool:'成功与否']
        '''
        res = False
        await self._get_new_ali_obj(index=index)
        self.sql_cli = await _get_new_db_conn(
            db_obj=self.sql_cli,
            index=index,
            logger=self.lg)
        if self.sql_cli.is_connect_success:
            self.lg.info('------>>>| 正在更新的goods_id为({0}) | --------->>>@ 索引值为({1})'.format(
                db_goods_info_obj.goods_id,
                index))
            self.zhe_800.get_goods_data(goods_id=db_goods_info_obj.goods_id)
            data = self.zhe_800.deal_with_data()
            if data != {}:
                data = get_goods_info_change_data(
                    target_short_name='z8',
                    logger=self.lg,
                    data=data,
                    db_goods_info_obj=db_goods_info_obj,)
                res = self.zhe_800.to_right_and_update_data(
                    data=data,
                    pipeline=self.sql_cli)

            else:  # 表示返回的data值为空值
                pass
        else:  # 表示返回的data值为空值
            self.lg.error('数据库连接失败，数据库可能关闭或者维护中')

        index += 1
        self.goods_index = index
        collect()
        await async_sleep(2.)

        return [db_goods_info_obj.goods_id, res]
    
    async def _update_db(self):
        while True:
            self.lg = await self._get_new_logger(logger_name=get_uuid1())
            result = await self._get_db_old_data()
            if result is None:
                pass
            else:
                self.goods_index = 1
                tasks_params_list = TasksParamsListObj(tasks_params_list=result, step=self.concurrency)
                self.zhe_800 = Zhe800Parse()
                index = 1
                while True:
                    try:
                        slice_params_list = tasks_params_list.__next__()
                        # self.lg.info(str(slice_params_list))
                    except AssertionError:  # 全部提取完毕, 正常退出
                        break

                    tasks = []
                    for item in slice_params_list:
                        db_goods_info_obj = Z8DbGoodsInfoObj(item=item, logger=self.lg)
                        self.lg.info('创建 task goods_id: {}'.format(db_goods_info_obj.goods_id))
                        tasks.append(self.loop.create_task(self._update_one_goods_info(
                            db_goods_info_obj=db_goods_info_obj,
                            index=index)))
                        index += 1

                    await _get_async_task_result(tasks=tasks, logger=self.lg)
                    try:
                        del tasks
                    except:
                        pass

                self.lg.info('全部数据更新完毕'.center(100, '#'))
            if get_shanghai_time().hour == 0:  # 0点以后不更新
                await async_sleep(60 * 60 * 5.5)
            else:
                await async_sleep(10)
            try:
                del self.zhe_800
            except:
                pass
            collect()

    def __del__(self):
        try:
            del self.lg
        except:
            pass
        try:
            del self.loop
        except:
            pass
        collect()

def _fck_run():
    # 遇到: PermissionError: [Errno 13] Permission denied: 'ghostdriver.log'
    # 解决方案: sudo touch /ghostdriver.log && sudo chmod 777 /ghostdriver.log
    _ = Z8Updater()
    loop = get_event_loop()
    loop.run_until_complete(_._update_db())
    try:
        del loop
    except:
        pass

def main():
    print('========主函数开始========')
    daemon_init()
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    _fck_run()

if __name__ == '__main__':
    if IS_BACKGROUND_RUNNING:
        main()
    else:
        _fck_run()