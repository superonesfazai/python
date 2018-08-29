# coding:utf-8

'''
@author = super_fazai
@File    : auto_ops_utils.py
@Time    : 2016/7/27 11:38
@connect : superonesfazai@gmail.com
'''

"""
自动化运维相关包
"""

import os
import time
import re
from os import system
from os.path import (
    exists,
    basename,)
from os.path import (
    basename,
    dirname,)
from fabric.connection import Connection

from .time_utils import get_shanghai_time

__all__ = [
    'judge_whether_file_exists',                                # linux server端判断一个文件是否存在
    'upload_or_download_files',                                 # 上传/下载文件
    'local_compress_folders',                                   # 本地压缩文件夹
    'remote_decompress_folders',                                # server端解压文件, 并删除原压缩文件

    # github
    'auto_git',                                                 # master 自动 git
]

def judge_whether_file_exists(connect_object:Connection, file_path):
    '''
    linux server端判断一个文件是否存在
    :param connect_object:
    :param file_path: 文件绝对路径
    :return: bool
    '''
    result = False
    _ = connect_object.run(
        command='[ -e \"{0}\" ] && echo 1 || echo 0'.format(file_path),
        hide=True)  # hide=True隐藏输出
    _ = str(_).replace('\n', '').replace('Command exited with status 0.=== stdout ===', '').replace('(no stderr)', '')
    if int(_) == 1:
        print('[+] 文件 {0} 原先存在!'.format(file_path))
        _ = True
    else:
        print('[-] 文件 {0} 原先不存在!'.format(file_path))

    return result

def upload_or_download_files(method, connect_object:Connection, local_file_path, remote_file_path):
    '''
    上传/下载文件
        use: eg:
            upload_or_download_files(
                method='put',
                connect_object=xxx,
                local_file_path='/Users/afa/myFiles/tmp/my_spider_logs.zip',
                remote_file_path='/root/myFiles/my_spider_logs.zip'
            )
    :param method: 上传的方式
    :param connect_object: 连接对象
    :param local_file_path: 本地待上传文件路径(必须是绝对路径)
    :param remote_file_path: server待上传文件路径(必须是绝对路径)
    :return: bool
    '''
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

    elif method == 'get':
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

def local_compress_folders(father_folders_path, folders_name, default_save_path='/Users/afa/myFiles/tmp'):
    '''
    本地压缩文件夹
        use: eg:
            local_compress_folders(
                father_folders_path='/Users/afa/myFiles',
                folders_name='my_spider_logs',
                default_save_path='xxxxxx'
            )
    :param father_folders_path: 文件夹所在父目录地址
    :param folders_name: 要压缩的文件夹名
    :param default_save_path: 默认存储路径
    :return:
    '''
    if not exists(father_folders_path):
        raise ValueError('{0} 父目录地址不存在!请检查!'.format(father_folders_path))
    elif not exists(default_save_path):
        raise ValueError('{0} 存储路径不存在!请检查!'.format(default_save_path))
    else:
        pass

    _ = False
    '''用zip, unzip的原因是: mac与linux用tar存在解码冲突'''
    # 先cd 到父目录, 再压缩对应文件夹, 最后移动到默认保存目录
    cmd = 'cd {0} && zip -r {1}.zip {2} && mv {3}.zip {4}'.format(
        father_folders_path,
        folders_name,
        './'+folders_name+'/*',
        folders_name,
        default_save_path           # 默认存储路径
    )
    try:
        system(cmd)
        print('\n[+] 本地压缩 {0}.zip 成功!'.format(folders_name))
        _ = True

    except Exception as e:
        print(e)
        print('\n[-] 本地压缩 {0}.zip 失败!'.format(folders_name))

    return _

def remote_decompress_folders(connect_object:Connection, folders_path, target_decompress_path):
    '''
    server端解压文件, 并删除原压缩文件(默认解压到当前目录)
        use: eg:
            remote_decompress_folders(
                connect_object=xxx,
                folders_path='/root/myFiles/my_spider_logs.zip',
                target_decompress_path='/root/myFiles/'
            )
    :param connect_object:
    :param folders_path: 压缩文件的保存路径(绝对路径)
    :param target_decompress_path: 目标解压路径(绝对路径)
    :return:
    '''
    if not exists(folders_path):
        # raise ValueError('{0} 文件不存在!请检查!'.format(folders_path))
        pass    # 报错就先不判断处理
    elif not exists(target_decompress_path):
        raise ValueError('{0} 保存路径不存在!请检查!'.format(target_decompress_path))
    else:
        pass

    _ = False
    # 先删除原始文件夹, 再进行解压覆盖, (否则无法覆盖)
    cmd = 'cd {0} && rm -rf {1} && unzip -o -O CP936 {2} && rm {3}'.format(
        target_decompress_path,
        basename(folders_path).split('.')[0],
        folders_path,
        folders_path)
    # print(cmd)
    try:
        connect_object.run(cmd)
        print('[+] server端解压 {0} 成功!'.format(folders_path))
        _ = True
    except Exception as e:
        print(e)
        print('[-] server端解压 {0} 失败!'.format(folders_path))

    return _

def auto_git(path):
    '''
    master 自动git
    :param path: 绝对路径
    :return:
    '''
    os.system('cd {0} && git pull'.format(path))
    print('------>>>| 远程合并分支完毕!!!')
    print((path + ' 正在提交').center(100, '*'))
    os.popen('cd {0} && git add --all'.format(path))
    time.sleep(2)
    now_time = str(get_shanghai_time())
    now_time = str(re.compile(r'\..*').sub('', now_time))
    os.system('cd {0} && git commit -m "{1}"'.format(path, now_time))
    time.sleep(2)
    os.system('cd {0} && git push -u origin master'.format(path))
    print((path + ' 提交成功!!').center(100, '*') + '\n')

    return True
