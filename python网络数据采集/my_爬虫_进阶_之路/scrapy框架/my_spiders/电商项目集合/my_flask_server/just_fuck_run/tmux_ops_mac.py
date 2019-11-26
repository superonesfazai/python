# coding:utf-8

'''
@author = super_fazai
@File    : tmux_ops_mac.py
@connect : superonesfazai@gmail.com
'''

from sys import path as sys_path
sys_path.append('..')
from fzutils.spider.async_always import *

class TmuxOps(AsyncCrawler):
    def __init__(self):
        AsyncCrawler.__init__(
            self,
        )
        self.python_version_cmd = 'python3'
        self.cp_path = '/Users/afa/myFiles/codeDoc/pythonDoc/python/python网络数据采集/my_爬虫_进阶_之路/scrapy框架/my_spiders/电商项目集合/my_flask_server/cp'
        self.zwm_path = '/Users/afa/myFiles/codeDoc/pythonDoc/python/python网络数据采集/my_爬虫_进阶_之路/scrapy框架/my_spiders/电商项目集合/my_flask_server'
        self.redis_path = '~'
        self.comment_spiders_path = '/Users/afa/myFiles/codeDoc/pythonDoc/python/python网络数据采集/my_爬虫_进阶_之路/scrapy框架/my_spiders/电商项目集合/my_flask_server/comment_spiders'
        self.goods_keywords_spider_path = '/Users/afa/myFiles/codeDoc/pythonDoc/python/python网络数据采集/my_爬虫_进阶_之路/scrapy框架/my_spiders/电商项目集合/my_flask_server/goods_keywords_spiders'

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
                'page_name': 'redis',
                'cmd': 'cd {} && redis-server /usr/local/etc/redis.conf'.format(
                    self.redis_path,
                ),
                'delay_time': 3,
            },
            # 不打印日志, 占用内存少
            {
                'page_name': 'celery_tasks',
                'cmd': 'cd {} && celery multi start w0 w1 --app=celery_tasks --concurrency=250 --pool=gevent --pidfile=/Users/afa/myFiles/my_spider_logs/celery/run/%N.pid --logfile=/Users/afa/myFiles/my_spider_logs/celery/log/celery_tasks.log'.format(
                    self.zwm_path,
                ),
                'delay_time': 3,
            },
            {
                'page_name': 'all_comment_spider',
                'cmd': 'cd {} && {} all_comment_spider.py'.format(
                    self.comment_spiders_path,
                    self.python_version_cmd,
                ),
                'delay_time': 3,
            },
            # 每个商品有20条就够, 不要太多, 故这个先不跑
            # {
            #     'page_name': 'all_comment_real-times_update_spider',
            #     'cmd': 'cd {} && {} all_comment_real-times_update_spider.py'.format(
            #         self.comment_spiders_path,
            #         self.python_version_cmd,
            #     ),
            #     'delay_time': 3,
            # },
            {
                'page_name': 'goods_coupon_spider',
                'cmd': 'cd {} && {} goods_coupon_spider.py'.format(
                    self.zwm_path,
                    self.python_version_cmd,
                ),
                'delay_time': 3,
            },
            {
                'page_name': 'goods_keywords_spider',
                'cmd': 'cd {} && {} goods_keywords_spider.py'.format(
                    self.goods_keywords_spider_path,
                    self.python_version_cmd,
                ),
                'delay_time': 3,
            },
            # 需要进入输入账号
            {
                'page_name': 'recommend_good_ops',
                'cmd': 'cd {} && {} recommend_good_ops.py'.format(
                    self.cp_path,
                    self.python_version_cmd,
                ),
                'delay_time': 3,
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