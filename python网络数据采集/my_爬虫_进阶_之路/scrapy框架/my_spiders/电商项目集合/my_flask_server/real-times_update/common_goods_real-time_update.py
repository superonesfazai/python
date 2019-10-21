# coding:utf-8

'''
@author = super_fazai
@File    : common_goods_real-time_update.py
@connect : superonesfazai@gmail.com
'''

try:
    # debug python segmentation fault
    # use: python3 -X faulthandler xxx.py
    import faulthandler
    faulthandler.enable()
except ImportError as e:
    print(e)

import platform
from os import system
from sys import path as sys_path
sys_path.append('..')

try:
    from celery_tasks import _get_tm_one_goods_info_task
except:
    pass

from tmall_parse_2 import TmallParse
from taobao_parse import TaoBaoLoginAndParse
from my_pipeline import (
    SqlServerMyPageInfoSaveItemPipeline,
    SqlPools,
)

from settings import (
    IS_BACKGROUND_RUNNING,
    MY_SPIDER_LOGS_PATH,
    TMALL_REAL_TIMES_SLEEP_TIME,
    TAOBAO_REAL_TIMES_SLEEP_TIME,
)
from sql_str_controller import (
    tm_select_str_3,
    tb_select_str_3,
)
from multiplex_code import (
    _get_new_db_conn,
    _print_db_old_data,
    to_right_and_update_data_by_goods_type,
    get_goods_info_change_data,
    get_waited_2_update_db_data_from_server,
    block_get_one_goods_info_task_by_external_type,
    get_waited_2_update_db_data_from_redis_server,
    TMDbGoodsInfoObj,
    TBDbGoodsInfoObj,
    handle_real_times_goods_one_res,
)

from fzutils.celery_utils import _get_celery_async_results
from fzutils.shell_utils import *
from fzutils.spider.async_always import *

# 启动的爬虫name
GOODS_SPIDER_NAME = None
# 设置并发类型
CONCURRENT_TYPE = 1
# 抓取类型
CRAWL_TYPE_ASYNCIO = 0
CRAWL_TYPE_CELERY = 1
# 抓取类型
CRAWL_TYPE = CRAWL_TYPE_ASYNCIO
# 待更新数据来源(0 sqlserver | 1 new_my_server | 2 redis)
DB_RES_FROM = 2
# db 连接类型(1 SqlServerMyPageInfoSaveItemPipeline | 2 SqlPools)
DB_CONN_TYPE = 1

class CommonGoodsRealTimeUpdater(AsyncCrawler):
    """常规商品实时更新"""
    def __init__(self):
        self.goods_spider_type = GOODS_SPIDER_NAME
        assert self.goods_spider_type is not None
        assert self.goods_spider_type in ('tb', 'tm'), \
            'self.goods_spider_type value异常!'
        AsyncCrawler.__init__(
            self,
            log_print=True,
            log_save_path=self.get_log_save_path(),
        )
        self.set_concurrency()
        self.crawl_type = CRAWL_TYPE_ASYNCIO
        self.concurrent_type = CONCURRENT_TYPE
        self.db_res_from = DB_RES_FROM
        self.db_conn_type = DB_CONN_TYPE
        self.sql_cli = None
        self.set_sql_cli()
        assert self.db_res_from in (0, 1, 2,), \
            'self.db_res_from value异常!'
        self.db_data_slice_num = 800
        self.is_real_times_update_call = True
        if 'armv7l-with-debian' in platform.platform():
            self.server_ip = 'http://0.0.0.0:80'
        else:
            self.server_ip = 'http://118.31.39.97'
            # self.server_ip = 'http://0.0.0.0:5000'

    def get_log_save_path(self) -> str:
        if self.goods_spider_type == 'tm':
            return MY_SPIDER_LOGS_PATH + '/天猫/实时更新/'

        elif self.goods_spider_type == 'tb':
            return MY_SPIDER_LOGS_PATH + '/淘宝/实时更新/'

        else:
            raise NotImplemented

    def set_concurrency(self) -> None:
        """
        设置并发量, log_save_path
        :return:
        """
        if self.goods_spider_type == 'tm':
            self.concurrency = 100
        elif self.goods_spider_type == 'tb':
            self.concurrency = 100
        else:
            raise NotImplemented

    def set_sql_cli(self):
        """
        设置连接类型
        :return:
        """
        if self.db_conn_type == 1:
            # 推荐
            self.sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        elif self.db_conn_type == 2:
            # 使用sqlalchemy管理数据库连接池
            self.sql_cli = SqlPools()
        else:
            raise ValueError('db_conn_type 值异常!')

    async def _update_db(self):
        while True:
            # 长期运行报: OSError: [Errno 24] Too many open files, 故不采用每日一志
            # self.lg = await self._get_new_logger(logger_name=get_uuid1())
            result = await self._get_db_old_data()
            if result is None:
                pass
            else:
                tasks_params_list = TasksParamsListObj(
                    tasks_params_list=result,
                    step=self.concurrency)
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

                self.lg.info('全部数据更新完毕'.center(100, '#'))

            if get_shanghai_time().hour == 0:
                # 0点以后不更新
                await async_sleep(60 * 60 * .5)
            else:
                await async_sleep(5.)

            try:
                # del self.lg
                del result
            except Exception:
                pass
            collect()

    async def _get_db_old_data(self) -> (list, None):
        """
        获取db需求更新的数据
        :return:
        """
        result = None
        try:
            if self.db_res_from == 0:
                if self.goods_spider_type == 'tm':
                    sql_str = tm_select_str_3
                elif self.goods_spider_type == 'tb':
                    sql_str = tb_select_str_3
                else:
                    raise NotImplemented

                result = list(self.sql_cli._select_table(
                    sql_str=sql_str,
                    logger=self.lg,))

            elif self.db_res_from == 1:
                result = await get_waited_2_update_db_data_from_server(
                    server_ip=self.server_ip,
                    _type=self.goods_spider_type,
                    child_type=0,)
            else:
                # 默认拿300个, 避免前100个失败率较高的情况下, 后面能继续更新
                result = get_waited_2_update_db_data_from_redis_server(
                    # eg: 'tm0'
                    spider_name=self.goods_spider_type + '0',
                    logger=self.lg,
                    slice_num=self.db_data_slice_num,)

        except TypeError:
            self.lg.error('TypeError错误, 原因数据库连接失败...(可能维护中)')

        await _print_db_old_data(logger=self.lg, result=result)

        return result

    async def _get_one_res(self, slice_params_list, index) -> tuple:
        """
        获取slice_params_list对应的one_res
        :param slice_params_list:
        :param index:
        :return: (list, int)
        """
        if self.crawl_type == CRAWL_TYPE_ASYNCIO:
            """asyncio"""
            if self.goods_spider_type == 'tm':
                tasks_params_list = self.get_tm_tasks_params_list(
                    slice_params_list=slice_params_list,
                    index=index,)
                func_name_where_get_create_task_msg = self.get_tm_create_task_msg
                func_name_where_get_now_args = self.get_tm_now_args
            elif self.goods_spider_type == 'tb':
                tasks_params_list = self.get_tb_tasks_params_list(
                    slice_params_list=slice_params_list,
                    index=index,)
                func_name_where_get_create_task_msg = self.get_tb_create_task_msg
                func_name_where_get_now_args = self.get_tb_now_args
            else:
                raise NotImplemented

            one_res = await get_or_handle_target_data_by_task_params_list(
                loop=self.loop,
                tasks_params_list=tasks_params_list,
                func_name_where_get_create_task_msg=func_name_where_get_create_task_msg,
                func_name=block_get_one_goods_info_task_by_external_type,
                func_name_where_get_now_args=func_name_where_get_now_args,
                func_name_where_handle_one_res=None,
                func_name_where_add_one_res_2_all_res=default_add_one_res_2_all_res2,
                one_default_res=(),
                step=self.concurrency,
                logger=self.lg,
                get_all_res=True,
                concurrent_type=self.concurrent_type,
            )
            # pprint(one_res)

        elif self.crawl_type == CRAWL_TYPE_CELERY:
            """celery"""
            tasks = []
            if self.goods_spider_type == 'tm':
                for item in slice_params_list:
                    index += 1
                    db_goods_info_obj = TMDbGoodsInfoObj(item=item, logger=self.lg)
                    self.lg.info('创建 task goods_id: {}'.format(db_goods_info_obj.goods_id))
                    tmp_item = self.get_tm_tmp_item(
                        site_id=db_goods_info_obj.site_id,
                        goods_id=db_goods_info_obj.goods_id, )
                    try:
                        async_obj = await self.create_tm_celery_obj(
                            goods_id=tmp_item,
                            index=index, )
                        tasks.append(async_obj)
                    except Exception:
                        continue
                one_res = await _get_celery_async_results(tasks=tasks)

            else:
                raise NotImplemented

        else:
            raise NotImplemented

        res = await handle_real_times_goods_one_res(
            # eg: 'tm', 'tb'
            goods_type=self.goods_spider_type,
            loop=self.loop,
            func_name_where_update_one_goods_info_in_db=self._update_one_goods_info_in_db,
            slice_params_list=slice_params_list,
            one_res=one_res,
            logger=self.lg,
        )
        try:
            del slice_params_list
        except:
            pass

        return (res, index)

    def get_tm_tasks_params_list(self, slice_params_list: list, index: int) -> list:
        tasks_params_list = []
        for item in slice_params_list:
            db_goods_info_obj = TMDbGoodsInfoObj(item=item, logger=self.lg)
            tmp_item = self.get_tm_tmp_item(
                site_id=db_goods_info_obj.site_id,
                goods_id=db_goods_info_obj.goods_id, )
            tasks_params_list.append({
                'db_goods_info_obj': db_goods_info_obj,
                'index': index,
                'tmp_item': tmp_item,
            })
            index += 1

        return tasks_params_list

    def get_tb_tasks_params_list(self, slice_params_list: list, index: int) -> list:
        tasks_params_list = []
        for item in slice_params_list:
            db_goods_info_obj = TBDbGoodsInfoObj(item=item, logger=self.lg)
            tasks_params_list.append({
                'db_goods_info_obj': db_goods_info_obj,
                'index': index,
            })
            index += 1

        return tasks_params_list

    @staticmethod
    def get_tm_create_task_msg(k) -> str:
        return 'create task[where is goods_id: {}, index: {}] ...'.format(
            k['db_goods_info_obj'].goods_id,
            k['index'],
        )

    @staticmethod
    def get_tb_create_task_msg(k) -> str:
        return 'create task[where is goods_id: {}, index: {}] ...'.format(
            k['db_goods_info_obj'].goods_id,
            k['index'],
        )

    def get_tm_now_args(self, k) -> list:
        return [
            'tm',
            k['tmp_item'],
            k['index'],
            self.lg,
        ]

    def get_tb_now_args(self, k) -> list:
        return [
            'tb',
            k['db_goods_info_obj'].goods_id,
            k['index'],
            self.lg,
        ]

    async def _update_one_goods_info_in_db(self,
                                           db_goods_info_obj,
                                           index,
                                           before_goods_data,
                                           end_goods_data) -> (list, tuple):
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
            remainder=25)
        if self.sql_cli.is_connect_success:
            self.lg.info('*' * 20 + ' updating goods_id: {}, index: {} ...'.format(
                db_goods_info_obj.goods_id,
                index,))
            # 避免下面解析data错误休眠
            before_goods_data_is_delete = before_goods_data.get('is_delete', 0)
            if end_goods_data != {}:
                data = get_goods_info_change_data(
                    # eg: 'tm', 'tb'
                    target_short_name=self.goods_spider_type,
                    logger=self.lg,
                    data=end_goods_data,
                    db_goods_info_obj=db_goods_info_obj,
                    sql_cli=self.sql_cli,)
                res = to_right_and_update_data_by_goods_type(
                    goods_type=self.goods_spider_type,
                    data=data,
                    pipeline=self.sql_cli,
                    logger=self.lg,)

            else:  # 表示返回的data值为空值
                if before_goods_data_is_delete == 1:
                    # 检索后下架状态的, res也设置为True
                    res = True
                else:
                    self.lg.info('goods_id: {}, 阻塞休眠7s中...'.format(
                        db_goods_info_obj.goods_id,
                    ))
                    await async_sleep(delay=7., loop=self.loop)
                    # 改为阻塞进程, 机器会挂
                    # sleep(7.)

        else:
            self.lg.error('数据库连接失败，数据库可能关闭或者维护中')
            await async_sleep(delay=8, loop=self.loop)

        collect()

        return [db_goods_info_obj.goods_id, res]

    async def create_tm_celery_obj(self, **kwargs):
        """
        创建celery obj
        :param kwargs:
        :return:
        """
        goods_id = kwargs.get('goods_id', [])
        index = kwargs['index']

        async_obj = _get_tm_one_goods_info_task.apply_async(
            args=[
                goods_id,
                index,
            ],
            expires=5 * 60,
            retry=False,
        )

        return async_obj

    @staticmethod
    def get_tm_tmp_item(site_id, goods_id):
        tmp_item = []
        # 从数据库中取出时，先转换为对应的类型
        if site_id == 3:
            tmp_item.append(0)
        elif site_id == 4:
            tmp_item.append(1)
        elif site_id == 6:
            tmp_item.append(2)

        tmp_item.append(goods_id)

        return tmp_item

    @staticmethod
    def get_jd_tmp_item(site_id, goods_id):
        tmp_item = []
        # 从数据库中取出时，先转换为对应的类型
        if site_id == 7 \
                or site_id == 8:
            tmp_item.append(0)
        elif site_id == 9:
            tmp_item.append(1)
        elif site_id == 10:
            tmp_item.append(2)

        tmp_item.append(goods_id)

        return tmp_item

    async def _except_sleep(self, res):
        """
        异常休眠
        :param res:
        :return:
        """
        count = 0
        all_count_fail_sleep_time = 100.

        # 本来是40., 此处不休眠
        sleep_time = 0.
        # pprint(res)
        for item in res:
            try:
                if not item[1]:
                    count += 1
            except IndexError:
                pass
        self.lg.info('Fail count: {}个, 并发量: {}个'.format(count, self.concurrency))
        if count/self.concurrency >= .96:
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


goods_spider_name_help = 'value in ("tb", "tm",)'
db_res_from_help = 'value in (0 sqlserver | 1 new_my_server | 2 redis(推荐))'
crawl_type_help = 'value in (0 asyncio | 1 celery)'
db_conn_type_help = 'value in (1 SqlServerMyPageInfoSaveItemPipeline(推荐) | 2 SqlPools)'


@click_command()
@click_option('--goods_spider_name', type=str, default=None, help=goods_spider_name_help)
@click_option('--db_res_from', type=int, default=2, help=db_res_from_help)
@click_option('--crawl_type', type=int, default=0, help=crawl_type_help)
@click_option('--db_conn_type', type=int, default=1, help=db_conn_type_help)
def init_spider(goods_spider_name, db_res_from, crawl_type, db_conn_type):
    global GOODS_SPIDER_NAME, CONCURRENT_TYPE, DB_RES_FROM
    global CRAWL_TYPE, DB_CONN_TYPE

    # 报错segmentation fault解决方案
    try:
        cmd_str = 'ulimit -s 65536'
        system(cmd_str)
        cmd_str = 'ulimit -n 65536'
        system(cmd_str)
    except Exception as e:
        print('遇到错误:', e)

    GOODS_SPIDER_NAME = goods_spider_name
    DB_RES_FROM = db_res_from
    CRAWL_TYPE = crawl_type
    DB_CONN_TYPE = db_conn_type
    # CONCURRENT_TYPE设置为定值
    if GOODS_SPIDER_NAME == 'tm':
        CONCURRENT_TYPE = 1
    elif GOODS_SPIDER_NAME == 'tb':
        CONCURRENT_TYPE = 2
    else:
        raise NotImplemented

    if CONCURRENT_TYPE == 2:
        gevent_monkey.patch_all()
    else:
        pass

    if IS_BACKGROUND_RUNNING:
        main()
    else:
        _fck_run()


def _fck_run():
    # 遇到: PermissionError: [Errno 13] Permission denied: 'ghostdriver.log'
    # 解决方案: sudo touch /ghostdriver.log && sudo chmod 777 /ghostdriver.log
    _ = CommonGoodsRealTimeUpdater()
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
    init_spider()