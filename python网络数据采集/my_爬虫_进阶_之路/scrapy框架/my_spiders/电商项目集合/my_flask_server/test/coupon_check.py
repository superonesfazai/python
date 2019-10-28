# coding:utf-8

'''
@author = super_fazai
@File    : coupon_check.py
@connect : superonesfazai@gmail.com
'''

from sys import path as sys_path
sys_path.append('..')

from multiplex_code import CP_PROFIT

# 原始最低价
ori_tb_price: float = 29.9
# 优惠券面值
coupon_value: float = 5
# 使用门槛
threshold: float = 14
# 使用优惠券后的价格
preferential_price = ((ori_tb_price - coupon_value if ori_tb_price >= threshold else ori_tb_price) * (1 + CP_PROFIT)).__round__(2)
print('preferential_price: {}'.format(preferential_price))