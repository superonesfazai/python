# coding:utf-8

'''
@author = super_fazai
@File    : flask_部署后并发测试_规模_300.py
@Time    : 2017/10/21 21:47
@connect : superonesfazai@gmail.com
'''

import threading, time, requests
url = "http://0.0.0.0:5000"
total = 0
suc = 0
fail = 0
exception = 0
maxtime=0
mintime=100
gt3=0
lt3=0
class RequestThread(threading.Thread):
    def __init__(self, thread_name):
        threading.Thread.__init__(self)
        self.test_count = 0
    def run(self):
        self.test_performace()
    def test_performace(self):
            global total
            global suc
            global fail
            global exception
            global gt3
            global lt3
            try:
                st = time.time()
                conn = requests.get(url)
                res = conn.status_code
                if res== 200:
                    total+=1
                    suc+=1
                else:
                    total+=1
                    fail+=1
                time_span = time.time()-st
                print ('%s:%f\n' % (self.name,time_span))
                self.maxtime(time_span)
                self.mintime(time_span)
                if time_span>3:
                    gt3+=1
                else:
                    lt3+=1
            except Exception as e:
                print (e)
                total+=1
                exception+=1
    def maxtime(self,ts):
            global maxtime
            print(ts)
            if ts>maxtime:
                maxtime=ts
    def mintime(self,ts):
            global mintime
            if ts<mintime:
                mintime=ts
print ('===========请求开始===========')
start_time = time.time()
thread_count = 100
i = 0
while i <= thread_count:
    t = RequestThread("线程：" + str(i))
    t.start()
    i += 1
t=0
while total<thread_count|t>20:
        print ("总数:%d,成功数:%d,失败:%d,异常:%d\n"%(total,suc,fail,exception))
        print (url)
        t+=1
        time.sleep(1)
print ('===========task end===========')
print ("总数:%d,成功:%d,失败:%d,异常:%d"%(total,suc,fail,exception))
print ('响应最大时间:',maxtime)
print ('响应最小时间',mintime)
print ('大于3秒的响应:%d,占比:%0.2f'%(gt3,float(gt3)/total))
print ('小于3秒:%d,占比:%0.2f'%(lt3,float(lt3)/total))