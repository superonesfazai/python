# coding:utf-8

'''
@author = super_fazai
@File    : just_fuck_run.py
@Time    : 2017/11/29 13:46
@connect : superonesfazai@gmail.com
'''

import os
from time import sleep
import datetime
import re
import os
import sys

spike_file_name_list = [
    'zhe_800_spike',
    'zhe_800_miaosha_real-times_update',
    'juanpi_spike',
    'juanpi_miaosha_real-times_update',
    # 'pinduoduo_spike',
    # 'pinduoduo_miaosha_real-times_update',
]

pintuan_file_name_list = [
    'zhe_800_pintuan',
    'zhe_800_pintuan_real-times_update',
    'juanpi_pintuan',
    'juanpi_pintuan_real-times_update',
]

real_file_name_list = [
    'zhe_800_real-times_update',
    'juanpi_real-times_update',
    'tmall_real-times_update',
]

def auto_run(*params):
    print('开始执行秒杀脚本'.center(60, '*'))

    for item in spike_file_name_list:
        process_name = item + '.py'
        if process_exit(process_name) == 0:
            # 如果对应的脚本没有在运行, 则运行之
            os.system('cd {0} && python3 {1}.py'.format(params[0], item))
            sleep(2.5)      # 避免同时先后启动先sleep下
        else:
            print(process_name + '脚本已存在!')

    for item in pintuan_file_name_list:
        process_name = item + '.py'
        if process_exit(process_name) == 0:
            os.system('cd {0} && python3 {1}.py'.format(params[1], item))
            sleep(2.5)      # 避免同时先后启动先sleep下
        else:
            print(process_name + '脚本已存在!')

    for item in real_file_name_list:
        process_name = item + '.py'
        if process_exit(process_name) == 0:
            os.system('cd {0} && python3 {1}.py'.format(params[2], item))
            sleep(2.5)  # 避免同时先后启动先sleep下
        else:
            print(process_name + '脚本已存在!')

    print('脚本执行完毕'.center(60, '*'))

def process_exit(process_name):
    '''
    判断进程是否存在
    :param process_name:
    :return: 0 不存在 | >= 1 存在
    '''
    # Linux
    process_check_response = os.popen('ps aux | grep "' + process_name + '" | grep -v grep').readlines()
    return len(process_check_response)

def main_2():
    while True:
        spike_path = '~/myFiles/python/my_flask_server/spike_everything'
        pintuan_path = '~/myFiles/python/my_flask_server/pintuan_script'
        real_path = '~/myFiles/python/my_flask_server/real-times_update'

        auto_run(spike_path, pintuan_path, real_path)
        print(' Money is on the way! '.center(100, '*'))

        sleep(60*60)

def daemon_init(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    '''
    杀掉父进程，独立子进程
    :param stdin:
    :param stdout:
    :param stderr:
    :return:
    '''
    sys.stdin = open(stdin, 'r')
    sys.stdout = open(stdout, 'a+')
    sys.stderr = open(stderr, 'a+')
    try:
        pid = os.fork()
        if pid > 0:     # 父进程
            os._exit(0)
    except OSError as e:
        sys.stderr.write("first fork failed!!" + e.strerror)
        os._exit(1)

    # 子进程， 由于父进程已经退出，所以子进程变为孤儿进程，由init收养
    '''setsid使子进程成为新的会话首进程，和进程组的组长，与原来的进程组、控制终端和登录会话脱离。'''
    os.setsid()
    '''防止在类似于临时挂载的文件系统下运行，例如/mnt文件夹下，这样守护进程一旦运行，临时挂载的文件系统就无法卸载了，这里我们推荐把当前工作目录切换到根目录下'''
    os.chdir("/")
    '''设置用户创建文件的默认权限，设置的是权限“补码”，这里将文件权限掩码设为0，使得用户创建的文件具有最大的权限。否则，默认权限是从父进程继承得来的'''
    os.umask(0)

    try:
        pid = os.fork()  # 第二次进行fork,为了防止会话首进程意外获得控制终端
        if pid > 0:
            os._exit(0)  # 父进程退出
    except OSError as e:
        sys.stderr.write("second fork failed!!" + e.strerror)
        os._exit(1)

    # 孙进程
    #   for i in range(3, 64):  # 关闭所有可能打开的不需要的文件，UNP中这样处理，但是发现在python中实现不需要。
    #       os.close(i)
    sys.stdout.write("Daemon has been created! with pid: %d\n" % os.getpid())
    sys.stdout.flush()  # 由于这里我们使用的是标准IO，这里应该是行缓冲或全缓冲，因此要调用flush，从内存中刷入日志文件。

def main():
    '''
    这里的思想是将其转换为孤儿进程，然后在后台运行
    :return:
    '''
    print('========主函数开始========')  # 在调用daemon_init函数前是可以使用print到标准输出的，调用之后就要用把提示信息通过stdout发送到日志系统中了
    daemon_init()  # 调用之后，你的程序已经成为了一个守护进程，可以执行自己的程序入口了
    print('--->>>| 孤儿进程成功被init回收成为单独进程!')
    # time.sleep(10)  # daemon化自己的程序之后，sleep 10秒，模拟阻塞
    main_2()

if __name__ == '__main__':
    main()