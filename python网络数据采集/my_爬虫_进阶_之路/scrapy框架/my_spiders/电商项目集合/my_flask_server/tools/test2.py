# coding:utf-8

'''
@author = super_fazai
@File    : test2.py
@connect : superonesfazai@gmail.com
'''

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline
from pprint import pprint
from json import dumps
import re

sql_cli = SqlServerMyPageInfoSaveItemPipeline()

def get_db_data(sql_cli=None) -> list:
    sql_str = '''
    select top 5000 unique_id, brief_introduction
    from dbo.company_info
    where site_id=2
    and (phone = %s and email_address = %s)
    '''
    try:
        sql_cli = sql_cli if sql_cli is not None else SqlServerMyPageInfoSaveItemPipeline()
        res = sql_cli._select_table(
            sql_str=sql_str,
            params=('[]', '[]'))
    except Exception as e:
        print(e)
        return []

    return res

def re_get_phone_num_list(target_str:str) -> list:
    """
    re获取目标str中的手机号
    :return:
    """
    regex1 = '1[3|4|5|7|8][0-9]{9}'
    phone_num_list = re.compile(regex1).findall(target_str)
    phone_num_list = list(set(phone_num_list))

    return phone_num_list

def re_get_email_list(target_str:str) -> list:
    """
    re获取目标str中的email
    :param target_str:
    :return:
    """
    regex1 = '[a-zA-Z0-9_\.-]+@[a-zA-Z0-9_\.-]+\.[a-zA-Z0-9_]{2,4}'
    email_list = re.compile(regex1).findall(target_str)
    email_list = list(set(email_list))

    return email_list

def update_db_phone(unique_id:str, phone_list:list, sql_cli=None,):
    sql_str = '''
    update dbo.company_info 
    set phone=%s
    where unique_id=%s
    '''
    try:
        sql_cli = sql_cli if sql_cli is not None else SqlServerMyPageInfoSaveItemPipeline()
        sql_cli._update_table(
            sql_str=sql_str,
            params=(
                dumps(phone_list, ensure_ascii=False,),
                unique_id,
            ))
    except Exception as e:
        print(e)

db_data = get_db_data(sql_cli=sql_cli)
had_phone_count = 0
_ = []
for item in db_data:
    unique_id = item[0]
    intro = item[1]
    print('unique_id: {}, intro: {}'.format(unique_id, intro))
    phone_num_list = [{
        'phone': i,
    } for i in re_get_phone_num_list(target_str=intro)]
    email_list = [{
        'email_address': i,
    } for i in re_get_email_list(target_str=intro)]
    if phone_num_list != []\
            or email_list != []:
        had_phone_count += 1
        _.append({
            'unique_id': unique_id,
            # 'intro': intro,
            'phone_num_list': phone_num_list,
            'email_list': email_list,
        })
        # update_db_phone(unique_id=unique_id, phone_list=phone_num_list)

    # print('[{}] unique_id: {}, phone_num_list: {}'.format(
    #     '+' if phone_num_list != [] else '-',
    #     unique_id,
    #     str(phone_num_list)
    # ))

pprint(_)
print('had_phone_count: {}'.format(had_phone_count))
