# coding:utf-8

'''
@author = super_fazai
@File    : distributed_tasks_producer.py
@connect : superonesfazai@gmail.com
'''

try:
    # debug python segmentation fault
    # use: python3 -X faulthandler xxx.py
    import faulthandler
    faulthandler.enable()
except ImportError as e:
    print(e)

from sys import path as sys_path
sys_path.append('..')

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from sql_str_controller import (
    tm_select_str_3,
    tb_select_str_3,
)
from settings import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
    REDIS_DB,
)

from redis import StrictRedis
from redis import ConnectionPool as RedisConnectionPool
from fzutils.sql_utils import create_dcs_tasks_in_redis
from fzutils.memory_utils import get_current_func_info_by_traceback
from fzutils.spider.async_always import *

# 设置并发类型
CONCURRENT_TYPE = 2
if CONCURRENT_TYPE == 2:
    gevent_monkey.patch_all()
else:
    pass

class DistributedTasksProducer(AsyncCrawler):
    """
    分布式任务生产者
    """
    def __init__(self):
        AsyncCrawler.__init__(
            self,
        )
        self.concurrency = 10
        self.concurrent_type = CONCURRENT_TYPE
        # redis dcs最大任务数
        self.max_tasks_num = 1500
        self.sleep_time = 8
        self.redis_pool = RedisConnectionPool(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=REDIS_DB,)
        self.base_name = 'fzhook'
        self.spider_name_list = [
            'tm0',
            'tb0',
        ]

    async def _fck_run(self):
        print(get_current_func_info_by_traceback(self=self,))
        for spider_name in self.spider_name_list:
            # 每次启动先清空老数据
            # 删除指定键
            self.del_keys_by_pattern(
                pattern='{base_name}:{spider_name}:*'.format(
                    base_name=self.base_name,
                    spider_name=spider_name, ))
        print('每次启动先清空老数据 !!')

        while True:
            print('\nnow_time: {}'.format(get_shanghai_time()))
            await self.execute_all_create_dcs_tasks()
            print('sleep {} s ...'.format(self.sleep_time))
            await async_sleep(self.sleep_time)

    async def execute_all_create_dcs_tasks(self):
        """
        执行所有创建分布式任务
        :return:
        """
        async def get_tasks_params_list():
            tasks_params_list = []
            for spider_name in self.spider_name_list:
                tasks_params_list.append({
                    'spider_name': spider_name,
                })

            return tasks_params_list

        def get_create_task_msg(k) -> str:
            return 'create task[where spider_name: {}] ...'.format(
                k['spider_name']
            )

        def get_now_args(k) -> list:
            return [
                k['spider_name'],
            ]

        one_res = await get_or_handle_target_data_by_task_params_list(
            loop=self.loop,
            tasks_params_list=await get_tasks_params_list(),
            func_name_where_get_create_task_msg=get_create_task_msg,
            func_name=self.create_dcs_tasks_in_redis_by_spider_name,
            func_name_where_get_now_args=get_now_args,
            func_name_where_handle_one_res=None,
            func_name_where_add_one_res_2_all_res=default_add_one_res_2_all_res2,
            one_default_res=None,
            step=self.concurrency,
            get_all_res=True,
            concurrent_type=self.concurrent_type,)

    @catch_exceptions(default_res=None)
    def create_dcs_tasks_in_redis_by_spider_name(self,
                                                 spider_name='tm0',) -> None:
        """
        根据spider_name创建分布式任务
        :return:
        """
        if spider_name == 'tm0':
            # tm 实时更新
            sql_str = tm_select_str_3
            # 唯一id所在位置
            unique_id_position = 1

        elif spider_name == 'tb0':
            # tb 实时更新
            sql_str = tb_select_str_3
            unique_id_position = 1

        else:
            raise ValueError('未知 spider_name: {}'.format(spider_name))

        redis_cli = StrictRedis(connection_pool=self.redis_pool,)
        db_keys_list = redis_cli.keys(
            pattern='{base_name}:{spider_name}:*'.format(
                base_name=self.base_name,
                spider_name=spider_name,
            ))
        # 二进制转str
        db_keys_list = [item.decode() for item in db_keys_list]
        # pprint(db_keys_list)
        db_keys_list_len = len(db_keys_list)

        if db_keys_list_len >= self.max_tasks_num:
            print('spider_name: {} db_keys_list_len: {}, 大于max_tasks_num, pass!'.format(
                spider_name,
                db_keys_list_len,))
            return None

        print('spider_name: {}, db_keys_list_len: {}'.format(
            spider_name,
            db_keys_list_len,))
        # 小于最大值则插入新值
        sql_cli = SqlServerMyPageInfoSaveItemPipeline()
        tmp_res = list(sql_cli._select_table(
            sql_str=sql_str,))
        # 不删, 否则abort退出
        # try:
        #     del sql_cli
        # except:
        #     pass

        if tmp_res is None:
            tmp_res = []

        target_list = []
        for item in tmp_res:
            key_name = '{base_name}:{spider_name}:{unique_id}'.format(
                base_name=self.base_name,
                spider_name=spider_name,
                unique_id=item[unique_id_position],)
            if key_name not in db_keys_list:
                target_list.append({
                    'unique_id': item[unique_id_position],
                    'value': item,
                })
            else:
                continue
        print('spider_name: {}, 新增待存储target_list_len: {}'.format(
            spider_name,
            len(target_list),
        ))

        # 存入
        create_dcs_tasks_in_redis(
            redis_pool=self.redis_pool,
            spider_name=spider_name,
            target_list=target_list,
            base_name=self.base_name,
            # True 以encoding解码存入
            decode_responses=True,
            key_expire=60 * 60,)

        return None

    def del_keys_by_pattern(self, pattern: str):
        """
        根据正则删除指定key
        :return:
        """
        redis_cli = StrictRedis(connection_pool=self.redis_pool)
        db_keys_list = list(redis_cli.keys(
            pattern=pattern))
        for item in db_keys_list:
            print('delete key_name: {} ...'.format(item.decode()))
            redis_cli.delete(item)

        return None

    def __del__(self):
        collect()

if __name__ == '__main__':
    loop = get_event_loop()
    producer = DistributedTasksProducer()
    loop.run_until_complete(producer._fck_run())