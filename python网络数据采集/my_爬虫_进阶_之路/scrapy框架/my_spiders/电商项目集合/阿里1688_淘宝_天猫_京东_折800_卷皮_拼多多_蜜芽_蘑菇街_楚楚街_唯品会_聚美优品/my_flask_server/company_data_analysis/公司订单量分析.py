# coding:utf-8

'''
@author = super_fazai
@File    : 公司订单量分析.py
@Time    : 2018/3/17 13:22
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from my_pipeline import DataAnalysisDbPipeline
import pandas
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

tmp_pipeline = DataAnalysisDbPipeline()

def s_100(a):
    return a*100

def everyday_order_sell_count(year, month, day):
    if tmp_pipeline.is_connect_success is True:
        result = tmp_pipeline.select_everyday_order_sell_count(year, month, day)
        print(result)
    else:
        pass

def one_month_everyday_order_sell_count(year, month):
    if tmp_pipeline.is_connect_success is True:
        result = tmp_pipeline.select_every_month_order_sell_count(year, month)
        # print(result)

        return result
    else:
        pass

def one_year_order_sell_count(year):
    if tmp_pipeline.is_connect_success is True:
        result = tmp_pipeline.select_one_year_every_month_order_sell_count(year)

        return result
    else:
        pass

def plot_one_month_everydaya_sell_count(year, month):
    '''
    绘制某月每天的订单
    :param year:
    :param month:
    :return:
    '''
    result = one_month_everyday_order_sell_count(year, month)

    # 设置x轴值区间
    plt.xlim(1, result[-1][0])

    # 切记x, y的shape长度是一样的
    x = [item[0] for item in result]
    plt.xticks([1 + 1 * i for i in x], [1 + 1 * i for i in x])
    y = [item[1] for item in result]

    # 加载字体
    font = FontProperties(fname='/Library/Fonts/Songti.ttc', size=15)

    # 显示标题
    plt.title('浙江甄优智能科技有限公司-{0}年{1}月所有订单折线图'.format(year, month), fontproperties=font, fontsize=18)
    plt.ylabel('订单数', fontproperties=font)
    plt.xlabel('日', fontproperties=font)

    # 显示网格
    plt.grid()

    # 调用绘制线性图函数plot()
    plt.plot(x, y, marker='o', markerfacecolor='r', markersize=5)

    # 显示图例
    plt.legend(['单位:个'], loc=1, prop=font)

    # 标识数字标签
    for a, b in zip(x, y):
        plt.text(a, b, '%d' % (b,), fontsize=10)

    # 调用show方法显式
    plt.show()

def plot_every_month_everyday_sell_count_in_one_table(year):
    '''
    每月的订单量在同一张表中
    :param year:
    :return:
    '''
    # 加载字体
    font = FontProperties(fname='/Library/Fonts/Songti.ttc', size=10)

    # 显示标题
    plt.title('浙江甄优智能科技有限公司-{0}年12个月每天订单折线图'.format(year,), fontproperties=font, fontsize=18)
    plt.ylabel('订单数', fontproperties=font)
    plt.xlabel('日', fontproperties=font)

    # 显示网格
    plt.grid()
    for month in range(1, 13):
        result = one_month_everyday_order_sell_count(year, month)

        # 设置x轴值区间
        plt.xlim(1, result[-1][0])

        # 切记x, y的shape长度是一样的
        x = [item[0] for item in result]
        # plt.xticks([1 + 1 * i for i in x], [1 + 1 * i for i in x])
        plt.xticks(np.linspace(1, 31, 31))
        y = [item[1] for item in result]
        new_yticks = np.linspace(0, 110000, 300)      # 范围是(,2);个数是5.
        plt.yticks(new_yticks)


        # 调用绘制线性图函数plot()
        plt.plot(x, y, marker='o', markerfacecolor='r', markersize=5, label=month.__str__() + '月份')
        # 显示图例
        plt.legend(loc=1, fontsize=10, prop=font)       # 切记: 显示图例在每次绘制完图形都要设置一次

        # 标识数字标签
        # for a, b in zip(x, y):
        #     plt.text(a, b, '%d' % (b,), fontsize=10)

    # 调用show方法显式
    plt.show()

def plot_one_year_every_month_sell_count(year):
    '''
    绘制某年所有月份的订单
    :param year:
    :return:
    '''
    result = one_year_order_sell_count(year)

    # 设置x轴值区间
    plt.xlim(1, result[-1][0]-1)

    # 切记x, y的shape长度是一样的
    x = [item[0] for item in result]
    plt.xticks([1 + 1 * i for i in x], [1 + 1 * i for i in x])
    y = [item[1] for item in result]

    # 加载字体
    font = FontProperties(fname='/Library/Fonts/Songti.ttc', size=15)

    # 显示标题
    plt.title('浙江甄优智能科技有限公司-{0}年所有订单折线图'.format(year,), fontproperties=font, fontsize=18)
    plt.ylabel('订单数', fontproperties=font)
    plt.xlabel('月', fontproperties=font)

    # 显示网格
    plt.grid()

    # 调用绘制线性图函数plot()
    plt.plot(x, y, marker='o', markerfacecolor='r', markersize=5)

    # 显示图例
    plt.legend(['单位:个'], loc=1, prop=font)

    # 标识数字标签
    for a, b in zip(x, y):
        plt.text(a, b, '%d' % (b,), fontsize=10)

    # 调用show方法显式
    plt.show()

# plot_one_month_everydaya_sell_count(2017, 10)
plot_one_year_every_month_sell_count(2016)
# plot_every_month_everyday_sell_count_in_one_table(2017)