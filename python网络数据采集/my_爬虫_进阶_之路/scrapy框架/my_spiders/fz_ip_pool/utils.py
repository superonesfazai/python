# coding:utf-8

'''
@author = super_fazai
@File    : utils.py
@connect : superonesfazai@gmail.com
'''

from fzutils.sql_utils import BaseRedisCli
from fzutils.safe_utils import get_uuid3
from fzutils.data.pickle_utils import deserializate_pickle_object
from pprint import pprint
from pickle import dumps

# print(get_uuid3('proxy_tasks'))
# _ = BaseRedisCli()
# pprint(deserializate_pickle_object(_.get('5e421d78-a394-3b44-aae1-fd86aa127255') or dumps([])))