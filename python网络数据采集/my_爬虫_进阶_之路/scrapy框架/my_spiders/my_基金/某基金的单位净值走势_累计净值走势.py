# coding:utf-8

'''
@author = super_fazai
@File    : 某基金的单位净值走势_累计净值走势.py
@Time    : 2018/7/10 18:26
@connect : superonesfazai@gmail.com
'''

import re
from pprint import pprint
from urllib.parse import unquote
from matplotlib.font_manager import FontProperties
import gc
import os
from numpy import arange
import datetime
from time import sleep
import demjson
from matplotlib.pyplot import savefig

from fzutils.spider.fz_requests import MyRequests
from fzutils.time_utils import (
    get_shanghai_time,
    timestamp_to_regulartime,
    string_to_datetime,)

def month_differ(x, y):
    """暂不考虑day, 只根据month和year计算相差月份
    Parameters
    ----------
    x, y: 两个datetime.datetime类型的变量

    Return
    ------
    differ: x, y相差的月份
    """
    month_differ = abs((x.year - y.year) * 12 + (x.month - y.month) * 1)

    return month_differ

def json_2_dict(json_str):
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

class BaseFund(object):
    def __init__(self, base_path='/Users/afa/myFiles/tmp/基金/伪好基/'):
        '''
        :param base_path: 基金图片存储path
        '''
        self.page_num_start = 1     # 开放基金排行开始page
        self.page_num_end = 3
        self.CRAWL_FUND_TIME = 1.5  # 抓取每只基金的sleep time
        self.plot_pic = None
        self.base_path = base_path

    def _get_rank_fund_info(self):
        '''
        得到天天基金全部基金的rank_fund
        :return: a list
        '''
        rank_fund_list = []
        for page_num in range(self.page_num_start, self.page_num_end):
            print('正在抓取第{0}页的基金信息...'.format(page_num))
            cookies = {
                'st_pvi': '11586003301354',
                'EMFUND1': 'null',
                'EMFUND0': 'null',
                'EMFUND2': '07-10%2018%3A01%3A38@%23%24%u534E%u6DA6%u5143%u5927%u73B0%u91D1%u901A%u8D27%u5E01B@%23%24002884',
                'EMFUND3': '07-10%2018%3A01%3A48@%23%24%u5929%u5F18%u73B0%u91D1%u7BA1%u5BB6%u8D27%u5E01B@%23%24420106',
                'EMFUND4': '07-10%2018%3A11%3A53@%23%24%u65B9%u6B63%u5BCC%u90A6%u4FDD%u9669%u4E3B%u9898%u6307%u6570%u5206%u7EA7@%23%24167301',
                'EMFUND5': '07-10%2018%3A04%3A32@%23%24%u62DB%u5546%u4E2D%u8BC1%u94F6%u884C%u6307%u6570%u5206%u7EA7@%23%24161723',
                'EMFUND6': '07-10%2018%3A05%3A13@%23%24%u5929%u5F18%u4E2D%u8BC1%u94F6%u884C%u6307%u6570C@%23%24001595',
                'EMFUND7': '07-10%2018%3A06%3A13@%23%24%u5929%u5F18%u4E2D%u8BC1%u94F6%u884C%u6307%u6570A@%23%24001594',
                'st_si': '38764934559714',
                'ASP.NET_SessionId': 'hqeo1xk5oqgwb0cqzxicytda',
                'EMFUND8': '07-11 11:28:55@#$%u7533%u4E07%u83F1%u4FE1%u591A%u7B56%u7565%u7075%u6D3B%u914D%u7F6E%u6DF7%u5408A@%23%24001148',
                'EMFUND9': '07-11 11:28:55@#$%u5E7F%u53D1%u751F%u7269%u79D1%u6280%u6307%u6570%28QDII%29@%23%24001092',
            }

            headers = {
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                'Accept': '*/*',
                # 'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
                'Proxy-Connection': 'keep-alive',
            }

            end_date = str(get_shanghai_time())[:10]
            start_date = str(datetime.datetime(year=get_shanghai_time().year-1, month=get_shanghai_time().month, day=get_shanghai_time().day))[:10]
            print('开始时间: {0}, 结束时间: {1}'.format(start_date, end_date))

            params = (
                ('op', 'ph'),
                ('dt', 'kf'),
                ('ft', 'all'),
                ('rs', ''),
                ('gs', '0'),
                ('sc', 'zzf'),
                ('st', 'desc'),
                ('sd', start_date),     # '2017-07-10'
                ('ed', end_date),       # '2018-07-10'
                ('qdii', ''),
                ('tabSubtype', ',,,,,'),
                ('pi', str(page_num)),            # rank_data的页码
                ('pn', '50'),
                ('dx', '1'),
                ('v', '0.5290053467389759'),
            )

            url = 'http://fund.eastmoney.com/data/rankhandler.aspx'
            body = MyRequests.get_url_body(url=url, headers=headers, params=params, cookies=None)
            # print(body)

            try:
                this_page_rank_data = re.compile(r'rankData = (.*);').findall(body)[0]
                # print(this_page_rank_data)
            except IndexError:
                print('在获取this_page_rank_data时索引异常!请检查!')
                continue

            # 报错: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
            # 解决方案: 用demjson处理下
            this_page_rank_data = demjson.decode(this_page_rank_data).get('datas', {})
            # pprint(this_page_rank_data)
            if this_page_rank_data == {}:
                return []

            for item in this_page_rank_data:
                _i = item.split(',')
                rank_fund_list.append({
                    '基金代码': _i[0],
                    '基金简称': _i[1],
                    '当天日期': _i[3],
                    '单位净值': _i[4],
                    '累计净值': _i[5],
                    '日增长率': _i[6],
                    '近1周': _i[7],
                    '近1月': _i[8],
                    '近3月': _i[9],
                    '近6月': _i[10],
                    '近1年': _i[11],
                    '近2年': _i[12],
                    '近3年': _i[13],
                    '今年来': _i[14],
                    '成立来': _i[15],
                    '手续费': _i[20],
                })

            sleep(2.5)

        print('\n抓取完毕!\n')

        # pprint(rank_fund_list)

        return rank_fund_list

    def _deal_with_rank_fund_info(self):
        '''
        处理rank_fund_info
        :return:
        '''
        rank_fund_list = self._get_rank_fund_info()

        for item in rank_fund_list:
            fund_code = item.get('基金代码', '')
            print('正在处理基金代码: {0}...'.format(fund_code))
            self._get_one_fund_info(fund_code=fund_code)
            sleep(self.CRAWL_FUND_TIME)

        print('\n@@@ 所有操作完成!\n')

        return True

    def _get_one_fund_info(self, fund_code):
        '''
        得到一只基金的info，并处理
        :return:
        '''
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

        fund_url = 'http://fund.eastmoney.com/pingzhongdata/{0}.js'.format(fund_code)
        # response = requests.get(fund_url, headers=headers, params=params, cookies=None)
        # body = response.text
        # print(body)

        body = MyRequests.get_url_body(url=fund_url, headers=headers, params=params, cookies=None)
        # print(body)
        self._get_this_fund_info(body=body)

        return True

    def _get_this_fund_info(self, body):
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
            data_net_worth_trend = json_2_dict(re.compile(r'Data_netWorthTrend = (.*?);').findall(body)[0])
            # pprint(data_net_worth_trend)
            # print('单位净值走势: {0}'.format(data_net_worth_trend))
            self._deal_with_data_net_worth_trend(
                fund_name=fund_name,
                fund_code=fund_code,
                data_net_worth_trend=data_net_worth_trend)

            # 累计净值走势
            data_ac_worth_trend = json_2_dict(re.compile(r'Data_ACWorthTrend = (.*?);').findall(body)[0])
            # pprint(data_ac_worth_trend)
            # print('累计净值走势: {0}'.format(data_ac_worth_trend))

            # 累计收益率走势
            data_grand_total = json_2_dict(re.compile(r'Data_grandTotal = (.*?);').findall(body)[0])
            # print('累计收益率走势: {0}'.format(data_grand_total))

            # 同类排名走势
            data_rate_in_similar_type = json_2_dict(re.compile(r'Data_rateInSimilarType = (.*?);').findall(body)[0])
            # print('同类排名走势: {0}'.format(data_rate_in_similar_type))

            # 同类排名百分比
            data_rate_in_similar_persent = json_2_dict(re.compile(r'Data_rateInSimilarPersent=(.*?);').findall(body)[0])
            # print('同类排名百分比: {0}'.format(data_rate_in_similar_persent))

            # 同类型基金涨幅榜（页面底部通栏）
            swith_same_type = json_2_dict(re.compile(r'swithSameType = (.*?);').findall(body)[0])
            # print('同类型基金涨幅榜: {0}'.format(swith_same_type))

        except IndexError as e:
            print(e)

        return None

    def _deal_with_data_net_worth_trend(self, **kwargs):
        '''
        处理data_net_worth_trend(单位净值走势), 并成像
        :param fund_name:
        :param fund_code:
        :param data_net_worth_trend:
        :return:
        '''
        fund_name = kwargs.get('fund_name')
        fund_code = kwargs.get('fund_code')
        data_net_worth_trend = kwargs.get('data_net_worth_trend', [])

        [item.update({'x': str(timestamp_to_regulartime(str(item.get('x'))[:10]))}) for item in data_net_worth_trend]
        print('时间格式转换成功!')
        # pprint(data_net_worth_trend)

        x = [item.get('x') for item in data_net_worth_trend]
        y = [item.get('y') for item in data_net_worth_trend]

        '''绘图'''
        self.plot_pic = self._drawing(fund_name=fund_name, fund_code=fund_code, x=x, y=y)

        try: del self.plot_pic
        except: pass
        gc.collect()

        return True

    def _drawing(self, **kwargs):
        '''
        初始化画笔
        :param kwargs:
        :return:
        '''
        import matplotlib.pyplot as plt
        from random import randint

        figure_num = randint(1, 10000)
        plt.figure(figure_num)   # 创建图表1, 一个Figure对象可以包含多个子图（Axes）, 从而避免图都画在一张上

        fund_name = kwargs.get('fund_name')
        fund_code = kwargs.get('fund_code')
        x = kwargs.get('x')
        y = kwargs.get('y')

        # 加载字体
        font = FontProperties(fname='/Library/Fonts/Songti.ttc', size=10)

        # 显示标题
        plt.title('{0}(代码{1})的单位净值走势图'.format(fund_name, fund_code), fontproperties=font, fontsize=15)
        plt.xlabel('日期', fontproperties=font)
        plt.ylabel('单位净值', fontproperties=font)

        # 显示网格
        # plt.grid()    # 太密集了不显示

        # 设置坐标轴步长step
        x_axis_label = self._get_x_axis_label(x)
        # pprint(x_axis_label)
        y_axis_label = self._get_y_axis_label(y)
        # pprint(y_axis_label)
        plt.xticks(arange(len(x_axis_label)), x_axis_label, rotation=30, fontsize=5)     # 放str得先处理成这个格式
        # plt.yticks(y_axis_label)

        # 设置x轴值区间
        # plt.xlim(x[0], x[-2])

        # 显示图例
        plt.legend(['单位:元'], loc=1, prop=font)

        plt.figure(figure_num)
        # 调用绘制线性图函数plot()
        plot_pic = plt.plot(
            x,
            y,
            marker='.',
            markerfacecolor='r',
            markersize=1,  # 标记的点的size
            linewidth=.4,  # 线宽
            color='#7EB6EA'  # 线的颜色
        )

        # 标识数字标签
        # for a, b in zip(x, y):
        #     plt.text(a, b, '%.3f' % (b,), fontsize=5)

        # 调用show方法显式
        # plt.show()

        # 保存pic
        pic_file_name = '{0}(代码{1}).jpg'.format(fund_name, fund_code)
        pic_path = self.base_path + pic_file_name
        if os.path.exists(pic_path):  # 原先存在，就删除!
            # print('文件已存在!')
            os.remove(pic_path)

        savefig(fname=pic_path, dpi=300)  # dpi控制图片像素
        print('[+] {0} 保存完毕!'.format(pic_file_name))

        plt.cla()   # 清空当前图像

        return plot_pic

    def _get_x_axis_label(self, x):
        '''
        得到x轴的刻度list
        :param x:
        :return: list
        '''
        now_time = datetime.datetime.now()
        x_axis_label = []
        for _x in x:
            if _x is not None and month_differ(now_time, string_to_datetime(_x)) % 6 == 0:
                if str(_x)[:7] in x_axis_label:     # 如果已存在append('')
                    x_axis_label.append('')
                else:
                    x_axis_label.append(str(_x)[:7])
            else:
                x_axis_label.append('')

        return x_axis_label

    def _get_y_axis_label(self, y):
        '''
        得到y轴的刻度list
        :param y:
        :return:
        '''
        y_step = .1
        y_axis_label = [_y for _y in arange(min(y) - y_step, max(y) + y_step, y_step)]

        return y_axis_label

    def __del__(self):
        gc.collect()

if __name__ == '__main__':
    _ = BaseFund()
    # fund_code = '001092'
    # _._get_one_fund_info(fund_code=fund_code)
    _._deal_with_rank_fund_info()

    # rank_data = _._get_rank_fund_info()
    # rank_data = [item for item in rank_data if float(item.get('成立来')) > 10.]
    # pprint(rank_data)