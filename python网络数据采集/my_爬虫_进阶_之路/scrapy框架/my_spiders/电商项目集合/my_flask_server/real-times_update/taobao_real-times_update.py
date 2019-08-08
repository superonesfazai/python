# coding:utf-8

'''
@author = super_fazai
@File    : ali_1688_real-times_update.py
@Time    : 2017/10/28 07:24
@connect : superonesfazai@gmail.com
'''

"""
我们需要两台服务器一台拿来专门更新数据，一台拿来专门处理客服入信息
"""

import sys
sys.path.append('..')

from taobao_parse import TaoBaoLoginAndParse
from my_pipeline import (
    SqlServerMyPageInfoSaveItemPipeline,
    SqlPools,
)

from settings import TAOBAO_REAL_TIMES_SLEEP_TIME
from settings import (
    IS_BACKGROUND_RUNNING,
    MY_SPIDER_LOGS_PATH,)

from sql_str_controller import tb_select_str_3
from multiplex_code import (
    _get_async_task_result,
    _get_new_db_conn,
    _print_db_old_data,
    to_right_and_update_tb_data,
    get_goods_info_change_data,
    BaseDbCommomGoodsInfoParamsObj,
    get_waited_2_update_db_data_from_server,)

from fzutils.spider.async_always import *

class TBUpdater(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/淘宝/实时更新/')
        self.sql_cli = None
        self.goods_index = 1
        # 并发量
        self.concurrency = 50
        # self.server_ip = 'http://0.0.0.0:5000'
        self.server_ip = 'http://118.31.39.97'

    async def _update_db(self):
        '''
        实时更新数据
        :return:
        '''
        while True:
            # 长期运行报: OSError: [Errno 24] Too many open files, 故不采用每日一志
            # self.lg = await self._get_new_logger(logger_name=get_uuid1())
            result = await self._get_db_old_data()
            if result is None:
                pass
            else:
                self.goods_index = 1
                tasks_params_list = TasksParamsListObj(tasks_params_list=result, step=self.concurrency)
                self.taobao = TaoBaoLoginAndParse(logger=self.lg)
                index = 1
                while True:
                    try:
                        slice_params_list = tasks_params_list.__next__()
                    except AssertionError:
                        break

                    tasks = []
                    for item in slice_params_list:
                        db_goods_info_obj = TBDbGoodsInfoObj(item=item, logger=self.lg)
                        self.lg.info('创建 task goods_id: {}'.format(db_goods_info_obj.goods_id))
                        tasks.append(self.loop.create_task(self._update_one_goods_info(
                            db_goods_info_obj=db_goods_info_obj,
                            index=index)))
                        index += 1

                    res = await _get_async_task_result(tasks=tasks, logger=self.lg)
                    await self._except_sleep(res=res)

                self.lg.info('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)
            if get_shanghai_time().hour == 0:  # 0点以后不更新
                await async_sleep(60 * 60 * 5.5)
            else:
                await async_sleep(5.)
            try:
                # del self.lg
                del result
            except:
                pass
            collect()

    async def _get_db_old_data(self) -> (list, None):
        '''
        获取db需求更新的数据
        :return:
        '''
        # self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        # 使用sqlalchemy管理数据库连接池
        self.sql_cli = SqlPools()
        result = None
        try:
            # result = self.sql_cli._select_table(sql_str=tb_select_str_3,)
            result = await get_waited_2_update_db_data_from_server(
                server_ip=self.server_ip,
                _type='tb',
                child_type=0,)
        except TypeError:
            self.lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')
        except Exception:
            self.lg.error('遇到错误:', exc_info=True)

        await _print_db_old_data(logger=self.lg, result=result)

        return result

    async def _get_new_tb_obj(self, index) -> None:
        if index % 10 == 0:
            try:
                del self.taobao
            except:
                pass
            collect()
            self.taobao = TaoBaoLoginAndParse(logger=self.lg)

    async def _update_one_goods_info(self, db_goods_info_obj, index):
        '''
        更新单个goods
        :return:
        '''
        res = False
        await self._get_new_tb_obj(index=index)
        self.sql_cli = await _get_new_db_conn(
            db_obj=self.sql_cli,
            index=index,
            logger=self.lg,
            db_conn_type=2,
            remainder=50)
        if self.sql_cli.is_connect_success:
            self.lg.info('------>>>| 正在更新的goods_id为(%s) | --------->>>@ 索引值为(%s)' % (
                db_goods_info_obj.goods_id,
                str(index)))
            oo = self.taobao.get_goods_data(goods_id=db_goods_info_obj.goods_id)
            oo_is_delete = oo.get('is_delete', 0)  # 避免下面解析data错误休眠
            data = self.taobao.deal_with_data(goods_id=db_goods_info_obj.goods_id)
            if data != {}:
                data = get_goods_info_change_data(
                    target_short_name='tb',
                    logger=self.lg,
                    data = data,
                    db_goods_info_obj=db_goods_info_obj,)
                res = to_right_and_update_tb_data(
                    data=data,
                    pipeline=self.sql_cli,
                    logger=self.lg)

            else:
                if oo_is_delete == 1:
                    # 检索后下架状态的, res也设置为True
                    res = True
                else:
                    self.lg.info('------>>>| 休眠8s中...')
                    await async_sleep(delay=8, loop=self.loop)

        else:  # 表示返回的data值为空值
            self.lg.error('数据库连接失败，数据库可能关闭或者维护中')
            await async_sleep(delay=10, loop=self.loop)

        index += 1
        self.goods_index = index
        collect()
        # 国外服务器上可以缩短时间, 可以设置为0s
        await async_sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)  # 不能太频繁，与用户请求错开尽量

        return [db_goods_info_obj.goods_id, res]

    async def _except_sleep(self, res):
        '''
        异常休眠
        :param res:
        :return:
        '''
        count = 0
        all_count_fail_sleep_time = 100.
        sleep_time = 50.
        for item in res:
            try:
                if not item[1]:
                    count += 1
            except IndexError:
                pass
        self.lg.info('Fail count: {}个, 并发量: {}个'.format(count, self.concurrency))
        if count/self.concurrency >= .9:
            # 全失败的休眠方式
            self.lg.info('抓取异常!! 休眠{}s中...'.format(all_count_fail_sleep_time))
            await async_sleep(all_count_fail_sleep_time)

        else:
            if count >= int(self.concurrency/5):
                self.lg.info('抓取异常!! 休眠{}s中...'.format(sleep_time))
                await async_sleep(sleep_time)

        return None

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

class TBDbGoodsInfoObj(BaseDbCommomGoodsInfoParamsObj):
    def __init__(self, item: list, logger=None):
        BaseDbCommomGoodsInfoParamsObj.__init__(
            self,
            item=item,
            logger=logger,
        )

def _fck_run():
    _ = TBUpdater()
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