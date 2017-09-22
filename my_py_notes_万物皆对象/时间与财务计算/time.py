#coding:utf-8

# 获取平台所使用的纪元
import time
print(time.asctime(time.gmtime(0)))

# 当前time
print(time.asctime())

# 得到年月日
print(time.localtime().tm_year)
print(time.localtime().tm_mon)
print(time.localtime().tm_mday)
print(time.localtime().tm_hour)

tmp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print(tmp)

tmp2 = time.strftime('%Y-%m-%d %H',time.localtime(time.time()))
print(tmp2)

# time.struct_time(tm_year=2014, tm_mon=8, tm_mday=15, tm_hour=9, tm_min=42, tm_sec=20, tm_wday=4, tm_yday=227, tm_isdst=0)

# 延时
for i in range(3):
    time.sleep(0.5)
    print('fuck')
