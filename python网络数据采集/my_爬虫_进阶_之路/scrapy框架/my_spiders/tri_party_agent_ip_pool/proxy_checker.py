# coding:utf-8

"""
@author = super_fazai
@File    : proxy_checker.py
@connect : superonesfazai@gmail.com
"""

from os import system
from fzutils.sql_utils import BaseSqlite3Cli
from fzutils.spider.async_always import *

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from db_controller import (
    create_proxy_obj_table,
    empty_db_proxy_data,)

# 避免函数名重复导致异常!
from utils import (
    proxy_checker_welcome_page,
    _get_proxy_list,
    _add_to_white_list,
    _get_local_ip,
    _get_api_url_call_frequency_sleep_time,
    _check_one_proxy,
    _get_ip_activity_time,
    _delete_proxy_item,
    _add_to_checked_proxy_list,
    _update_db,
    _insert_into_db,
    _get_db_old_data,
)
from settings import (
    CONCURRENCY_NUM,
    CHECKED_PROXY_SLEEP_TIME,
    MIN_IP_POOl_NUM,
)

class ProxyChecker(AsyncCrawler):
    """
    第三方代理高匿可用度验证器(可扩展)

        已验证(短效高匿代理[下面都为测试单日不限量版]):
        1. 快代理vip(包月:200, 高匿名数量极低)
        2. 蜻蜓代理(包月:240, 高匿数量大, 接口并发: 否[5-10s一次])
        3. 站大爷(包月:475, 太贵)
        4. 蘑菇代理(包月:499, 太贵, 高匿数量大)
    """
    def __init__(self, tri_id, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
        )
        self.concurrency = CONCURRENCY_NUM
        self.local_ip = ''                      # 本地ip值
        self.checked_proxy_list = []            # 已被验证的proxy的list
        self.CHECKED_PROXY_SLEEP_TIME = CHECKED_PROXY_SLEEP_TIME
        self.sqlite3_cli = BaseSqlite3Cli(db_path='proxy.db')
        self.tri_id = tri_id                    # 三方的id
        self.concurrent_type = 0
        proxy_checker_welcome_page()

    async def _fck_run(self) -> None:
        """
        main
        :return:
        """
        self.local_ip = _get_local_ip()
        create_proxy_obj_table()
        # 每次启动先清空一次过期table
        print('Empty db old ip...')
        empty_db_proxy_data()
        # TODO 避免报: linux server sqlite3 disk I/O error
        #  $ chmod 777 proxy_checker.py proxy.db
        # 添加本机到白名单
        _add_to_white_list(
            tri_id=self.tri_id,
            local_ip=self.local_ip,)
        self.checked_proxy_list = _get_db_old_data(
            tri_id=self.tri_id,
            sqlite3_cli=self.sqlite3_cli,)
        activity_time = _get_ip_activity_time(id=self.tri_id)
        # 非并发api_url单次调用频率的休眠时间
        api_url_call_frequency_sleep_time = _get_api_url_call_frequency_sleep_time(
            tri_id=self.tri_id,)
        while True:
            while len(self.checked_proxy_list) < MIN_IP_POOl_NUM:
                print('--->>> Ip Pool num: {} 个'.format(len(self.checked_proxy_list)))
                try:
                    # 单次请求api获取数据
                    proxy_list = _get_proxy_list(id=self.tri_id)
                except Exception:
                    print('sleep {}s ...'.format(4.5))
                    await async_sleep(4.5)
                    continue

                # pprint(proxy_list)
                if proxy_list == []:
                    if self.tri_id == 1:
                        # 只短暂休眠, server(请求频繁)一允许通过就会成功拿到数据
                        print('sleep {}s ...'.format(.5))
                        await async_sleep(.5)
                    else:
                        print('sleep {}s ...'.format(4.5))
                        await async_sleep(4.5)

                # 验证此次api返回数据的可用性
                check_res = await self._check_proxy_list(proxy_list=proxy_list)
                # pprint(check_res)
                self.checked_proxy_list = _add_to_checked_proxy_list(
                    check_res=check_res,
                    checked_proxy_list=self.checked_proxy_list,)
                _insert_into_db(
                    checked_proxy_list=self.checked_proxy_list,
                    sqlite3_cli=self.sqlite3_cli,)
                await async_sleep(api_url_call_frequency_sleep_time)    # 避免调用频次过快

            # 检验所有可用proxy
            if activity_time is None:
                # activity_time为空，则表明存活时间未知, 调用检测
                await self._check_proxy_list(
                    proxy_list=self.checked_proxy_list)
            else:
                pass

            # 删除checked_proxy_list中score低的proxy
            self.checked_proxy_list = _delete_proxy_item(
                tri_id=self.tri_id,
                checked_proxy_list=self.checked_proxy_list,)

            # 更新db proxy
            _update_db(
                checked_proxy_list=self.checked_proxy_list,
                sqlite3_cli=self.sqlite3_cli,)

            if activity_time is None:
                print('self.checked_proxy_list验证完毕, 进入休眠{}s...'.format(
                    self.CHECKED_PROXY_SLEEP_TIME))
                await async_sleep(self.CHECKED_PROXY_SLEEP_TIME)
            else:
                # activity_time不为空, 则实时监控
                pass

    async def _check_proxy_list(self, proxy_list):
        """
        验证代理ip可用度
        :return:
        """
        tasks_params_list = TasksParamsListObj(
            tasks_params_list=proxy_list,
            step=self.concurrency)
        all_res = []
        while True:
            try:
                slice_params_list = tasks_params_list.__next__()
            except AssertionError:
                break

            tasks = []
            for item in slice_params_list:
                tasks.append(self.loop.create_task(unblock_func(
                    func_name=_check_one_proxy,
                    func_args=[
                        self.local_ip,
                        item,
                    ],
                    default_res={},)))

            one_part_res = await async_wait_tasks_finished(tasks=tasks)
            for i in one_part_res:
                all_res.append(i)

        return all_res

    def __del__(self):
        try:
            del self.loop
        except:
            pass
        try:
            del self.sqlite3_cli
        except:
            pass
        collect()

def main():
    _ = ProxyChecker(tri_id=1)
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())

if __name__ == '__main__':
    main()