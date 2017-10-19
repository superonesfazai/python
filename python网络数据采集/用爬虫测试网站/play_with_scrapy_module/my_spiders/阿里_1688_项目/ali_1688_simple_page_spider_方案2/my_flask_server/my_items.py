# coding:utf-8

'''
@author = super_fazai
@File    : my_items.py
@Time    : 2017/10/11 13:47
@connect : superonesfazai@gmail.com
'''

class MyPageInfoSaveItem(object):
    def __init__(self):
        # 需要抓取的url
        self.spider_url = ''
        # 操作人员的username
        self.username = ''
        # 操作的时间
        self.deal_with_time = ''

        """
        商品信息
        """
        # 商品标题
        self.title = ''
        # 商品价格
        self.price = []
        # 商品起批量
        self.trade_number = []

        # 颜色
        self.color = []
        # 颜色的图片url(需要一一对应)
        self.color_img_url = []

        # 适合尺寸
        self.size_info = []

        # 对应颜色或者尺寸的价格(需要一一对应)
        self.detail_price = []

        # 对应颜色或者尺寸的库存量(需要一一对应)
        self.rest_number = []

        # 主显示的图片url
        self.center_img_url = []

        # 所有图片url
        self.all_img_url = []