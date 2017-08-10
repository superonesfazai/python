#coding:utf-8

# 获取平台所使用的纪元
import time
print(time.asctime(time.gmtime(0)))

# 当前time
print(time.asctime())

# 得到年月日
print(time.localtime().tm_mon)

# 延时
for i in range(3):
    time.sleep(0.5)
    print('fuck')
