# coding:utf-8

'''
@author = super_fazai
@File    : my_exceptions.py
@connect : superonesfazai@gmail.com
'''

class GoodsShelvesException(Exception):
    """商品下架异常"""
    pass

class MiaSkusIsNullListException(Exception):
    """蜜芽skus参数为空list"""
    pass

class SqlServerConnectionException(Exception):
    """sql server连接异常!"""
    pass

class NoNextPageException(Exception):
    """没有后续页面的异常"""
    pass

class DBGetGoodsSkuInfoErrorException(Exception):
    """db中获取某个goods_id的sku_info失败的异常!"""
    pass

class ProvinceIdNotFindException(Exception):
    """db中province_id未找到的异常"""
    pass

class CityIdNotFindException(Exception):
    """db中city_id未找到的异常"""
    pass

class ArticleTitleOverLongException(Exception):
    """文章标题过长异常"""
    pass

class LoginFailException(Exception):
    """登录失败异常"""
    pass

class ArticleTitleContainSensitiveWordsException(Exception):
    """文章标题包含敏感词异常"""
    pass

class PublishOneArticleFailException(Exception):
    """发布单篇文章失败异常"""
    pass

class EnterTargetPageFailException(Exception):
    """driver: 进入目标页失败异常"""
    pass