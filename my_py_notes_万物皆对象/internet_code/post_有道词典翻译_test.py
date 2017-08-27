# coding = utf-8

'''
@author = super_fazai
@File    : post_有道词典翻译_test.py
@Time    : 2017/8/27 21:08
@connect : superonesfazai@gmail.com
'''

import urllib
import urllib.request
import urllib.parse

# POST请求的目标URL
url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"

headers={
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
}

formdata = {
    "type":"AUTO",
    "i":"i love python",
    "doctype":"json",
    "xmlVersion":"1.8",
    "keyfrom":"fanyi.web",
    "ue":"UTF-8",
    "action":"FY_BY_ENTER",
    "typoResult":"true"
}

data = urllib.parse.urlencode(formdata)

request = urllib.request.Request(url, data = data.encode('utf-8'), headers = headers)
response = urllib.request.urlopen(request)
print(response.read().decode('utf-8'))

'''
发送POST请求时，需要特别注意headers的一些属性：

    Content-Length: 144： 是指发送的表单数据长度为144，
        也就是字符个数是144个。
    
    X-Requested-With: XMLHttpRequest ：表示Ajax异步请求。
    
    Content-Type: application/x-www-form-urlencoded ： 
        表示浏览器提交 Web 表单时使用，
        表单数据会按照 name1=value1&name2=value2 键值对形式进行编码。
'''