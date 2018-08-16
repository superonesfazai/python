# coding:utf-8

'''
@author = super_fazai
@File    : 关于母基金_A份额_B份额.py
@Time    : 2017/3/16 13:19
@connect : superonesfazai@gmail.com
'''

from CAL.PyCAL import *

def get_leverage_fund(show_type='M', order_by='discount_rate', order_method='desc', date=None):
    '''
    输入参数：
       show_type  str，展示/返回的数据，'T'为返回所有，'A'为返回A类相关，'B'为返回B类相关，'M'为返回母基金相关
       order_by  str，返回结果的排序属性列，可选的为'B_leverage'(B类价格杠杆),'ticker'(交易代码),'discount_rate'(整体溢价率)
       order_method  str，排序规则，降序（'desc'）,升序（'acd'）
    输出参数：
       计算好指标的dataframe，同时还将结果直接打印出来
    '''
    import pandas as pd
    import numpy as np

    if show_type not in ['T','A','B','M']:
        raise ValueError('show type 必须为T，A，B，M中的一个！')

    if order_by not in ['B_leverage','ticker','discount_rate']:
        raise ValueError('order_by 必须为B_leverage,ticker,discount_rate中的一个！')

    if order_method not in ['desc','acd']:
        raise ValueError('order_method 必须为desc,acd中的一个！')

    # 日期默认为前一个工作日
    if date is None:
        date = Date.todaysDate()
        cal = Calendar('China.SSE')
        period = Period('-1B')
        date = cal.advanceDate(date, period)
        date = date.toDateTime().strftime('%Y%m%d')
    elif not (isinstance(date, str) and len(date) == 8):
        raise ValueError('date必须为xxxxxxxx字符串类型日期格式！')

    # 所有股票类分级基金ticker
    funds = DataAPI.FundLeverageInfoGet(exchangeCDLeverage=['XSHG','XSHE'], field='ticker,secShortName,tickerLeverage,secShortNameLeverage,shareType,category,,shareProp,idxCn,splitNote,downThrshold')
    funds_total = funds[funds['category']=='E']
    funds_total.drop('category', axis=1, inplace=True)
    funds_total.columns = ['母基金代码','母基金简称','子基金代码','子基金简称','份额类别','分拆比例A/B','跟踪指数','折算说明','下折B阈值']
    funds_total['子基金代码'] = funds_total['子基金代码'].apply(str)
    funds_total['分拆比例A/B'][funds_total['分拆比例A/B'] == 1] = 5.0

    # 替换基金简称
    codes = funds_total.drop_duplicates('母基金代码')['母基金代码'].tolist()
    codes_leverage = map(str,funds_total['子基金代码'].tolist())
    short_names = DataAPI.FundGet(ticker=codes_leverage+codes, listStatusCd=['L','UN'], field='ticker,tradeAbbrName', pandas='1')
    tmp = pd.merge(funds_total, short_names, how='left', left_on='母基金代码', right_on='ticker')
    funds_total['母基金简称'] = tmp['tradeAbbrName']
    tmp = pd.merge(funds_total, short_names, how='left', left_on='子基金代码', right_on='ticker')
    funds_total['子基金简称'] = tmp['tradeAbbrName']

    # 取净值
    net_values = DataAPI.FundNavGet(ticker=codes+codes_leverage, dataDate=date, field='ticker,NAV', pandas='1')
    tmp = pd.merge(funds_total, net_values, how='left', left_on='母基金代码', right_on='ticker')
    funds_total['母基金净值'] = tmp['NAV']
    tmp = pd.merge(funds_total, net_values, how='left', left_on='子基金代码', right_on='ticker')
    funds_total['子基金净值'] = tmp['NAV']

    # 取行情
    prices = DataAPI.MktFunddGet(ticker=codes+codes_leverage, field='ticker,closePrice', tradeDate=date, pandas='1')
    tmp = pd.merge(funds_total, prices, how='left', left_on='子基金代码', right_on='ticker')
    funds_total['子基金价格'] = tmp['closePrice']
    funds_total['子基金溢价率'] = funds_total['子基金价格'] / funds_total['子基金净值'] - 1

    # 计算相关指标，合并dataframe
    funds_A = funds_total[funds_total['份额类别'] == 'A']
    funds_A.drop('份额类别',axis=1, inplace=True)
    funds_B = funds_total[funds_total['份额类别'] == 'B'][['母基金代码','子基金代码','子基金简称','子基金净值','子基金价格','子基金溢价率']]
    funds_B.columns = [['母基金代码','B类代码','B类简称','B类净值','B类价格','B类溢价率']]
    funds_leverage = pd.merge(funds_A, funds_B, how='left', on='母基金代码')
    funds_leverage.rename(columns={'子基金代码':'A类代码', '子基金简称':'A类简称', '子基金净值':'A类净值', '子基金价格':'A类价格', '子基金溢价率':'A类溢价率'}, inplace=True)
    funds_leverage['整体溢价率'] = (funds_leverage['A类价格'] * (funds_leverage['分拆比例A/B'] / 10) + funds_leverage['B类价格'] * (1 - funds_leverage['分拆比例A/B'] / 10)) / funds_leverage['母基金净值'] -1
    funds_leverage['B类价格杠杆'] = (funds_leverage['A类价格'] * funds_leverage['分拆比例A/B'] / 10 + funds_leverage['B类价格'] * (1 - funds_leverage['分拆比例A/B'] / 10)) / funds_leverage['B类价格'] / (1 - funds_leverage['分拆比例A/B'] / 10)
    funds_leverage['下折母需跌'] = 1 - (funds_leverage['A类净值'] * funds_leverage['分拆比例A/B'] / 10 + funds_leverage['下折B阈值'] * (1 - funds_leverage['分拆比例A/B'] / 10)) / funds_leverage['母基金净值']
    funds_leverage = funds_leverage[['母基金代码','母基金简称','母基金净值','整体溢价率','跟踪指数','分拆比例A/B','下折母需跌','A类代码','A类简称','A类净值','A类价格','A类溢价率','B类代码','B类简称','B类净值','B类价格','B类溢价率','B类价格杠杆','下折B阈值','折算说明']]
    funds_leverage['B类价格杠杆'] = np.round(funds_leverage['B类价格杠杆'], 2)
    funds_leverage.dropna(inplace=True)
    funds_leverage['整体溢价率'] = pd.Series(["{0:.1f}%".format(val * 100) for val in funds_leverage['整体溢价率']], index = funds_leverage.index)
    funds_leverage['A类溢价率'] = pd.Series(["{0:.1f}%".format(val * 100) for val in funds_leverage['A类溢价率']], index = funds_leverage.index)
    funds_leverage['B类溢价率'] = pd.Series(["{0:.1f}%".format(val * 100) for val in funds_leverage['B类溢价率']], index = funds_leverage.index)
    funds_leverage['下折母需跌'] = pd.Series(["{0:.1f}%".format(val * 100) for val in funds_leverage['下折母需跌']], index = funds_leverage.index)

    # 返回类型
    if show_type == 'T':
        columns = funds_leverage.columns
    elif show_type == 'A':
        columns = ['A类代码','A类简称','A类净值','A类价格','A类溢价率','整体溢价率','跟踪指数']
    elif show_type == 'B':
        columns = ['B类代码','B类简称','B类净值','B类价格','B类溢价率','B类价格杠杆','下折B阈值','整体溢价率','跟踪指数']
    else:
        columns = ['母基金代码','母基金简称','母基金净值','整体溢价率','跟踪指数','分拆比例A/B','下折母需跌','折算说明']

    # 排序
    if order_by == 'B_leverage':
        order_by = 'B类价格杠杆'
    elif order_by == 'ticker':
        order_by = '母基金代码'
    else:
        order_by = '整体溢价率'

    if order_method == 'acd':
        res = funds_leverage.sort(columns=order_by, ascending=True)[columns]
    else:
        res = funds_leverage.sort(columns=order_by, ascending=False)[columns]

    res = res.reset_index().drop('index', axis=1)

    return res

get_leverage_fund()