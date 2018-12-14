# coding:utf-8

'''
@author = super_fazai
@File    : zhima_vps_ops.py
@connect : superonesfazai@gmail.com
'''

from __future__ import print_function

"""
芝麻vps ops(http://vps.zhimaruanjian.com/)
"""

import re
from os import popen
from random import choice
from subprocess import Popen as subprocess_popen
from subprocess import PIPE

class ZMVpsOps(object):
    """混播vps"""
    def __init__(self):
        pass

    def _run(self):
        pass

    @classmethod
    def _init_vps(cls):
        '''
        初始化拨号功能
        :return:
        '''
        res = popen('./init.sh').read()
        print(res)

        return

    @classmethod
    def _get_area_info(cls):
        '''
        获取可用的区域信息
        :return: list
        '''
        _ = popen('/usr/local/bin/vpscmd -areaID=help').read().split('\n')
        area_list = []
        for item in _:
            o = re.compile('{(\w+-\d+) ').findall(item)[0]
            area_list.append(o)

        return area_list

    @classmethod
    def _dial_num(cls):
        '''
        拨号
        :return: bool
        '''
        area_list = cls._get_area_info()
        one = choice(area_list)
        res = popen('./dial.sh {}'.format(one)).read()
        if '成功' in res:
            return True
        else:
            return False

    @classmethod
    def _install_tiny_proxy(cls):
        '''
        安装tinyproxy
        :return: bool
        '''
        # 安装前先重新拨号
        dial_res = cls._dial_num()
        if not dial_res:
            return False

        print('正在yum update -y ...')
        popen = subprocess_popen('yum update -y', stdout=PIPE)
        cls.oo(popen)

        print('正在yum install -y epel-release ...')
        popen = subprocess_popen('yum install -y epel-release', stdout=PIPE)
        cls.oo(popen)

        print('正在yum install -y tinyproxy ...')
        popen = subprocess_popen('yum install -y tinyproxy', stdout=PIPE)
        cls.oo(popen)

        # 修改conf
        cls._modify_tiny_proxy_conf()

        # 重启
        cls._restart_tiny_proxy_service()

        return True

    @classmethod
    def _restart_tiny_proxy_service(cls):
        '''
        重启tinyproxy
        :return:
        '''
        print('重启tinyproxy...')
        popen = subprocess_popen('systemctl enable tinyproxy.service', stdout=PIPE)
        cls.oo(popen)
        popen = subprocess_popen('systemctl restart  tinyproxy.service', stdout=PIPE)
        cls.oo(popen)

        return

    @classmethod
    def oo(cls, popen):
        while True:
            try:
                print(popen.stdout.readline())
            except:
                break

    @classmethod
    def _modify_tiny_proxy_conf(cls):
        '''
        修改tinyproxy配置文件
        :return:
        '''
        tiny_proxy_conf_path = '/etc/tinyproxy/tinyproxy.conf'
        f = open(tiny_proxy_conf_path, 'r')

        w_str = ''
        for line in f:
            if re.search('Allow 127\.0\.0\.1', line):
                line = re.sub('Allow 127\.0\.0\.1', '#Allow 127.0.0.1', line)
            else:
                pass
            w_str += line
        f.close()

        # print(w_str)
        with open(tiny_proxy_conf_path, 'w') as w:
            w.write(w_str)

        return

if __name__ == '__main__':
    _ = ZMVpsOps()
    _._run()
