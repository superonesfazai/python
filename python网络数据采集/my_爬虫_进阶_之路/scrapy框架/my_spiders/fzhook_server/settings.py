# coding:utf-8

'''
@author = super_fazai
@File    : settings.py
@connect : superonesfazai@gmail.com
'''

from json import loads

SERVER_PORT = 9001

"""
db_info_json_path
"""
# 自己电脑上
db_info_json_path = '/Users/afa/my_company_db_info.json'
# linux服务器
# db_info_json_path = '/root/my_company_db_info.json'

def get_db_info():
    try:
        with open(db_info_json_path, 'r') as f:
            _tmp = loads(f.readline())
    except FileNotFoundError:
        print('严重错误, 数据库初始配置json文件未找到!请检查!')
        return ('', '', '', '', 1433)
    except Exception as e:
        print('错误如下: ', e)
        return ('', '', '', '', 1433)

    return (_tmp['HOST'], _tmp['USER'], _tmp['PASSWORD'], _tmp['DATABASE'], _tmp['PORT'])

"""
数据库相关
"""
HOST, USER, PASSWORD, DATABASE, PORT = get_db_info()