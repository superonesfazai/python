# coding:utf-8

'''
@author = super_fazai
@File    : 某基金的单位净值走势_累计净值走势.py
@Time    : 2018/7/10 18:26
@connect : superonesfazai@gmail.com
'''

import requests
import re
from pprint import pprint
from urllib.parse import unquote
from my_requests import MyRequests
from matplotlib.font_manager import FontProperties
import gc
import os

def get_shanghai_time():
    '''
    时区处理，得到上海时间
    :return: datetime类型
    '''
    import pytz
    import datetime
    import re

    # 时区处理，时间处理到上海时间
    # pytz查询某个国家时区
    country_timezones_list = pytz.country_timezones('cn')
    # print(country_timezones_list)

    tz = pytz.timezone('Asia/Shanghai')  # 创建时区对象
    now_time = datetime.datetime.now(tz)

    # 处理为精确到秒位，删除时区信息
    now_time = re.compile(r'\..*').sub('', str(now_time))
    # 将字符串类型转换为datetime类型
    now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')

    return now_time

def timestamp_to_regulartime(timestamp):
    '''
    将时间戳转换成时间
    '''
    import time
    # 利用localtime()函数将时间戳转化成localtime的格式
    # 利用strftime()函数重新格式化时间

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))

def json_str_2_dict(json_str):
    from json import JSONDecodeError, loads
    try:
        _ = loads(json_str)
    except JSONDecodeError as e:
        print(e)
        _ = {}

    return _

def unquote_cookies(cookies: dict):
    '''
    # cookies解码
    :param cookies:
    :return:
    '''
    from urllib.parse import unquote
    _ = {}
    for key, value in cookies.items():
        _.update({
            key: unquote(value, encoding='utf-8').encode().decode(),
        })

    return _

cookies = {
    'st_pvi': '11586003301354',
    'st_si': '46806950936799',
    'ASP.NET_SessionId': 'fhllwae2zicg00o0x4ub1fxs',
    'EMFUND1': 'null',
    'EMFUND0': 'null',
    # 'EMFUND2': '07-10%2018%3A01%3A38@%23%24%u534E%u6DA6%u5143%u5927%u73B0%u91D1%u901A%u8D27%u5E01B@%23%24002884',
    'EMFUND2': '07-10 18:01:38@#$华润元大现金通货币B@#$002884',
    # 'EMFUND3': '07-10%2018%3A01%3A48@%23%24%u5929%u5F18%u73B0%u91D1%u7BA1%u5BB6%u8D27%u5E01B@%23%24420106',
    'EMFUND3': '07-10 18:01:48@#$天弘现金管家货币B@#$420106',
    # 'EMFUND4': '07-10%2018%3A11%3A53@%23%24%u65B9%u6B63%u5BCC%u90A6%u4FDD%u9669%u4E3B%u9898%u6307%u6570%u5206%u7EA7@%23%24167301',
    'EMFUND4': '07-10 18:11:53@#$方正富邦保险主题指数分级@#$167301',
    # 'EMFUND5': '07-10%2018%3A04%3A32@%23%24%u62DB%u5546%u4E2D%u8BC1%u94F6%u884C%u6307%u6570%u5206%u7EA7@%23%24161723',
    'EMFUND5': '07-10 18:04:32@#$招商中证银行指数分级@#$161723',
    # 'EMFUND6': '07-10%2018%3A05%3A13@%23%24%u5929%u5F18%u4E2D%u8BC1%u94F6%u884C%u6307%u6570C@%23%24001595',
    'EMFUND6': '07-10 18:05:13@#$天弘中证银行指数C@#$001595',
    # 'EMFUND7': '07-10%2018%3A06%3A13@%23%24%u5929%u5F18%u4E2D%u8BC1%u94F6%u884C%u6307%u6570A@%23%24001594',
    'EMFUND7': '07-10 18:06:13@#$天弘中证银行指数A@#$001594',
    # 'EMFUND8': '07-10%2018%3A11%3A22@%23%24%u7533%u4E07%u83F1%u4FE1%u591A%u7B56%u7565%u7075%u6D3B%u914D%u7F6E%u6DF7%u5408A@%23%24001148',
    'EMFUND8': '07-10 18:11:22@#$申万菱信多策略灵活配置混合A@#$001148',
    # 'EMFUND9': '07-10 18:12:26@#$%u5E7F%u53D1%u751F%u7269%u79D1%u6280%u6307%u6570%28QDII%29@%23%24001092',
    'EMFUND9': '07-10 18:12:26@#$广发生物科技指数(QDII)@#$001092',
}

cookies = unquote_cookies(cookies)
# pprint(cookies)

headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Accept': '*/*',
    # 'Referer': 'http://fund.eastmoney.com/001092.html',
    'Proxy-Connection': 'keep-alive',
}

v = re.compile(r'-| |:').sub('', str(get_shanghai_time()))  # 2018-07-10 18:30:46 -> 20180710183046
# print(v)
params = (
    # ('v', '20180710175951'),    # 时间
    ('v', v),  # 时间
)

def deal_with_data_net_worth_trend(fund_name, fund_code, data_net_worth_trend):
    '''
    处理data_net_worth_trend(单位净值走势), 并成像
    :param fund_name:
    :param fund_code:
    :param data_net_worth_trend:
    :return:
    '''
    [item.update({'x': str(timestamp_to_regulartime(str(item.get('x'))[:10]))}) for item in data_net_worth_trend]
    print('时间格式转换成功!')
    # pprint(data_net_worth_trend)

    # 绘图
    # 加载字体
    font = FontProperties(fname='/Library/Fonts/Songti.ttc', size=15)

    import matplotlib.pyplot as plt
    from matplotlib.pyplot import savefig

    # 显示标题
    plt.title('基金名(代码{0}): {1} 的单位净值走势图'.format(fund_code, fund_name), fontproperties=font, fontsize=18)
    plt.ylabel('价格', fontproperties=font)
    plt.xlabel('日期', fontproperties=font)

    # 显示网格
    plt.grid()

    x = [item.get('x') for item in data_net_worth_trend]
    y = [item.get('y') for item in data_net_worth_trend]

    # 设置x轴值区间
    # plt.xlim(x[0], x[-2])

    # 调用绘制线性图函数plot()
    plt.plot(x, y, marker='o', markerfacecolor='r', markersize=5)

    # 显示图例
    plt.legend(['单位:元'], loc=1, prop=font)

    # 标识数字标签
    for a, b in zip(x, y):
        plt.text(a, b, '%.3f' % (b,), fontsize=5)

    # 调用show方法显式
    # plt.show()

    # 保存pic
    base_path = '/Users/afa/myFiles/tmp/基金/'
    pic_file_name = '{0}(代码{1}).jpg'.format(fund_name, fund_code)
    pic_path = base_path + pic_file_name
    if os.path.exists(pic_path):    # 原先存在，就删除!
        # print('文件已存在!')
        os.remove(pic_path)

    savefig(pic_path)
    print('{0} 保存完毕!'.format(pic_file_name))

    del plt
    gc.collect()

    return True

def get_this_fund_info(body):
    try:
        # 基金名
        fund_name = re.compile(r'fS_name = "(.*?)";').findall(body)[0]
        # 基金代码
        fund_code = re.compile(r'fS_code = "(.*?)";').findall(body)[0]
        print('基金名: {0}, 基金代码: {1}'.format(fund_name, fund_code))

        # 购买手续费
        fund_source_rate = re.compile(r'fund_sourceRate="(.*?)";').findall(body)[0]
        # 现费率
        fund_rate = re.compile('fund_Rate="(.*?)";').findall(body)[0]
        # 最小起购金额
        fund_minsg = re.compile(r'fund_minsg="(.*?)";').findall(body)[0]
        print('购买手续费: {0}%, 现费率: {1}%, 最小起购金额: {2}RMB'.format(fund_source_rate, fund_rate, fund_minsg))

        '''收益率'''
        # 近一年收益率
        syl_1n = re.compile(r'syl_1n="(.*?)";').findall(body)[0]
        # 近6月收益率
        syl_6y = re.compile(r'syl_6y="(.*?)";').findall(body)[0]
        # 近三月收益率
        syl_3y = re.compile(r'syl_3y="(.*?)";').findall(body)[0]
        # 近一月收益率
        syl_1y = re.compile(r'syl_1y="(.*?)";').findall(body)[0]
        msg = '@@收益率:\n\t近1年: {0}%, 近6月: {1}%, 近3月: {2}%, 近1月: {3}%'.format(syl_1n, syl_6y, syl_3y, syl_1y)
        print(msg)

        # 单位净值走势 equityReturn-净值回报 unitMoney-每份派送金
        data_net_worth_trend = json_str_2_dict(re.compile(r'Data_netWorthTrend = (.*?);').findall(body)[0])
        # pprint(data_net_worth_trend)
        # print('单位净值走势: {0}'.format(data_net_worth_trend))
        deal_with_data_net_worth_trend(
            fund_name=fund_name,
            fund_code=fund_code,
            data_net_worth_trend=data_net_worth_trend)

        # 累计净值走势
        data_ac_worth_trend = json_str_2_dict(re.compile(r'Data_ACWorthTrend = (.*?);').findall(body)[0])
        # pprint(data_ac_worth_trend)
        # print('累计净值走势: {0}'.format(data_ac_worth_trend))

        # 累计收益率走势
        data_grand_total = json_str_2_dict(re.compile(r'Data_grandTotal = (.*?);').findall(body)[0])
        # print('累计收益率走势: {0}'.format(data_grand_total))

        # 同类排名走势
        data_rate_in_similar_type = json_str_2_dict(re.compile(r'Data_rateInSimilarType = (.*?);').findall(body)[0])
        # print('同类排名走势: {0}'.format(data_rate_in_similar_type))

        # 同类排名百分比
        data_rate_in_similar_persent = json_str_2_dict(re.compile(r'Data_rateInSimilarPersent=(.*?);').findall(body)[0])
        # print('同类排名百分比: {0}'.format(data_rate_in_similar_persent))

        # 同类型基金涨幅榜（页面底部通栏）
        swith_same_type = json_str_2_dict(re.compile(r'swithSameType = (.*?);').findall(body)[0])
        # print('同类型基金涨幅榜: {0}'.format(swith_same_type))

    except IndexError as e:
        print(e)

fund_url = 'http://fund.eastmoney.com/pingzhongdata/001092.js'
# response = requests.get(fund_url, headers=headers, params=params, cookies=None)
# body = response.text
# print(body)

body = MyRequests.get_url_body(url=fund_url, headers=headers, params=params, cookies=None)
# print(body)
get_this_fund_info(body=body)

