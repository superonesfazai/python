# coding:utf-8

'''
@author = super_fazai
@File    : auto_code_deloy.py
@Time    : 2018/7/25 09:57
@connect : superonesfazai@gmail.com
'''

"""
项目自动化部署(没打算用git)
"""

import re
from pprint import pprint
from fabric import (
    group,)
from fabric.connection import Connection
from fzutils.data.json_utils import read_json_from_local_json_file
from fzutils.auto_ops_utils import (
    upload_or_download_files,
    local_compress_folders,
    remote_decompress_folders,)

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
    def compress_folders():
        '''本地压缩文件夹'''
        # 本地先压缩待上传的文件夹
        wait_2_compress_folders = [
            ('/Users/afa/myFiles', 'my_spider_logs'),
            ('/Users/afa/myFiles/codeDoc/pythonDoc/python/python网络数据采集/my_爬虫_进阶_之路/scrapy框架/my_spiders/电商项目集合',
            'my_flask_server',)]
        [local_compress_folders(father_folders_path=o[0], folders_name=o[1]) for o in wait_2_compress_folders]

        return

    def update_python_packages(connect_object:Connection):
        '''更新python包'''
        print('正在更新相关依赖包...')
        try:
            connect_object.run('sudo apt-get update --fix-missing && sudo apt-get autoremove && sudo apt-get clean && apt-get -f install && apt-get install unzip --fix-missing')
            # connect_object.run('sudo apt-get install libcurl4-openssl-dev')   # for pycurl
            connect_object.run('pip3 install --upgrade pip')
            connect_object.run('pip3 install -i http://pypi.douban.com/simple/ fzutils --trusted-host pypi.douban.com -U')
        except Exception as e:
            print(e)
            return False
        return True

    def upload_base_files(item):
        '''上传基础文件'''
        # 执行上传文件操作
        print('正在上传相关文件...')
        file_path = [
            ('/Users/afa/my_company_db_info.json', '/root/my_company_db_info.json'),
            ('/Users/afa/my_username_and_passwd.json', '/root/my_username_and_passwd.json'),
            ('/Users/afa/myFiles/tmp/my_spider_logs.zip', '/root/myFiles/my_spider_logs.zip'),
            ('/Users/afa/myFiles/tmp/my_flask_server.zip', '/root/myFiles/python/my_flask_server.zip'),
        ]
        for i in file_path:
            upload_or_download_files(
                method='put',
                connect_object=item,
                local_file_path=i[0],
                remote_file_path=i[1])

        return

    def decompress_files(item):
        '''解压相关文件'''
        # 解压相关压缩文件
        print('正在解压文件...')
        wait_2_decompress_folders = [
            ('/root/myFiles/my_spider_logs.zip', '/root/myFiles/'),
            ('/root/myFiles/python/my_flask_server.zip', '/root/myFiles/python'),
        ]
        [remote_decompress_folders(
            connect_object=item,
            folders_path=k[0],
            target_decompress_path=k[1]
        ) for k in wait_2_decompress_folders]

        return

    def upload_and_replace_settings(item):
        '''上传替换settings.py'''
        # 替换原settings.py
        server_settings_file_path = [
            ('/Users/afa/server_settings/{0}/settings.py', '/root/myFiles/python/my_flask_server/settings.py'),
        ]
        for e in server_settings_file_path:
            if re.compile(r'118.31.39.97').findall(item.__repr__()) != []:
                r = (e[0].format(2), e[1])
            else:
                r = (e[0].format(3), e[1])
            upload_or_download_files(
                method='put',
                connect_object=item,
                local_file_path=r[0],
                remote_file_path=r[1])

        return

    compress_folders()
    for item in my_group:
        if not item.is_connected:
            print('正在处理{0}'.format(item.__repr__()).center(100, '='))
            # _ = item.sudo('apt-get update && apt-get upgrade -y')     # 不乱更新软件, 容易出现依赖问题

            update_python_packages(connect_object=item)
            upload_base_files(item=item)
            decompress_files(item=item)
            upload_and_replace_settings(item=item)

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