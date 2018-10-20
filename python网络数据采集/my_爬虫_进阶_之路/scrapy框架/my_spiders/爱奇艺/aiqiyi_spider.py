# coding:utf-8

'''
@author = super_fazai
@File    : aiqiyi_spider.py
@connect : superonesfazai@gmail.com
'''

"""
爱奇艺m站爬虫
"""

# 1. 视频地址在cache.m.iqiyi.com这个接口里
# jp/tmts
# function E(...){}
# getTmtsVf: E,
# 找到getTmtsVf 查看其传入哪些参数

# 2. 或者直接解析m站的视频块div得到其播放地址

# 下面是示例
import requests

cookies = {
    'QC005': '2d3f9a2fcda22663a554809ec477e3e2',
    'QP001': '1',
    'QC006': '71b8d0b639cf6ab325d363c070373d77',
    'QC173': '0',
    'T00404': '1e903292cc0184ec7b201d334cd545fb',
    'QC118': '%7B%22color%22%3A%22FFFFFF%22%2C%22channelConfig%22%3A0%7D',
    'P00004': '1909962238.1533622161.26a1673568',
    'QP0010': '1',
    'QP007': '7980',
    'Hm_lvt_53b7374a63c37483e5dd97d78d9bb36e': '1540020692',
    'QC008': '1533622154.1533622154.1540020691.2',
    'nu': '0',
    'Hm_lvt_5df871ab99f94347b23ca224fc7d013f': '1540020773',
    'Hm_lpvt_5df871ab99f94347b23ca224fc7d013f': '1540020773',
    'play_stream': '1',
    'QP0013': '',
    'PCAU': '0',
    'QILINPUSH': '1',
    'QC007': 'DIRECT',
    'QC001': '1',
    'Hm_lpvt_53b7374a63c37483e5dd97d78d9bb36e': '1540022394',
    'QC010': '233186013',
    'QC159': '%7B%22color%22%3A%22FFFFFF%22%2C%22channelConfig%22%3A1%2C%22hadTip%22%3A1%2C%22isOpen%22%3A0%2C%22speed%22%3A13%2C%22density%22%3A30%2C%22opacity%22%3A86%2C%22isFilterColorFont%22%3A0%2C%22proofShield%22%3A1%2C%22forcedFontSize%22%3A24%2C%22isFilterImage%22%3A1%2C%22isset%22%3A1%7D',
    '__dfp': 'a07729e712b0db4c63a81135bdb3b42832636c0ab6e86840208a5124d029f9b372@1541316693406@1540020693406',
    'T00700': 'EgcI4b-tIRABEgcIkMDtIRAB',
    'TQC002': 'type%3Djspfmc140109%26pla%3D11%26uid%3D2d3f9a2fcda22663a554809ec477e3e2%26ppuid%3D%26brs%3DCHROME%26pgtype%3Dplay%26purl%3Dhttps%3A%252F%252Fwww.iqiyi.com%252Fv_19rr6pmtx4.html%3Flist%253D19rrm59xnm%26cid%3D1%26tmplt%3D%26tm1%3D8826%2C0%26tm8%3D1%2C9215%26tm7%3D388%2C8828%26tm9%3D5%2C9424%26tm10%3D1%2C9429%26tm6%3D12920%2C0',
    'QC112': 'f5a1645390429f99509ec069d87ac15d',
}

headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
    'Accept': '*/*',
    'Referer': 'http://m.iqiyi.com/v_19rr6pmtx4.html?list=19rrm59xnm',
    'Connection': 'keep-alive',
}

params = (
    ('uid', ''),
    ('cupid', 'qc_100001_100186'),                  # cst 表示定值
    ('platForm', 'h5'),
    ('qyid', '71b8d0b639cf6ab325d363c070373d77'),   # cst
    ('agenttype', '13'),
    ('type', 'mp4'),
    ('nolimit', ''),
    ('k_ft1', '8'),
    ('rate', '1'),
    ('sgti', '13_71b8d0b639cf6ab325d363c070373d77_1540023747287'),  # 13_{qyid}_tm + '287'(随机)
    ('codeflag', '1'),
    ('preIdAll', ''),
    ('dfp', 'a07729e712b0db4c63a81135bdb3b42832636c0ab6e86840208a5124d029f9b372'),  # cst
    ('pv', '0'),
    ('qd_v', '1'),
    ('qdy', 'a'),
    ('qds', '0'),
    ('tm', '1540023747'),                           # t
    ('src', '02020031010000000000'),                # cst
    ('vf', '7f3fe880476ce05cc909e8b403de5dc6'),     # 变量
    ('callback', 'tmtsCallback'),
)
# var a = "/jp/tmts/" + e + "/" + t + "/?" + $.param(i) + "&callback=tmtsCallback";
# vf = window.cmd5x ? window.cmd5x(a) : ""
response = requests.get('http://cache.m.iqiyi.com/jp/tmts/1447306900/6bca0f44025d50a54600fe439f4efbc4/', headers=headers, params=params, cookies=None)
print(response.text)