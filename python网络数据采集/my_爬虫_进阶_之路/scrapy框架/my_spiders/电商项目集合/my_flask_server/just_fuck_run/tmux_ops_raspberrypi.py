# coding:utf-8

'''
@author = super_fazai
@File    : tmux_ops_raspberrypi.py
@connect : superonesfazai@gmail.com
'''

"""
自动化tmux 脚本
"""

from sys import path as sys_path
sys_path.append('..')
from fzutils.spider.async_always import *

class TmuxOps(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
        )
        self.python_version_cmd = 'python3.6'
        self.spike_path = '~/myFiles/python/my_flask_server/spike_everything'
        self.pintuan_path = '~/myFiles/python/my_flask_server/pintuan_script'
        self.real_path = '~/myFiles/python/my_flask_server/real-times_update'
        self.logs_path = '~/myFiles/python/my_flask_server/logs'
        self.zwm_path = '~/myFiles/python/my_flask_server'
        self.ip_pool_path = '~/myFiles/tri_party_agent_ip_pool'
        self.fck_run_path = '~/myFiles/python/my_flask_server/just_fuck_run'
        self.dcs_path = '~/myFiles/python/my_flask_server/distribute_jobs'

    async def _fck_run(self):
        print('开始执行tmux 命令集合...')
        tmux_cmd_list = await self.get_tmux_cmd_list()
        bulk_execute_order_cmd_by_tmux_cmd_list(
            tmux_cmd_list=tmux_cmd_list,)
        print('执行完毕!')

    async def get_tmux_cmd_list(self) -> list:
        """
        :return:
        """
        return [
            {
                'page_name': 'redis_server',
                'cmd': 'cd ~ && redis-server',
                'delay_time': 2,
            },
            {
                'page_name': 'cpolar_http',
                'cmd': 'cd ~ && ./cpolar http 80',
                'delay_time': 2,
            },
            {
                'page_name': 'ip_pool',
                'cmd': 'cd {} && {} proxy_checker.py'.format(
                    self.ip_pool_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            {
                'page_name': 'ip_server',
                'cmd': 'cd {} && {} server.py'.format(
                    self.ip_pool_path,
                    self.python_version_cmd,
                ),
                'delay_time': 20,
            },
            {
                'page_name': 'new_my_server',
                'cmd': 'cd {} && {} new_my_server.py'.format(
                    self.zwm_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            {
                'page_name': 'just_fck_run',
                'cmd': 'cd {} && {} just_fck_run_raspberrypi.py'.format(
                    self.fck_run_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            # 已在just_fck_run_raspberrypi.py 中监控
            # {
            #     'page_name': 'dcs_producer',
            #     'cmd': 'cd {} && {} -X faulthandler distributed_tasks_producer.py'.format(
            #         self.dcs_path,
            #         self.python_version_cmd,
            #     ),
            #     'delay_time': 2,
            # },
            {
                'page_name': 'jd0',
                'cmd': 'cd {} && {} jd_real-times_update.py'.format(
                    self.real_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            {
                'page_name': 'tb0',
                'cmd': 'cd {} && {} taobao_real-times_update.py'.format(
                    self.real_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            {
                'page_name': 'tb1',
                'cmd': 'cd {} && {} taobao_real-times_update.py'.format(
                    self.real_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            # tm 实时更新, 测试发现: 3个出错率低
            {
                'page_name': 'tm0',
                'cmd': 'cd {} && {} tmall_real-times_update.py'.format(
                    self.real_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            {
                'page_name': 'tm1',
                'cmd': 'cd {} && {} tmall_real-times_update.py'.format(
                    self.real_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            {
                'page_name': 'tm2',
                'cmd': 'cd {} && {} tmall_real-times_update.py'.format(
                    self.real_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            {
                'page_name': 'jp0',
                'cmd': 'cd {} && {} juanpi_real-times_update.py'.format(
                    self.real_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            {
                'page_name': 'zwm',
                'cmd': 'cd {} && {} zwm_spider.py'.format(
                    self.zwm_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            {
                'page_name': 'logs',
                'cmd': 'cd {} && {} expired_logs_deal_with.py'.format(
                    self.logs_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
        ]

    def __del__(self):
        collect()

def main():
    tmux_ops = TmuxOps()
    loop = get_event_loop()
    loop.run_until_complete(tmux_ops._fck_run())

if __name__ == '__main__':
    main()