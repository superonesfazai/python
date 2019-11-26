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
        self.cp_path = '~/myFiles/python/my_flask_server/cp'
        self.tejia_path = '~/myFiles/python/my_flask_server/tejia'

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
                'page_name': 'file_ulimit_set',
                'cmd': 'cd ~ && ulimit -n 80000',
                'delay_time': 2,
            },
            {
                'page_name': 'redis_server',
                'cmd': 'cd ~ && redis-server /etc/redis/redis.conf',
                'delay_time': 2,
            },
            {
                'page_name': 'cpolar_http',
                'cmd': 'cd ~ && ./cpolar http 80',
                'delay_time': 2,
            },
            {
                'page_name': 'ip_pool',
                'cmd': 'cd {} && {} proxy_checker_plus.py'.format(
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
                'delay_time': 25,
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
                'delay_time': 8,
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
                'cmd': 'cd {} && {} common_goods_real-time_update.py --goods_spider_name=tb'.format(
                    self.real_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            {
                'page_name': 'tb1',
                'cmd': 'cd {} && {} common_goods_real-time_update.py --goods_spider_name=tb'.format(
                    self.real_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            # tm 实时更新, 测试发现: 3个出错率低(mac不跑, pi上跑3个即可(多开的多为失败, 休眠100s)!)
            {
                'page_name': 'tm0',
                'cmd': 'cd {} && {} common_goods_real-time_update.py --goods_spider_name=tm'.format(
                    self.real_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            {
                'page_name': 'tm1',
                'cmd': 'cd {} && {} common_goods_real-time_update.py --goods_spider_name=tm'.format(
                    self.real_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            {
                'page_name': 'tm2',
                'cmd': 'cd {} && {} common_goods_real-time_update.py --goods_spider_name=tm'.format(
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
            # tejia
            {
                'page_name': 'tb_tejia',
                'cmd': 'cd {} && {} taobao_tiantiantejia.py'.format(
                    self.tejia_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            {
                'page_name': 'tb_tejia_update',
                'cmd': 'cd {} && {} taobao_tiantiantejia_real-times_update.py'.format(
                    self.tejia_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            # 拼团
            {
                'page_name': 'zhe_800_pintuan',
                'cmd': 'cd {} && {} zhe_800_pintuan.py'.format(
                    self.pintuan_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            {
                'page_name': 'zhe_800_pintuan_update',
                'cmd': 'cd {} && {} zhe_800_pintuan_real-times_update.py'.format(
                    self.pintuan_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            # server在跑, https
            # {
            #     'page_name': 'mia_pintuan',
            #     'cmd': 'cd {} && {} mia_pintuan.py'.format(
            #         self.pintuan_path,
            #         self.python_version_cmd,
            #     ),
            #     'delay_time': 2,
            # },
            {
                'page_name': 'mia_pintuan_update',
                'cmd': 'cd {} && {} mia_pintuan_real-times_update.py'.format(
                    self.pintuan_path,
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
            # 说周期性变化, 此处不跑这个了
            # {
            #     'page_name': 'cp_goods_info_monitor',
            #     'cmd': 'cd {} && {} cp_goods_info_monitor_spider.py'.format(
            #         self.cp_path,
            #         self.python_version_cmd,
            #     ),
            #     'delay_time': 2,
            # },
            {
                'page_name': 'db_timing_script',
                'cmd': 'cd {} && {} db_timing_script.py'.format(
                    self.cp_path,
                    self.python_version_cmd,
                ),
                'delay_time': 2,
            },
            {
                'page_name': 'recommend_good_ops',
                'cmd': 'cd {}'.format(
                    self.cp_path,
                ),
                'delay_time': 2,
            },
            {
                'page_name': 'cpolar_controler',
                'cmd': 'cd {} && {} cpolar_controler.py'.format(
                    self.cp_path,
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