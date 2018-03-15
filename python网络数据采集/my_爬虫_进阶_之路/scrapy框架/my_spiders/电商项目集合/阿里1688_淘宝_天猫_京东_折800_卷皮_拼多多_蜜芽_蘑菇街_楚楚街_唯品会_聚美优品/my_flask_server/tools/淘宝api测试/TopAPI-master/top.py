# -*- coding: utf8 -*-
import json,hashlib,requests,datetime, time, re
from random import randint


P_CODE = 'code'
P_SUB_CODE = 'sub_code'
P_MSG = 'msg'
P_SUB_MSG = 'sub_msg'

def sign(secret, parameters):
    #===========================================================================
    # '''签名方法
    # @param secret: 签名需要的密钥
    # @param parameters: 支持字典和string两种
    # '''
    #===========================================================================
    # 如果parameters 是字典类的话
    if hasattr(parameters, "items"):
        keys = sorted(parameters.keys())
        
        parameters = "%s%s%s" % (secret,
            str().join('%s%s' % (key, parameters[key]) for key in keys),
            secret)
    sign = hashlib.md5(parameters.encode(encoding='utf8')).hexdigest().upper()
    print(sign)

    return sign
    
def mixStr(pstr):
    #print(type(pstr))
    if(isinstance(pstr, str)):
        return pstr
    else:
        return str(pstr)

class TopException(Exception):
    #===========================================================================
    # 业务异常类
    #===========================================================================

    def __init__(self):
        self.errorcode = None
        self.message = None
        self.subcode = None
        self.submsg = None
        self.application_host = None
        self.service_host = None
    
    def format(self):
        sb = f"""错误码: {self.errorcode}\n错误消息:{self.message}"""
        
        return sb

    def __str__(self, *args, **kwargs):
        sb = "errorcode=" + mixStr(self.errorcode) +\
            " message=" + mixStr(self.message) +\
            " subcode=" + mixStr(self.subcode) +\
            " submsg=" + mixStr(self.submsg) +\
            " application_host=" + mixStr(self.application_host) +\
            " service_host=" + mixStr(self.service_host)
        return sb
        

class TaoAPI(object):
    def __init__(self,url,appkey,secret):
        self.appkey,self.secret = appkey,secret
        self.postdata = {}
        self.data = {}
        self.url = url

    def set_api_info(self, method, tpwd_param):#设置api信息 api方法 参数
        self.method = method
        self.data.update(tpwd_param)
        self.data["tpwd_param"] = json.dumps(tpwd_param)

        print(self.data)

    def get(self):
        headers = {'content-type': 'application/x-www-form-urlencoded;charset=utf-8'}

        self.data["app_key"] = self.appkey#设置appkey
        self.data["format"] = "json"#设置响应格式
        self.data["method"] = self.method#设置API接口的名称
        # #self.postdata["partner_id"] = ""#设置合作伙伴的身份标识
        self.data["sign_method"] = "md5"#设置签名的摘要算法
        self.data["timestamp"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#设置时间戳
        self.data["v"] = "2.0"#设置app协议版本

        self.postdata["sign"] = sign(self.secret, self.data)#设置API输入参数的签名结果
        #print(self.postdata["sign"])
        self.postdata.update(self.data)

        try:
            t = str(time.time().__round__()) + str(randint(100, 999))  # time.time().__round__() 表示保留到个位

            self.url = self.url + '?jsv=2.4.8&appKey=12574478&t={t}&api=mtop.ju.data.get&sign={sign}&v=1.0&type=jsonp&dataType=jsonp&callback=mtopjsonp1'.format(
                t = t,
                sign = sign(self.secret, self.data).lower()
            )
            # print(self.url)

            # r = requests.post(self.url, headers=headers, data=self.postdata)

            r = requests.get(self.url, headers=headers, params={'data':self.data['data']}, timeout=13)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
            last_url = re.compile(r'\+').sub('', r.url)  # 转换后得到正确的url请求地址
            print(last_url)
            r = requests.get(last_url, headers=headers, timeout=13)
            print(r.content.decode('utf-8'))

            jsonobj = r.json()
            if "error_response" in jsonobj:
                error = TopException()
                if P_CODE in jsonobj["error_response"]:
                    error.errorcode = jsonobj["error_response"][P_CODE]
                if P_MSG in jsonobj["error_response"]:
                    error.message = jsonobj["error_response"][P_MSG]
                if P_SUB_CODE in jsonobj["error_response"]:
                    error.subcode = jsonobj["error_response"][P_SUB_CODE]
                if P_SUB_MSG in jsonobj["error_response"]:
                    error.submsg = jsonobj["error_response"][P_SUB_MSG]
                error.application_host = r.headers.get("Application-Host", "")
                error.service_host = r.headers.get("Location-Host", "")
                raise error

            return r.json()
        
        except TopException as msg:
            print(msg)

    def timestamp_to_regulartime(self, timestamp):
        '''
        将时间戳转换成时间
        '''
        # 利用localtime()函数将时间戳转化成localtime的格式
        # 利用strftime()函数重新格式化时间

        # 转换成localtime
        time_local = time.localtime(int(timestamp))
        # print(time_local)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

        return dt