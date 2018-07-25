# coding:utf-8

'''
@author = super_fazai
@File    : auto_code_deloy.py
@Time    : 2018/7/25 09:57
@connect : superonesfazai@gmail.com
'''

"""
自动化代码部署
"""

from pprint import pprint
from fabric import (
    group,)
from fzutils.data.json_utils import read_json_from_local_json_file

host_json_path = '/Users/afa/hosts_info.json'

def get_env_hosts_info():
    '''
    得到hosts信息
    :return: a list eg: [{'ip': 'x', 'user': 'root', 'passwd': 'x', 'port': 22}, ...]
    '''
    _ = read_json_from_local_json_file(json_file_path=host_json_path)
    if _ == {}:
        print('获取hosts info失败!')
        return []
    else:
        _ = [item for item in _.get('hosts', [])]

    return _

def server_tasks(my_group):
    '''
    server tasks
    :param group:
    :return:
    '''
    for item in my_group:
        if not item.is_connected:
            print('正在处理{0}'.format(item.__repr__()).center(100, '='))
            # _ = item.sudo('apt-get update && apt-get upgrade -y')     # 不乱更新软件, 容易出现依赖问题
            _ = item.run('pip3 install --upgrade pip')
            _ = item.run('pip3 install -i http://pypi.douban.com/simple/ fzutils --trusted-host pypi.douban.com -U')
            _ = item.run(
                'cd /root/myFiles/my_spider_logs && '
                'mkdir 电商项目 '
            )
            print('{0}处理完毕'.format(item.__repr__()).center(100, '='))
        else:
            print('{0}连接失败!'.format(item))

def get_connected_hosts():
    '''
    连接所有主机, 并返回连接结果list
    :return: a list eg: [<连接对象>, ...]
    '''
    hosts_info = get_env_hosts_info()

    my_group = []
    for item in hosts_info:
        _ = group.Connection(
            host=item.get('ip'),
            user=item.get('user'),
            port=item.get('port'),
            connect_timeout=6,
            connect_kwargs={
                'password': item.get('passwd')
            }
        )
        my_group.append(_)
    # print(my_group)

    return my_group

def main():
    my_group = get_connected_hosts()
    server_tasks(my_group=my_group)

if __name__ == '__main__':
    main()







