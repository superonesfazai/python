#coding:utf-8

import datetime

'''
datetime类型的时间->str类型
'''
today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(today)

# birthday = datetime.date(1996, 8, 24)
# print(birthday)
# currenttime = datetime.datetime.now()
# now = datetime.datetime
# print(now)