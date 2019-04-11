# coding:utf-8

'''
@author = super_fazai
@File    : server.py
@connect : superonesfazai@gmail.com
'''

"""
server端: 提供多种本地服务
"""

from flask import (
    Flask,
    send_file,
    request,)
from os import getcwd

from settings import (
    SERVER_PORT,
)

from pprint import pprint

try:
    from gevent.wsgi import WSGIServer      # 高并发部署
except Exception as e:
    from gevent.pywsgi import WSGIServer

from fzutils.common_utils import json_2_dict

app = Flask(__name__, root_path=getcwd())
# 存储tb user_id
tb_shop_id_list = []
tb_shop_info_list = []

@app.route('/', methods=['GET', 'POST'])
def home():
    return '欢迎来到 fzhook_server 主页!'

@app.route('/dy', methods=['GET', 'POST'])
def dy():
    """
    获取dy 无水印视频
    :return:
    """
    return send_file('templates/douyin.php')

@app.route('/tb_shop_info', methods=['POST'])
def tb_shop_info():
    global tb_shop_info_list, tb_shop_id_list
    # print(str(request.args))
    # print(str(request.form))
    # post 请求
    # print(str(request.get_data()))

    try:
        shop_info = json_2_dict(
            json_str=request.get_data().decode(),
            default_res={})
        # pprint(shop_info)
        # print(shop_info)
        user_id = shop_info.get('globalData', {}).get('userId', '')
        assert user_id != '', 'user_id不为null'
        shop_name = shop_info.get('globalData', {}).get('userNick', '')
        assert shop_name != '', 'shop_name不为null'
        shop_id = shop_info.get('globalData', {}).get('shopId', '')
        assert shop_id != '', 'shop_id不为null'
        site_id = shop_info.get('globalData', {}).get('siteId', '')
        assert site_id != '', 'site_id不为null'
    except Exception as e:
        print(e)
        return 'tb_shop_info_page!!'

    if user_id not in tb_shop_id_list:
        print('新增: user_id: {}, shop_name: {}, shop_id: {}'.format(user_id, shop_name, shop_id))
        tb_shop_id_list.append(user_id)
        tb_shop_info_list.append({
            'user_id': user_id,
            'shop_name': shop_name,
            'shop_id': shop_id,
            'site_id': site_id,
        })

    tb_shop_id_list = list(set(tb_shop_id_list))

    return 'tb_shop_info_page!!'

def main():
    print('server 已启动...\nhttp://0.0.0.0:{}\n'.format(SERVER_PORT))
    WSGIServer(listener=('0.0.0.0', SERVER_PORT), application=app).serve_forever()  # 采用高并发部署

if __name__ == '__main__':
    main()
