# coding:utf-8

'''
@author = super_fazai
@File    : utils.py
@connect : superonesfazai@gmail.com
'''

from sql_obj import SqlServerCli
from json import dumps

def get_province_code_list_and_city_code_list() -> None:
    """
    获取province, city的code
    :return:
    """
    sql_str = """select c_name, code, parent_code from dbo.Region"""
    province_and_city_code_list = []
    print('正在获取province_and_city_code_list...')
    try:
        sql_cli = SqlServerCli()
        province_and_city_code_list = sql_cli._select_table(
            sql_str=sql_str,
            params=None)
        try:
            del sql_cli
        except:
            pass
    except Exception as e:
        print(e)

    assert province_and_city_code_list != [], 'province_and_city_code_list为空list!'
    print('获取province_and_city_code_list成功!')

    return province_and_city_code_list

def _get_db_company_unique_id_list_by_site_id(site_id: int, bloom_filter) -> tuple:
    """
    获取db中的unique id list
    :return:
    """
    print('正在获取db中的site_id:{} 的unique_id...'.format(site_id))
    sql_str = '''select unique_id from dbo.company_info where site_id=%s'''
    try:
        sql_cli = SqlServerCli()
        res = sql_cli._select_table(
            sql_str=sql_str,
            params=(site_id,),)
    except Exception as e:
        print(e)
        return [], bloom_filter

    print('unique_id获取成功!')
    print('正在组成unique_id list ...')
    oo = []
    for item in res:
        oo.append(item[0])

    for item in res:
        bloom_filter.add(item[0])

    print('组成unique_id list 成功!')

    return oo, bloom_filter

def _save_company_item(company_item,) -> bool:
    """
    存储company_item
    :param company_item:
    :return:
    """
    def _get_insert_params() -> tuple:
        nonlocal company_item

        params = [
            company_item['province_id'],
            company_item['city_id'],
            company_item['unique_id'],
            company_item['company_url'],
            company_item['company_link'],
            company_item['company_name'],
            company_item['legal_person'],
            dumps(company_item['phone'], ensure_ascii=False),
            dumps(company_item['email_address'], ensure_ascii=False),
            company_item['address'],
            company_item['brief_introduction'],
            company_item['business_range'],
            company_item['founding_time'],
            company_item['create_time'],
            company_item['site_id'],
            company_item['employees_num'],
            company_item['type_code'],
            company_item['lng'],
            company_item['lat'],
        ]

        return tuple(params)

    # 阻塞
    res = False
    sql_str = '''
    insert into dbo.company_info(province_id, city_id, unique_id, company_url, company_link, company_name, legal_person, phone, email_address, address, brief_introduction, business_range, founding_time, create_time, site_id, employees_num, type_code, lng, lat) 
    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    try:
        sql_cli = SqlServerCli()
        res = sql_cli._insert_into_table(
            sql_str=sql_str,
            params=_get_insert_params(),)
    except Exception as e:
        print(e)

    return res