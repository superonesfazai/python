# coding:utf-8

'''
@author = super_fazai
@File    : server.py
@connect : superonesfazai@gmail.com
'''

"""
server端

use: 
    python3 server.py --wsgi-disable-file-wrapper

(为避免)
1. In python3, uwsgi fails to respond a stream from BytesIO object.
解释: uWSGI中的wsgi.file_wrapper是使用sendfile（）或offloading的真正优化。BytesIO不基于文件描述符，因此无法进行优化。最好的（或唯一的）解决方案是禁用wsgi.file_wrapper：

2. OSError: [Errno 24] Too many open files <WSGIServer at 0x10e17d438 fileno=7 address=0.0.0.0:8001> failed with OSError
解释: 出现这句提示的原因是程序打开的文件/socket连接数量超过系统设定值。
查看每个用户最大允许打开文件数量
$ ulimit -a
# 修改最大可打开文件数(2048工作良好)(非永久)
$ ulimit -n 2048
[stack overflow: mac]: https://stackoverflow.com/questions/34821014/python-oserror-errno-24-too-many-open-files
"""

from flask import (
    Flask,)
from os import getcwd

from settings import (
    SERVER_PORT,
)

from json import dumps
from pprint import pprint
from fzutils.sql_utils import BaseSqlite3Cli

try:
    from gevent.wsgi import WSGIServer      # 高并发部署
except Exception as e:
    from gevent.pywsgi import WSGIServer

app = Flask(__name__, root_path=getcwd())
sqlite3_cli = BaseSqlite3Cli(db_path='proxy.db')
select_sql_str = 'select * from proxy_obj_table'

@app.route('/', methods=['GET', 'POST'])
def home():
    return '欢迎来到 proxy checker 主页!'

@app.route('/get_all', methods=['GET', 'POST'])
def get_proxy_list():
    '''
    获取代理的接口
    :return:
    '''
    res = []
    all = get_db_old_data()
    for item in all:
        ip = item[1]
        port = item[2]
        check_time = item[5]
        res.append({
            'ip': ip,
            'port': port,
            'check_time': check_time,
        })

    return dumps(res)

def get_db_old_data() -> list:
    '''
    获取db数据
    :return:
    '''
    try:    # 先不处理高并发死锁问题
        cursor = sqlite3_cli._execute(sql_str=select_sql_str)
        all = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print(e)
        return []

    return all

def main():
    print('server 已启动...\nhttp://0.0.0.0:{}\n'.format(SERVER_PORT))
    WSGIServer(listener=('0.0.0.0', SERVER_PORT), application=app).serve_forever()  # 采用高并发部署

if __name__ == '__main__':
    main()





