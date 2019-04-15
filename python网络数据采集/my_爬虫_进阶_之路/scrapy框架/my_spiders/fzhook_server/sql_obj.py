# coding:utf-8

'''
@author = super_fazai
@File    : sql_obj.py
@connect : superonesfazai@gmail.com
'''

from settings import (
    HOST,
    USER,
    PASSWORD,
    DATABASE,
    PORT,
)
from fzutils.sql_utils import BaseSqlServer

class SqlServerCli(BaseSqlServer):
    """
    页面存储管道
    """
    def __init__(self, host=HOST, user=USER, passwd=PASSWORD, db=DATABASE, port=PORT):
        super(SqlServerCli, self).__init__(
            host=host,
            user=user,
            passwd=passwd,
            db=db,
            port=port)

