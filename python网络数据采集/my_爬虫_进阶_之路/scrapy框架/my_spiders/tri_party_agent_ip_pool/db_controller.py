# coding:utf-8

'''
@author = super_fazai
@File    : db_controller.py
@connect : superonesfazai@gmail.com
'''

"""
sqlite3 
"""

from pprint import pprint
from fzutils.sql_utils import BaseSqlite3Cli

def create_proxy_obj_table() -> bool:
    '''
    if not exist 则 create proxy_obj_table
    :return:
    '''
    res = False
    sqlite_cli = BaseSqlite3Cli(db_path='proxy.db')
    sql_str_1 = 'select name from sqlite_master where type=? and name=? order by name'
    cursor = sqlite_cli._execute(sql_str=sql_str_1, params=('table', 'proxy_obj_table'))
    _ = cursor.fetchall()
    cursor.close()
    # print(_)

    if _ != []:
        print('proxy_obj_table表已存在!')
    else:
        print('创建proxy_obj_table...')
        sql_str = '''
        create table proxy_obj_table (
            id integer primary key autoincrement,
            ip varchar (100) not null unique, 
            port int not null,
            score int not null,
            agency_agreement varchar (20) not null,
            check_time datetime not null
        );
        '''
        cursor = sqlite_cli._execute(sql_str=sql_str)
        cursor.close()

        cursor = sqlite_cli._execute(sql_str=sql_str_1, params=('table', 'proxy_obj_table'))
        _ = cursor.fetchall()
        cursor.close()
        # print(_)

    if _ != []:
        res = True

    return res

def look_up_db_all_proxy_data() -> list:
    '''
    查看db中所有proxy
    :return:
    '''
    sqlite_cli = BaseSqlite3Cli(db_path='proxy.db')
    sql_str = 'select * from proxy_obj_table'
    cursor = sqlite_cli._execute(sql_str=sql_str)
    all = cursor.fetchall()
    cursor.close()

    return all

def empty_db_proxy_data() -> None:
    '''
    清空db原有proxy数据
    :return:
    '''
    sqlite_cli = BaseSqlite3Cli(db_path='proxy.db')
    sql_str = 'delete from proxy_obj_table'
    cursor = sqlite_cli._execute(sql_str=sql_str)
    row_count = cursor.rowcount
    cursor.close()
    print('已影响行数: {}'.format(row_count))

    return None

# create_proxy_obj_table()
# empty_db_proxy_data()
# all = look_up_db_all_proxy_data()
# pprint(all)


