# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

"""
driver截获请求数据
"""

from selenium import webdriver

PHANTOMJS_DRIVER_PATH = '/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs'
driver = webdriver.PhantomJS(executable_path=PHANTOMJS_DRIVER_PATH)
# url = 'https://www.baidu.com'
url = 'https://headline.taobao.com/feed/feedList.htm'
driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
# 截获请求数据
hook_resource_requested_js = '''
var page = this;
page.onResourceRequested = function(requestData, networkRequest) {
    // console.log('Request (#' + requestData.id + '): ' + JSON.stringify(requestData));
    var match = requestData.url.match(/wordfamily.js/g);
    if (match != null) {
        console.log('Request (#' + requestData.id + '): ' + JSON.stringify(requestData));
        
        // newWordFamily.js is an alternative implementation of wordFamily.js
        // and is available in local path
        networkRequest.changeUrl('newWordFamily.js'); 
    }
};
'''
# 截获应答数据
hook_resource_received_js = '''
var page = this;
page.onResourceReceived = function(response) {
    try{
        // console.log('Response (#' + response.id + ', stage "' + response.stage + '"): ' + JSON.stringify(response));
        console.log(requestData.url)
        var match = requestData.url.match(/feedQuery/g);
        console.log(match)
        if(match != null){
            console.log('1111')
            console.log('Request (#' + requestData.id + '): ' + JSON.stringify(requestData));
        }else{
            pass
        }
    }catch(err){
        pass
    }
};
'''
driver.execute('executePhantomScript', {'script': hook_resource_received_js, 'args': []})
driver.get(url=url)

del driver

"""
# 截获请求数据
The requestData metadata object contains these properties:
    id : the number of the requested resource
    method : http method
    url : the URL of the requested resource
    time : Date object containing the date of the request
    headers : list of http headers
    The networkRequest object contains these functions:
    
    abort() : aborts the current network request. Aborting the current network request will invoke onResourceError callback.
    changeUrl(newUrl) : changes the current URL of the network request. By calling networkRequest.changeUrl(newUrl), we can change the request url to the new url. This is an excellent and only way to provide alternative implementation of a remote resource. (see Example-2)
    setHeader(key, value)

# 截获应答数据
The response metadata object contains these properties:
    id : the number of the requested resource
    url : the URL of the requested resource
    time : Date object containing the date of the response
    headers : list of http headers
    bodySize : size of the received content decompressed (entire content or chunk content)
    contentType : the content type if specified
    redirectURL : if there is a redirection, the redirected URL
    stage : “start”, “end” (FIXME: other value for intermediate chunk?)
    status : http status code. ex: 200
    statusText : http status text. ex: OK
"""