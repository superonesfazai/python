# coding:utf-8

'''
@author = super_fazai
@File    : sniff_utils.py
@connect : superonesfazai@gmail.com
'''

"""
嗅探 utils
"""

from scapy.all import (
    linehexdump,
)

__all__ = [
    'get_hex_res_of_pkt',           # scapy中得到数据包的16进制结果
]

def get_hex_res_of_pkt(pkt) -> (str, None):
    '''
    scapy中得到数据包的16进制结果
    :param pkt: 数据包
    :return: None 表示失败
    '''
    pkt_load = pkt.load
    line_hex = linehexdump(pkt_load, dump=True)
    try:
        hex_16_pkt_load = line_hex.split(' ')[0] if line_hex is not None else None
    except IndexError:
        return None

    return hex_16_pkt_load