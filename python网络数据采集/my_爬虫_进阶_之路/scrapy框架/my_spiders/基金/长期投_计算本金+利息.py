# coding:utf-8

'''
@author = super_fazai
@File    : 长期投_计算本金+利息.py
@connect : superonesfazai@gmail.com
'''

def long_invest_principal_add_interest(principal, interest, day, every_month_add_money):
    '''
    长期投资: 计算本金加利息(复利再投)
    :param principal: 本金
    :param interest: 年化利率
    :param day: 投资天数
    :param every_month_add_money: 每月定投
    :return:
    '''
    tmp_principal = principal
    for index in range(1, day+1):
        if index % 30 == 0:     # 每月定投
            tmp_principal += every_month_add_money

        if tmp_principal > 50000:
            interest = 0.114

        profit = tmp_principal * interest / 365
        tmp_principal += profit
        # print('第{0}天本金加利息: {1}, 日盈利: {2}'.format(index, round(tmp_principal, 2), round(profit, 2)))

    return tmp_principal

'''理财的重要性'''
invest_year = 5
for i in range(1, invest_year + 1):
    # 例如: 1W的本金, 每月定投6000
    principal = 10000
    interest = 0.096        # 年化收益 9.6%

    day = 365 * 1 * i
    every_month_add_money = 6000
    money = long_invest_principal_add_interest(
        principal=principal,
        interest=interest,
        day=day,
        every_month_add_money=every_month_add_money
    )
    print('> 假如存{0}年'.format(i))
    print('钱躺银行: {0}'.format(principal + day/30 * every_month_add_money))
    print('不躺银行: {0}\n'.format(money))
