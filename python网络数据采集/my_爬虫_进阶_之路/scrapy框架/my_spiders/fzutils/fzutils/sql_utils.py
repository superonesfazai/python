# coding:utf-8

'''
@author = super_fazai
@File    : sql_utils.py
@Time    : 2017/7/14 14:36
@connect : superonesfazai@gmail.com
'''

"""
sql utils
"""

from pymssql import *
import gc
import asyncio

__all__ = [
    'BaseSqlServer',        # sql_utils for sql_server
]

class BaseSqlServer(object):
    """
    sql_utils for sql_server
    """
    def __init__(self, host, user, passwd, db, port):
        super(BaseSqlServer, self).__init__()
        self.is_connect_success = True
        try:
            self.conn = connect(
                host=host,
                user=user,
                password=passwd,
                database=db,
                port=port,
                charset='utf8'
            )
        except Exception:
            print('数据库连接失败!!')
            self.is_connect_success = False

    def _select_table(self, sql_str, params=None, lock_timeout=20000):
        '''
        搜索
        :param sql_str:
        :param params:
        :param lock_timeout:
        :return:
        '''
        result = None
        try:
            cs = self.conn.cursor()
        except AttributeError as e:
            print(e.args[0])
            return result

        try:
            cs.execute('set lock_timeout {0};'.format(lock_timeout))  # 设置客户端执行超时等待为20秒
            if params is not None:
                if not isinstance(params, tuple):
                    params = tuple(params)
                cs.execute(sql_str, params)
            else:
                cs.execute(sql_str)
            # self.conn.commit()

            result = cs.fetchall()
        except Exception as e:
            print('--------------------| 筛选level时报错：', e)
        finally:
            try:
                cs.close()
            except Exception:
                pass
            return result

    def _insert_into_table(self, sql_str, params: tuple):
        '''
        插入表数据
        :param sql_str:
        :param params:
        :return:
        '''
        cs = self.conn.cursor()
        _ = False
        try:
            cs.execute(sql_str.encode('utf-8'), params)  # 注意必须是tuple类型
            self.conn.commit()
            print('-' * 9 + '| ***该页面信息成功存入sqlserver中*** ')
            _ = True
        except Exception as e:
            print('-' * 9 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('-' * 9 + '| 错误如下: ', e)
            print('-' * 9 + '| 报错的原因：可能是重复插入导致, 可以忽略 ... |')
        finally:
            try:
                cs.close()
            except Exception:
                pass
            return _

    def _insert_into_table_2(self, sql_str, params: tuple, logger):
        cs = self.conn.cursor()
        _ = False
        try:
            # logger.info(str(params))
            cs.execute(sql_str.encode('utf-8'), params)  # 注意必须是tuple类型
            self.conn.commit()
            logger.info('-' * 9 + '| ***该页面信息成功存入sqlserver中*** ')
            _ = True
        except IntegrityError:
            logger.info('重复插入goods_id[%s], 此处跳过!' % params[0])

        except Exception:
            logger.error('| 修改信息失败, 未能将该页面信息存入到sqlserver中 | 出错goods_id: %s' % params[0], exc_info=True)
        finally:
            try:
                cs.close()
            except Exception:
                pass
            return _

    async def _insert_into_table_3(self, sql_str, params: tuple, logger, error_msg_dict=None):
        '''
        异步
            error_msg_dict参数:
                eg: {
                    # 重复插入
                    'repeat_error': {
                        'field_name': '重复插入要记录的字段名',
                        'field_value': '重复记录该字段的值',
                    },
                    # 其他异常
                    'other_error': [{
                        'field_name': '字段名',
                        'field_value': '字段值',
                    }, ...]
                }
        :param sql_str:
        :param params:
        :param logger:
        :param error_msg_dict: logger记录的额外信息
        :return:
        '''
        cs = self.conn.cursor()
        _ = False
        try:
            # logger.info(str(params))
            cs.execute(sql_str.encode('utf-8'), params)  # 注意必须是tuple类型
            self.conn.commit()
            logger.info('-' * 9 + '| ***该页面信息成功存入sqlserver中*** ')
            _ = True
        except IntegrityError:
            if not error_msg_dict:
                logger.info('重复插入goods_id[%s], 此处跳过!' % params[0])
            else:
                if isinstance(error_msg_dict, dict):
                    msg = '重复插入{0}[{1}], 此处跳过!'.format(
                        error_msg_dict.get('repeat_error', {}).get('field_name', ''),
                        error_msg_dict.get('repeat_error', {}).get('field_value', '')
                    )
                    logger.info(msg)
                else:
                    raise TypeError('传入的error_msg_dict类型错误, 请核对需求参数!')

        except Exception:
            if not error_msg_dict:
                logger.error('| 修改信息失败, 未能将该页面信息存入到sqlserver中 | 出错goods_id: {0}'.format(params[0]), exc_info=True)
            else:
                if isinstance(error_msg_dict, dict):
                    msg = '| 修改信息失败, 未能将该页面信息存入到sqlserver中 | '
                    for item in error_msg_dict.get('other_error', []):
                        msg += '出错{0}: {1} '.format(
                            item.get('field_name', ''),
                            item.get('field_value', '')
                        )
                    logger.error(msg, exc_info=True)
                else:
                    raise TypeError('传入的error_msg_dict类型错误, 请核对需求参数!')

        finally:
            try:
                cs.close()
            except Exception:
                pass
            return _

    def _update_table(self, sql_str, params: tuple):
        '''
        更新表数据
        :param sql_str:
        :param params:
        :return: bool
        '''
        cs = self.conn.cursor()
        _ = False
        try:
            cs.execute(sql_str, params)

            self.conn.commit()
            print('-' * 9 + '| ***该页面信息成功存入sqlserver中*** ')
            _ = True
        except Exception as e:
            print('-' * 9 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            print('--------------------| 错误如下: ', e)
        finally:
            try:
                cs.close()
            except Exception:
                pass

            return _

    def _update_table_2(self, sql_str, params: tuple, logger):
        cs = self.conn.cursor()
        _ = False
        try:
            cs.execute(sql_str, params)

            self.conn.commit()
            cs.close()
            logger.info('-' * 9 + '| ***该页面信息成功存入sqlserver中*** ')
            _ = True
        except Exception as e:
            logger.error('| 修改信息失败, 未能将该页面信息存入到sqlserver中 出错goods_id: %s|' % params[-1])
            logger.exception(e)

        finally:
            try:
                cs.close()
            except Exception:
                pass
            return _

    async def _update_table_3(self, sql_str, params: tuple, logger, error_msg_dict=None):
        '''
        异步更新数据
            error_msg_dict参数:
                eg: {
                    # 其他异常
                    'other_error': [{
                        'field_name': '字段名',
                        'field_value': '字段值',
                    }, ...]
                }
        :param sql_str:
        :param params:
        :param logger:
        :param error_msg_dict: logger记录的额外信息
        :return:
        '''
        cs = self.conn.cursor()
        _ = False
        try:
            cs.execute(sql_str, params)

            self.conn.commit()
            logger.info('-' * 9 + '| ***该页面信息成功存入sqlserver中*** ')
            _ = True
        except Exception:
            if not error_msg_dict:
                logger.error('-' * 9 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 | 出错goods_id: {0}'.format(params[-1]),
                     exc_info=True)
            else:
                if isinstance(error_msg_dict, dict):
                    msg = '-' * 9 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 | '
                    for item in error_msg_dict.get('other_error', []):
                        msg += '出错{0}: {1} '.format(
                            item.get('field_name', ''),
                            item.get('field_value', '')
                        )
                    logger.error(msg, exc_info=True)

                else:
                    raise TypeError('传入的error_msg_dict类型错误, 请核对需求参数!')
        finally:
            try:
                cs.close()
            except Exception:
                pass

            return _

    def _delete_table(self, sql_str, params=None, lock_timeout=20000):
        cs = self.conn.cursor()
        _ = False
        try:
            cs.execute('set lock_timeout {0};'.format(lock_timeout))  # 设置客户端执行超时等待为20秒
            if params is not None:
                if not isinstance(params, tuple):
                    params = tuple(params)
                cs.execute(sql_str, params)
            else:
                cs.execute(sql_str)
            self.conn.commit()
            # print('success')

            _ = True
        except Exception as e:
            print('删除时报错: ', e)
        finally:
            try:
                cs.close()
            except Exception:
                pass
            return _

    def __del__(self):
        try:
            self.conn.close()
        except Exception:
            pass
        gc.collect()

