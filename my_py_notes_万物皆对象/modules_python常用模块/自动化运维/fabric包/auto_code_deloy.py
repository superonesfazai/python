# coding:utf-8

'''
@author = super_fazai
@File    : auto_code_deloy.py
@Time    : 2018/7/25 09:57
@connect : superonesfazai@gmail.com
'''

"""
自动化代码部署(没打算用git)
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
    def judge_whether_file_exists(item, file_path):
        '''
        linux判断一个文件是否存在
        :param item:
        :param file_path: 必须传入文件的绝对路径
        :return: bool
        '''
        _ = item.run(
            command='[ -e \"{0}\" ] && echo 1 || echo 0'.format(file_path),
            hide=True)      # hide=True隐藏输出
        _ = str(_).replace('\n', '').replace('Command exited with status 0.=== stdout ===', '').replace('(no stderr)', '')
        if int(_) == 1:
            print('[+] 文件 {0} 原先存在!'.format(file_path))
            return True
        else:
            print('[-] 文件 {0} 原先不存在!'.format(file_path))
            return False

    def update_python_packages(item):
        '''更新python包'''
        try:
            _ = item.run('apt-get -f install && apt-get install unzip --fix-missing')
            _ = item.run('pip3 install --upgrade pip')
            _ = item.run('pip3 install -i http://pypi.douban.com/simple/ fzutils --trusted-host pypi.douban.com -U')
        except Exception as e:
            print(e)
            return False
        return True

    def upload_or_download_files(method, connect_object, local_file_path, remote_file_path):
        '''
        上传文件
        :param method: 上传的方式
        :param connect_object: 连接对象
        :param local_file_path: 本地待上传文件路径(必须是绝对路径)
        :param remote_file_path: server待上传文件路径(必须是绝对路径)
        :return: bool
        '''
        from os.path import (
            basename,
            dirname,)

        # 本地工作上下文path
        local_work_content = dirname(local_file_path)
        local_file_name = basename(local_file_path)

        # server工作上下文path
        remote_work_content = dirname(remote_file_path)
        remote_file_name = basename(remote_file_path)
        # print(remote_work_content)

        _ = False
        if method == 'put':
            try:
                connect_object.put(local=local_file_path, remote=remote_file_path)
                print('[+] 上传 {0} 到server成功!'.format(local_file_name))
                _ = True
            except Exception as e:
                print(e)
                print('[-] 上传 {0} 到server失败!'.format(local_file_name))

        elif method == 'get':   # TODO 此处get有问题, 先不使用
            try:
                connect_object.get(remote=remote_file_path, local=local_file_path)
                print('[+] 下载 {0} 到本地成功!'.format(remote_file_name))
                _ = True
            except Exception as e:
                print(e)
                print('[-] 下载 {0} 到本地失败!'.format(remote_file_name))

        else:   # method = 'get'
            raise ValueError('method只支持put or get 方法!')

        return _

    def backup_files(item):
        '''备份文件'''
        settings_file_path = '/root/myFiles/python/my_flask_server/settings.py'
        _ = judge_whether_file_exists(item=item, file_path=settings_file_path)
        if _:
            _ = item.run('cp {0} ~/settings.py'.format(settings_file_path))
            print('[+] 备份 settings.py 成功!')
            return True
        else:
            print('[-] 备份 settings.py 失败!')
            return False

    def local_compress_folders(folders_path, folders_name, default_save_path='/Users/afa/myFiles/tmp'):
        '''
        本地压缩文件夹
        :param folders_path: 文件夹所在目录地址
        :param folders_name: 要压缩的文件夹名
        :param default_save_path: 默认存储路径
        :return:
        '''
        from os import system

        '''用zip, unzip的原因是: mac与linux用tar存在解码冲突'''
        cmd = 'cd {0} && zip -r {1}.zip {2} && mv {3}.zip {4}'.format(
            folders_path,
            folders_name,
            './'+folders_name+'/*',
            folders_name,
            default_save_path           # 默认存储路径
        )
        try:
            system(cmd)
            print('\n[+] 本地压缩 {0}.zip 成功!'.format(folders_name))
            return True

        except Exception as e:
            print(e)
            print('\n[-] 本地压缩 {0}.zip 失败!'.format(folders_name))
            return False

    def remote_decompress_folders(connect_object, folders_path, target_decompress_path):
        '''
        server端解压文件, 并删除原压缩文件(默认解压到当前目录)
        :param connect_object:
        :param folders_path: 压缩文件的保存路径
        :param target_decompress_path: 目标解压路径
        :return:
        '''
        from os.path import basename

        # 先删除原始文件夹, 再进行解压覆盖, (否则无法覆盖)
        cmd = 'cd {0} && rm -rf {1} && unzip -o -O CP936 {2} && rm {3}'.format(
            target_decompress_path,
            basename(folders_path).split('.')[0],
            folders_path,
            folders_path)
        print(cmd)
        try:
            connect_object.run(cmd)
            print('[+] server端解压 {0}.zip 成功!'.format(folders_path))
            return True
        except Exception as e:
            print(e)
            print('[-] server端解压 {0}.zip 失败!'.format(folders_path))
            return False

    # 本地先压缩待上传的文件夹
    wait_2_compress_folders = [
        ('/Users/afa/myFiles', 'my_spider_logs'),
    ]
    [local_compress_folders(folders_path=o[0], folders_name=o[1]) for o in wait_2_compress_folders]
    for item in my_group:
        if not item.is_connected:
            print('正在处理{0}'.format(item.__repr__()).center(100, '='))
            # _ = item.sudo('apt-get update && apt-get upgrade -y')     # 不乱更新软件, 容易出现依赖问题

            # 更新软件包
            print('正在更新相关依赖包...')
            update_python_packages(item=item)

            # 执行上传文件操作
            print('正在上传相关文件...')
            file_path = [
                ('/Users/afa/my_company_db_info.json', '/root/my_company_db_info.json'),
                ('/Users/afa/my_username_and_passwd.json', '/root/my_username_and_passwd.json'),
                ('/Users/afa/myFiles/tmp/my_spider_logs.zip', '/root/myFiles/my_spider_logs.zip')
            ]
            [upload_or_download_files(
                method='put',
                connect_object=item,
                local_file_path=i[0],
                remote_file_path=i[1]
            ) for i in file_path]

            # 备份文件
            print('正在备份文件...')
            backup_files(item=item)

            # 解压相关压缩文件
            print('正在解压文件...')
            wait_2_decompress_folders = [
                '/root/myFiles/my_spider_logs.zip',
            ]
            [remote_decompress_folders(
                connect_object=item,
                folders_path=k,
                target_decompress_path='/root/myFiles/'
            ) for k in wait_2_decompress_folders]

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







