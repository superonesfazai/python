# coding:utf-8

from requests import get
import gc
from pickle import dumps
from random import randint
from .sql_utils import BaseRedisCli
from .safe_utils import get_uuid3
from .data.pickle_utils import deserializate_pickle_object

__all__ = [
    'MyIpPools',
    'IpPools',
]

ip_proxy_pool = 'IPProxyPool'
fz_ip_pool = 'fz_ip_pool'

class MyIpPools(object):
    def __init__(self, type=ip_proxy_pool, high_conceal=False):
        '''
        :param type: 所使用ip池类型
        :param high_conceal: 是否初始化为高匿代理
        '''
        super(MyIpPools, self).__init__()
        self.high_conceal = high_conceal
        self.type = type
        self.redis_cli = BaseRedisCli() if self.type == fz_ip_pool else None
        self.h_key = get_uuid3('h_proxy_list') if self.redis_cli is not None else None

    def get_proxy_ip_from_ip_pool(self):
        '''
        从代理ip池中获取到对应ip
        :return: dict类型 {'http': ['http://183.136.218.253:80', ...]}
        '''
        if self.type == ip_proxy_pool:
            if self.high_conceal:
                base_url = 'http://127.0.0.1:8000/?types=0' # types: 0高匿|1匿名|2透明
            else:
                base_url = 'http://127.0.0.1:8000'
            try:
                result = get(base_url).json()
            except Exception as e:
                print(e)
                return {'http': None}

            proxy_list = []
            for item in result:
                if item[2] > 7:
                    tmp_url = 'http://{}:{}'.format(item[0], item[1])
                    proxy_list.append(tmp_url)
                else:
                    delete_url = 'http://127.0.0.1:8000/delete?ip='
                    delete_info = get(delete_url + item[0])

        elif self.type == fz_ip_pool:
            _ = deserializate_pickle_object(
                pickle_object=self.redis_cli.get(name=self.h_key) or dumps([]),
                default_res=[])
            proxy_list = ['http://{}:{}'.format(i.get('ip', ''), i.get('port', '')) for i in _]

        else:
            raise ValueError('type值异常, 请检查!')

        return {
            'http': proxy_list,
        }

    def _get_random_proxy_ip(self):
        '''
        随机获取一个代理ip: 格式 'http://175.6.2.174:8088'
        :return:
        '''
        ip_list = self.get_proxy_ip_from_ip_pool().get('http')
        try:
            if isinstance(ip_list, list):
                proxy_ip = ip_list[randint(0, len(ip_list) - 1)]  # 随机一个代理ip
            else:
                raise TypeError
        except Exception:
            print('从ip池获取随机ip失败...正在使用本机ip进行爬取!')
            proxy_ip = False

        return proxy_ip

    def _empty_ip_pools(self):
        '''
        清空ip池
        :return:
        '''
        if self.type == ip_proxy_pool:
            base_url = 'http://127.0.0.1:8000'
            result = get(base_url).json()

            delete_url = 'http://127.0.0.1:8000/delete?ip='

            for item in result:
                if item[2] < 11:
                    delete_info = get(delete_url + item[0])
                    print(delete_info.text)
        elif self.type == fz_ip_pool:
            self.redis_cli.set(self.h_key, '')

        return None

    def __del__(self):
        try:
            del self.redis_cli
        except: pass
        gc.collect()

class IpPools(MyIpPools):
    pass