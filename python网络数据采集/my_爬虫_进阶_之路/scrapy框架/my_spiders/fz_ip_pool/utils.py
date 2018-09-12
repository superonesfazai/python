# coding:utf-8

'''
@author = super_fazai
@File    : utils.py
@connect : superonesfazai@gmail.com
'''

from fzutils.sql_utils import BaseRedisCli
from fzutils.safe_utils import get_uuid3
from fzutils.data.pickle_utils import deserializate_pickle_object
from fzutils.linux_utils import kill_process_by_name
from fzutils.time_utils import get_shanghai_time
from fzutils.common_utils import get_random_int_number
from fzutils.common_utils import retry
from pprint import pprint
from pickle import dumps
from time import sleep
from random import choice
from settings import high_proxy_list_key_name

print(get_uuid3('proxy_tasks'))
print(get_uuid3(high_proxy_list_key_name))
# _ = BaseRedisCli()
# pprint(deserializate_pickle_object(_.get('5e421d78-a394-3b44-aae1-fd86aa127255') or dumps([])))

# 清除celery workers
# kill_process_by_name(process_name='celery')
