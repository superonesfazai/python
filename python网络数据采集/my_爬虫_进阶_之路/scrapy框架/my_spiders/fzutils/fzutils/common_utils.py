# coding:utf-8

'''
@author = super_fazai
@File    : common_utils.py
@Time    : 2018/7/13 18:19
@connect : superonesfazai@gmail.com
'''

__all__ = [
    'json_2_dict',                                              # json转dict
    '_green',                                                   # 将字体变成绿色
    'delete_list_null_str',                                     # 删除list中的空str
    'list_duplicate_remove',                                    # list去重

    # json_str转dict时报错处理方案
    'deal_with_JSONDecodeError_about_value_invalid_escape',     # 错误如: ValueError: Invalid \escape: line 1 column 35442 (char 35441)

    '_print',                                                   # fz的输出方式(常规print or logger打印)
]

def json_2_dict(json_str, logger=None, encoding=None):
    '''
    json字符串转dict
    :param json_str:
    :param logger:
    :param encoding: 解码格式
    :return:
    '''
    from json import (
        loads,
        JSONDecodeError,)
    from demjson import decode

    _ = {}
    try:
        _ = loads(json_str)
    except JSONDecodeError:
        # 上方解码失败! 采用demjson二次解码
        try:
            _ = decode(json_str, encoding=encoding)
        except Exception as e:
            _print(msg='遇到json解码错误!', logger=logger, log_level=2, exception=e)

    return _

def _green(string):
    '''
    将字体转变为绿色
    :param string:
    :return:
    '''
    return '\033[32m{}\033[0m'.format(string)

def delete_list_null_str(_list):
    '''
    删除list中的所有空str
    :param _list:
    :return:
    '''
    while '' in _list:
        _list.remove('')

    return _list

def list_duplicate_remove(_list:list):
    '''
    list去重
    :param _list:
    :return:
    '''
    b = []
    [b.append(i) for i in _list if not i in b]

    return b

def deal_with_JSONDecodeError_about_value_invalid_escape(json_str):
    '''
    ValueError: Invalid \escape: line 1 column 35442 (char 35441)
    问题在于编码中是\xa0之类的，当遇到有些 不用转义的\http之类的，则会出现以上错误。
    :param json_str:
    :return: 正常的str类型的json字符串
    '''
    import re

    return re.compile(r'\\(?![/u"])').sub(r"\\\\", json_str)

def _print(**kwargs):
    '''
    fz的输出方式(常规print or logger打印)
        可传特殊形式:
            eg: _print(exception=e, logger=logger)  # logger可以为None
    :param kwargs:
    :return: None
    '''
    msg = kwargs.get('msg', None)
    logger = kwargs.get('logger', None)
    log_level = kwargs.get('log_level', 1)     # 日志等级(默认'info')
    exception = kwargs.get('exception', None)

    if not logger:
        if not exception:
            print(msg)
        else:
            if not msg:
                print(msg, exception)
            else:
                print(exception)
    else:
        if not msg:
            if isinstance(msg, str):
                if isinstance(log_level, int):
                    if log_level == 1:
                        logger.info(msg)
                    elif log_level == 2:
                        logger.error(msg)
                    else:
                        raise ValueError('log_level没有定义该打印等级!')
                else:
                    raise TypeError('log_level类型错误!')
            else:
                raise TypeError('log模式打印时, msg必须是str!')

        if not exception:
            if isinstance(exception, Exception):
                logger.exception(exception)
            else:
                raise TypeError('exception必须是Exception类型!')

    return True
