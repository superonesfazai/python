# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

from requests import session
from urllib.parse import quote

from fzutils.ip_pools import IpPools
from fzutils.spider.async_always import *

def get_random_proxy() -> tuple:
    proxy = IpPools()._get_random_proxy_ip()
    assert not isinstance(proxy, bool), '获取代理失败!'
    try:
        proxy_host = re.compile('://(.*?):').findall(proxy)[0]
        proxy_port = re.compile('://.*?:(\d+)').findall(proxy)[0]
        # print(proxy_host, proxy_port)
    except IndexError:
        raise IndexError('解析proxy时索引异常!')

    return proxy_host, proxy_port

proxy_host, proxy_port = get_random_proxy()
lua_code = '''
function main(splash, args)
    splash:on_request(function(request)
        request:set_proxy{
            host=\"%(proxy_host)s\",
            port=%(proxy_port)s,
            username=\"%(proxy_username)s\",
            password=\"%(proxy_pwd)s\",
        }
    end)
    -- 异步
    local ok, result = splash:with_timeout(function()
        splash:wait(1.5)
        assert(splash:http_get(\"%(target_url)s\"))
    end, %(timeout)s)
    
    return {
        html=splash:html(),
    }
end
''' % {
    'proxy_host': proxy_host,
    'proxy_port': proxy_port,
    'proxy_username': '',
    'proxy_pwd': '',
    'target_url': 'https://www.baidu.com',
    'timeout': 10,
}
print(lua_code)

url = 'http://localhost:8050/execute?lua_source=' + quote(lua_code)
with session() as s:
    with s.request(method='get', url=url) as resp:
        print(json_2_dict(resp.text))