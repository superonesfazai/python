# coding:utf-8

'''
@author = super_fazai
@File    : admin.py.py
@Time    : 2017/8/11 10:58
@connect : superonesfazai@gmail.com
'''

"""
admin相关操作func
"""

import sys
sys.path.append('..')
import json
import re

from settings import (
    key,
    INIT_PASSWD,)
from fzutils.time_utils import get_shanghai_time
from fzutils.safe_utils import (
    encrypt,
)

def find_user_name(**kwargs):
    '''
    查找
    :param kwargs:
    :return:
    '''
    find_name = kwargs.get('find_name', '')
    tmp_user = kwargs.get('tmp_user')
    my_lg = kwargs.get('my_lg')

    if len(find_name) == 11 and re.compile(r'^1').findall(find_name) != []:  # 根据手机号查找
        sql_str = 'select * from dbo.ali_spider_employee_table where username=%s'
        result = tmp_user._select_table(sql_str=sql_str, params=(find_name,))
        if result is not None and result != []:
            my_lg.info('查找成功!')
            result = result[0]
            # my_lg.info(str(result))     # 只返回的是一个list 如: ['15661611306', 'xxxx', datetime.datetime(2017, 10, 13, 10, 0), '杭州', 'xxx']
            data = [{
                'username': result[0],
                'passwd': encrypt(key, result[1]),
                'createtime': str(result[2]),  # datetime类型转换为字符串 .strftime('%Y-%m-%d %H:%M:%S')
                'department': result[3],
                'realnane': result[4],
            }]
            result = {
                'reason': 'success',
                'data': data,
                'error_code': 1,
            }
            result = json.dumps(result, ensure_ascii=False).encode()
            return result.decode()

        else:
            my_lg.info('查找失败!')
            result = {
                'reason': 'error',
                'data': [],
                'error_code': 0,  # 表示goodsLink为空值
            }
            result = json.dumps(result)
            return result

    elif len(find_name) > 1 and len(find_name) <= 4:  # 根据用户名查找
        sql_str = 'select * from dbo.ali_spider_employee_table where realnane=%s'
        result = tmp_user._select_table(sql_str=sql_str, params=(find_name,))
        # my_lg.info(str(result))
        if result is not None and result != []:
            my_lg.info('查找成功!')
            data = [{
                'username': item[0],
                'passwd': encrypt(key, item[1]),
                'createtime': str(item[2]),
                'department': item[3],
                'realnane': item[4]
            } for item in result]
            result = {
                'reason': 'success',
                'data': data,
                'error_code': 1,
            }
            result = json.dumps(result, ensure_ascii=False).encode()
            return result.decode()

        else:
            my_lg.info('查找失败!')
            result = {
                'reason': 'error',
                'data': [],
                'error_code': 0,  # 表示goodsLink为空值
            }

            result = json.dumps(result)
            return result
    else:
        my_lg.info('find_name非法!')
        result = {
            'reason': 'error',
            'data': [],
            'error_code': 0,  # 表示goodsLink为空值
        }
        result = json.dumps(result)
        return result

def init_passwd(**kwargs):
    '''
    重置用户密码
    :param kwargs:
    :return:
    '''
    tmp_user = kwargs.get('tmp_user')
    update_name = kwargs.get('update_name', '')
    my_lg = kwargs.get('my_lg')

    sql_str = 'update dbo.ali_spider_employee_table set passwd=%s where username=%s'
    result = tmp_user._update_table_2(sql_str=sql_str, params=(INIT_PASSWD, update_name), logger=my_lg)
    if result:
        my_lg.info('重置密码成功!')

    else:
        my_lg.error('重置密码失败!')

    # 返回所有数据
    return check_all_user(tmp_user=tmp_user)

def del_user(**kwargs):
    '''
    删除用户
    :param kwargs:
    :return:
    '''
    tmp_user = kwargs.get('tmp_user')
    user_to_delete_list = kwargs.get('user_to_delete_list')
    my_lg = kwargs.get('my_lg')

    sql_str = 'delete from dbo.ali_spider_employee_table where username=%s'
    for item in user_to_delete_list:
        tmp_user._delete_table(sql_str=sql_str, params=(item,))

    my_lg.info('删除操作执行成功!')

    return check_all_user(tmp_user=tmp_user)

def check_all_user(**kwargs):
    '''
    查看现有所有用户数据
    :param kwargs:
    :return:
    '''
    tmp_user = kwargs.get('tmp_user')

    sql_str = 'select * from dbo.ali_spider_employee_table'
    result = tmp_user._select_table(sql_str=sql_str) if tmp_user._select_table(sql_str=sql_str) is not None else []
    data = [{
        'username': item[0],
        'passwd': encrypt(key, item[1]),
        'createtime': str(item[2]),
        'department': item[3],
        'realnane': item[4]
    } for item in result]

    result = {
        'reason': 'success',
        'data': data,
        'error_code': 1,
    }
    result = json.dumps(result, ensure_ascii=False).encode()

    return result.decode()

def admin_add_new_user(**kwargs):
    '''
    在admin页面add new user
    :param kwargs:
    :return:
    '''
    request = kwargs.get('request')
    tmp_user = kwargs.get('tmp_user')
    my_lg = kwargs.get('my_lg')

    username = request.form.get('username', '')
    passwd = request.form.get('passwd', '')

    real_name = request.form.get('ralenane', '')
    department = request.form.get('department', '')

    create_time = get_shanghai_time()

    item = (
        str(username),
        str(passwd),
        create_time,
        str(department),
        str(real_name),
    )
    sql_str = 'insert into dbo.ali_spider_employee_table(username, passwd, createtime, department, realnane) values(%s, %s, %s, %s, %s)'
    is_insert_into = tmp_user._insert_into_table_2(sql_str=sql_str, params=item, logger=my_lg)

    if is_insert_into:
        my_lg.info('用户 %s 注册成功!' % str(username))
    else:
        my_lg.info("用户注册失败!")

    return
