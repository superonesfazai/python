# coding:utf-8

'''
@author = super_fazai
@File    : get_wx_phone.py
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from my_pipeline import SqlServerMyPageInfoSaveItemPipeline

from fzutils.spider.async_always import *

def get_phone_from_db():
    sql_cli = SqlServerMyPageInfoSaveItemPipeline()
    sql_str = '''
    select top 10000 phone
    from dbo.company_info
    where phone != '[]'
    '''
    res = sql_cli._select_table(
        sql_str=sql_str,)
    # pprint(res)

    data = []
    for item in res:
        phone_list = json_2_dict(
            json_str=item[0],
            default_res=[],)
        for i in phone_list:
            if i != {}:
                try:
                    phone = int(i.get('phone', ''))
                    # print(phone)
                    assert str(phone)[0] == '1'
                    assert len(str(phone)) == 11
                    data.append({
                        'phone': int(phone),
                    })
                except:
                    pass
            else:
                continue

    pprint(data)
    print(len(data))

    try:
        del sql_cli
    except:
        pass

get_phone_from_db()