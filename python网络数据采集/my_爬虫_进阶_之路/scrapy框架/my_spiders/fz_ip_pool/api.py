# coding:utf-8

'''
@author = super_fazai
@File    : api.py
@connect : superonesfazai@gmail.com
'''

"""
ip pools API
"""

from pickle import dumps
from random import choice
from pprint import pprint
from gc import collect
from settings import high_proxy_list_key_name
from fzutils.sql_utils import BaseRedisCli
from fzutils.safe_utils import get_uuid3
from fzutils.data.pickle_utils import deserializate_pickle_object

class IpPoolsObj(object):
    def __init__(self):
        self.redis_cli = BaseRedisCli()
        # self._k = get_uuid3('proxy_tasks')
        self._k = get_uuid3(high_proxy_list_key_name)

    def _get_all_ip_proxy(self) -> list:
        '''得到所有ip proxy'''
        _ = deserializate_pickle_object(self.redis_cli.get(name=self._k) or dumps([]))

        return _

    def _get_random_ip_proxy(self) -> str:
        '''
        随机获取一个代理
        :return: 格式: 'http://175.6.2.174:8088'
        '''
        _ = self._get_all_ip_proxy()
        if _ == []:
            return ''

        random_porxy = choice(_)

        return 'http://{}:{}'.format(
            random_porxy.get('ip'),
            random_porxy.get('port'))

    def __del__(self):
        try:
            del self.redis_cli
        except:
            pass
        collect()

ip_pools = IpPoolsObj()
# print(ip_pools._get_random_ip_proxy())
all_ip_proxy = ip_pools._get_all_ip_proxy()
pprint(all_ip_proxy)
print(len(all_ip_proxy))
