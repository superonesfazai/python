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

try:
    # debug python segmentation fault
    # use: python3 -X faulthandler xxx.py
    import faulthandler
    faulthandler.enable()
except ImportError as e:
    print(e)

import sys
import platform
from os import system
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
    get_waited_2_update_db_data_from_server,
    block_get_one_goods_info_task_by_external_type,
)

from fzutils.spider.async_always import *

# 设置并发类型
CONCURRENT_TYPE = 2
if CONCURRENT_TYPE == 2:
    gevent_monkey.patch_all()
else:
    pass

class TBUpdater(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            log_print=True,
            log_save_path=MY_SPIDER_LOGS_PATH + '/淘宝/实时更新/')
        self.sql_cli = None
        # 1 SqlServerMyPageInfoSaveItemPipeline | 2 SqlPools
        self.db_conn_type = 1
        self.goods_index = 1
        # 并发量
        self.concurrency = 100
        self.concurrent_type = CONCURRENT_TYPE
        if 'armv7l-with-debian' in platform.platform():
            self.server_ip = 'http://0.0.0.0:80'
        else:
            self.server_ip = 'http://118.31.39.97'
            # self.server_ip = 'http://0.0.0.0:5000'

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
                self.taobao = TaoBaoLoginAndParse(logger=self.lg, is_real_times_update_call=True)
                index = 1
                while True:
                    try:
                        slice_params_list = tasks_params_list.__next__()
                    except AssertionError:
                        break

                    one_res, index = await self._get_one_res(
                        slice_params_list=slice_params_list,
                        index=index)
                    await self._except_sleep(res=one_res)

                self.lg.info('全部数据更新完毕'.center(100, '#'))  # sleep(60*60)

            if get_shanghai_time().hour == 0:
                # 0点以后不更新
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
        if self.db_conn_type == 1:
            self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        elif self.db_conn_type == 2:
            # 使用sqlalchemy管理数据库连接池
            self.sql_cli = SqlPools()
        else:
            raise ValueError('db_conn_type 值异常!')

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

    async def _get_one_res(self, slice_params_list: list, index) -> tuple:
        """
        获取slice_params_list对应的one_res
        :param slice_params_list:
        :param index:
        :return: (list, int)
        """
        def get_tasks_params_list(slice_params_list: list, index: int) -> list:
            tasks_params_list = []
            for item in slice_params_list:
                db_goods_info_obj = TBDbGoodsInfoObj(item=item, logger=self.lg)
                tasks_params_list.append({
                    'db_goods_info_obj': db_goods_info_obj,
                    'index': index,
                })
                index += 1

            return tasks_params_list

        def get_create_task_msg(k) -> str:
            return 'create task[where is goods_id: {}, index: {}] ...'.format(
                k['db_goods_info_obj'].goods_id,
                k['index'],)

        def get_now_args(k) -> list:
            return [
                'tb',
                k['db_goods_info_obj'].goods_id,
                k['index'],
                self.lg,
            ]

        async def handle_one_res(one_res: list):
            """
            one_res后续处理
            :param one_res:
            :return:
            """
            nonlocal slice_params_list

            # 获取新new_slice_params_list
            new_slice_params_list = []
            for item in slice_params_list:
                goods_id = item[1]
                for i in one_res:
                    # self.lg.info(str(i))
                    try:
                        goods_id2 = i[1]
                        index = i[2]
                        if goods_id == goods_id2:
                            new_slice_params_list.append({
                                'index': index,
                                'before_goods_data': i[3],
                                'end_goods_data': i[4],
                                'item': item,
                            })
                            break
                        else:
                            continue
                    except IndexError:
                        continue

            # 阻塞方式进行存储, 避免db高并发导致大量死锁
            tasks = []
            for k in new_slice_params_list:
                item = k['item']
                index = k['index']
                db_goods_info_obj = TBDbGoodsInfoObj(item=item, logger=self.lg)
                self.lg.info('create task[where is goods_id: {}, index: {}]...'.format(
                    db_goods_info_obj.goods_id,
                    index))
                tasks.append(self.loop.create_task(self._update_one_goods_info_in_db(
                    db_goods_info_obj=db_goods_info_obj,
                    index=index,
                    before_goods_data=k['before_goods_data'],
                    end_goods_data=k['end_goods_data'],)))

            # self.lg.error(str(one_res))
            # self.lg.error(str(tasks))
            one_res = await _get_async_task_result(
                tasks=tasks,
                logger=self.lg)
            # pprint(one_res)
            try:
                del new_slice_params_list
            except:
                pass

            return one_res

        # tasks = []
        # # method 1
        # for item in slice_params_list:
        #     db_goods_info_obj = TBDbGoodsInfoObj(item=item, logger=self.lg)
        #     self.lg.info('创建 task goods_id: {}'.format(db_goods_info_obj.goods_id))
        #     tasks.append(self.loop.create_task(self._update_one_goods_info(
        #         db_goods_info_obj=db_goods_info_obj,
        #         index=index)))
        #     index += 1
        #
        # res = await _get_async_task_result(tasks=tasks, logger=self.lg)

        # method 2
        one_res = await get_or_handle_target_data_by_task_params_list(
            loop=self.loop,
            tasks_params_list=get_tasks_params_list(
                slice_params_list=slice_params_list,
                index=index,),
            func_name_where_get_create_task_msg=get_create_task_msg,
            func_name=block_get_one_goods_info_task_by_external_type,
            func_name_where_get_now_args=get_now_args,
            func_name_where_handle_one_res=None,
            func_name_where_add_one_res_2_all_res=default_add_one_res_2_all_res2,
            one_default_res=(),
            step=self.concurrency,
            logger=self.lg,
            get_all_res=True,
            concurrent_type=self.concurrent_type,
        )
        # pprint(one_res)
        res = await handle_one_res(one_res=one_res)

        return (res, index)

    async def _update_one_goods_info_in_db(self, db_goods_info_obj, index, before_goods_data, end_goods_data):
        """
        更新单个goods
        :param db_goods_info_obj:
        :param index:
        :param before_goods_data:
        :param end_goods_data:
        :return:
        """
        res = False

        self.sql_cli = await _get_new_db_conn(
            db_obj=self.sql_cli,
            index=index,
            logger=self.lg,
            db_conn_type=self.db_conn_type,
            remainder=25,)
        if self.sql_cli.is_connect_success:
            self.lg.info('*' * 20 + ' updating goods_id: {}, index: {} ...'.format(
                db_goods_info_obj.goods_id,
                index, ))
            # 避免下面解析data错误休眠
            before_goods_data_is_delete = before_goods_data.get('is_delete', 0)
            if end_goods_data != {}:
                data = get_goods_info_change_data(
                    target_short_name='tb',
                    logger=self.lg,
                    data=end_goods_data,
                    db_goods_info_obj=db_goods_info_obj, )
                res = to_right_and_update_tb_data(
                    data=data,
                    pipeline=self.sql_cli,
                    logger=self.lg,)

            else:  # 表示返回的data值为空值
                if before_goods_data_is_delete == 1:
                    # 检索后下架状态的, res也设置为True
                    res = True
                else:
                    self.lg.info('goods_id: {}, 阻塞休眠7s中...'.format(
                        db_goods_info_obj.goods_id,))
                    await async_sleep(delay=7., loop=self.loop)
                    # 改为阻塞进程, 机器会挂
                    # sleep(7.)

        else:
            self.lg.error('数据库连接失败，数据库可能关闭或者维护中')
            await async_sleep(delay=5, loop=self.loop)

        await async_sleep(TAOBAO_REAL_TIMES_SLEEP_TIME)
        collect()

        return [db_goods_info_obj.goods_id, res]

    async def _get_new_tb_obj(self, index) -> None:
        if index % 10 == 0:
            try:
                del self.taobao
            except:
                pass
            collect()
            self.taobao = TaoBaoLoginAndParse(logger=self.lg, is_real_times_update_call=True)

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
            db_conn_type=self.db_conn_type,
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
            del self.sql_cli
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
    system_type = get_system_type()
    if system_type == 'Darwin':
        # local以守护进程运行
        # IS_BACKGROUND_RUNNING = True
        pass
    else:
        pass

    # 报错segmentation fault解决方案
    try:
        cmd_str = 'ulimit -s 32768'
        system(cmd_str)
    except Exception as e:
        print('遇到错误:', e)

    if IS_BACKGROUND_RUNNING:
        main()
    else:
        _fck_run()