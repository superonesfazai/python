# coding:utf-8

'''
@author = super_fazai
@File    : spider_effic.py
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from my_exceptions import SqlServerConnectionException
from gc import collect
from concurrent.futures import ThreadPoolExecutor
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

class SpiderInfo(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
            ip_pool_type=tri_ip_pool,
        )
        self.concurrency = 20
        # with ThreadPoolExecutor(max_workers=10) as executor:
        self.executor = ThreadPoolExecutor(max_workers=self.concurrency)
        # 设置最大的统计截止num
        self.total_num = 200

    def _get_sql_params(self, before_time, end_time):
        """
        获取sql params
        :param before_time:
        :param end_time:
        :return:
        """
        return tuple([
            '[]',
            '[]',
            before_time,
            end_time,
        ])

    async def some_spider_crawl_effic(self, sql_str, time_period=3 * 60) -> list:
        """
        获取某spider采集效率
        :return:
        """
        async def get_tasks_params_list() -> list:
            tasks_params_list = []
            for index in range(1, self.total_num + 1):
                tasks_params_list.append({
                    'index': index,
                })

            return tasks_params_list

        async def get_one_res(slice_params_list) -> list:
            tasks = []
            for k in slice_params_list:
                index = k['index']
                print('create task[where index: {}] ...'.format(index))
                tasks.append(self.loop.create_task(self.async_get_save_2_db_count_by_time_period(
                    sql_str=sql_str,
                    index=index,
                    now_timestamp=now_timestamp,
                    time_period=time_period,
                )))

            one_res = await async_wait_tasks_finished(tasks=tasks)
            try:
                del tasks
            except:
                pass

            return one_res

        now_timestamp = datetime_to_timestamp(get_shanghai_time())
        tasks_params_list = await get_tasks_params_list()
        tasks_params_list = TasksParamsListObj(tasks_params_list=tasks_params_list, step=self.concurrency)
        all_res = []
        while True:
            try:
                slice_params_list = tasks_params_list.__next__()
            except AssertionError:
                break

            one_res = await get_one_res(slice_params_list=slice_params_list)
            for i in one_res:
                all_res.append(i)
            try:
                del one_res
            except:
                pass

        print(all_res)
        print(len(all_res))

        total = 0
        # 只计算非空的
        not_null_dict_count = 0
        for item in all_res:
            if item != {}:
                not_null_dict_count += 1

            count = item.get('count', 0)
            total += count

        print('ave_count: {}个'.format(total/not_null_dict_count))

        return all_res

    def get_save_2_db_count_by_time_period(self, sql_str, index, now_timestamp, time_period) -> dict:
        """
        获取某个时间区间的采集信息
        :param index:
        :param now_timestamp:
        :param time_period:
        :return:
        """
        before_time = get_some_time(now_timestamp=now_timestamp, index=index + 1, time_period=time_period)
        end_time = get_some_time(now_timestamp=now_timestamp, index=index, time_period=time_period)
        middle_time = timestamp_to_regulartime(int(datetime_to_timestamp(string_to_datetime(before_time))) + .5 * time_period)
        # print('index: {}, before_time: {}, middle_time: {}, end_time: {}'.format(index, before_time, middle_time, end_time))
        sql_params = self._get_sql_params(
            before_time=before_time,
            end_time=end_time,)

        res = {}
        try:
            sql_cli = SqlServerMyPageInfoSaveItemPipeline()
            if not sql_cli.is_connect_success:
                raise SqlServerConnectionException

            count = int(sql_cli._select_table(
                sql_str=sql_str,
                params=sql_params)[0][0])
            try:
                del sql_cli
            except:
                pass
            # TODO 此处不进行垃圾回收, 否则报对象无法被回收异常: malloc: *** error for object 0x10297b000: pointer being freed was not allocated
            # collect()
        except Exception as e:
            print(e)
            print('[-] index: {}, middle_time: {}, count: 0'.format(index, middle_time,))

            return res

        print('[+] index: {}, middle_time: {}, count: {}'.format(index, middle_time, count))
        res = {
            'index': index,
            'before_time': before_time,
            'middle_time': middle_time,
            'end_time': end_time,
            'count': count,
        }

        return res

    async def async_get_save_2_db_count_by_time_period(self, sql_str, index, now_timestamp, time_period) -> dict:
        """
        非阻塞获取某个时间区间的采集信息
        :param index:
        :param now_timestamp:
        :param time_period:
        :return:
        """
        async def _get_args() -> list:
            """获取args"""
            return [
                sql_str,
                index,
                now_timestamp,
                time_period,
            ]

        loop = get_event_loop()
        args = await _get_args()
        res = {}
        try:
            res = await loop.run_in_executor(self.executor, self.get_save_2_db_count_by_time_period, *args)
        except Exception as e:
            print(e)
        finally:
            # loop.close()
            try:
                del loop
            except:
                pass
            # collect()

            return res

    def __del__(self):
        try:
            self.loop
        except:
            pass
        collect()

def get_some_time(now_timestamp, index, time_period) -> str:
    return timestamp_to_regulartime(now_timestamp - index * time_period)

if __name__ == '__main__':
    _ = SpiderInfo()
    loop = get_event_loop()
    # company_spider
    sql_str = '''
    select count(id)
    from dbo.company_info
    where site_id=5
    and (phone != %s or email_address != %s)
    and create_time >= %s 
    and create_time <= %s
    '''
    res = loop.run_until_complete(_.some_spider_crawl_effic(
        sql_str=sql_str,
    ))