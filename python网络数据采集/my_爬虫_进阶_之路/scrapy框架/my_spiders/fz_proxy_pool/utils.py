# coding:utf-8

'''
@author = super_fazai
@File    : utils.py
@connect : superonesfazai@gmail.com
'''

from fzutils.sql_utils import BaseRedisCli
from fzutils.data.pickle_utils import deserializate_pickle_object
from pprint import pprint
from pickle import dumps

# _ = BaseRedisCli()
# pprint(deserializate_pickle_object(_.get('6e554b57-d773-3d32-8702-4000a31ffc27') or dumps([])))