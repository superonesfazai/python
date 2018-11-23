# coding:utf-8

'''
@author = super_fazai
@File    : server.py
@connect : superonesfazai@gmail.com
'''

"""
server端
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
    global db_search_count, db_proxy_list

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
    except Exception:
        print(e)
        return []

    return all

def main():
    print('server 已启动...\nhttp://0.0.0.0:{}\n'.format(SERVER_PORT))
    WSGIServer(listener=('0.0.0.0', SERVER_PORT), application=app).serve_forever()  # 采用高并发部署

if __name__ == '__main__':
    main()





