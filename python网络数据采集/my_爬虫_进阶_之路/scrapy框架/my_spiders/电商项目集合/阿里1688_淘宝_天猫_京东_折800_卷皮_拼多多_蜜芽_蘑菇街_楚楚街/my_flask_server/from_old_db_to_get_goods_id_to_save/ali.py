# coding:utf-8

'''
@author = super_fazai
@File    : ali.py
@Time    : 2017/11/5 18:20
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from ali_1688_login_and_parse_idea2 import ALi1688LoginAndParse
from my_pipeline import SqlServerMyPageInfoSaveItemPipeline, OtherDb
import gc
from time import sleep
from pprint import pprint

if __name__ == '__main__':
    db = OtherDb()
    result = list(db.select_other_db_goods_url())

    pprint(result)
    # with open('ali_url.txt', 'a+') as file:


