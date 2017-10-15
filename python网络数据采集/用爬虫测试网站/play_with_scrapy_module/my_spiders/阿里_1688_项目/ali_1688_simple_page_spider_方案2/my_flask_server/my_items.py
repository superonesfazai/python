# coding:utf-8

'''
@author = super_fazai
@File    : my_items.py
@Time    : 2017/10/11 13:47
@connect : superonesfazai@gmail.com
'''

class PageInfoItem(object):
    def __init__(self):
        # 商品标题
        title = ''
        # 商品价格
        price = []
        # 商品起批量
        trade_number = []

        # 颜色
        color = []
        # 颜色的图片url(需要一一对应)
        color_img_url = []

        # 适合尺寸
        size_info = []

        # 对应颜色或者尺寸的价格(需要一一对应)
        detail_price = []

        # 对应颜色或者尺寸的库存量(需要一一对应)
        rest_number = []

        # 主显示的图片url
        center_img_url = []

        # 所有图片url
        all_img_url = []