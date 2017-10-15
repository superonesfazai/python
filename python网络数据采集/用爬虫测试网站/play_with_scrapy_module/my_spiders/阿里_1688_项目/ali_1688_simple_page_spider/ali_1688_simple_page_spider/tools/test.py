# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/10 13:00
@connect : superonesfazai@gmail.com
'''

# 测试还原网址
from urllib.parse import unquote
import re
from pprint import pprint
import requests
import json

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding:': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'm.weibo.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}

cookies = {
    'CNZZDATA1253659577': '786969036-1507603880-%7C1507675639',
    'JSESSIONID': '8L78u3jv1-k4SYnlvV0LpqpGN70A-PNGddXQ-UarP',
    'LoginUmid': '"3Gp8iah%2F14EIs4b5sIVUyK3juRK3iiENwd0In5yCmXlHKPcCw7TGng%3D%3D"',
    'UM_distinctid': '15f044a495bcc-0354a6150865ee-31657c00-fa000-15f044a495c9b8',
    '__cn_logon__': 'true',
    '__cn_logon_id__': '%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA',
    '__last_loginid__': '"%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA"',
    '_cn_slid_': '"eEqvacXW%2FQ"',
    '_csrf_token': '1507647848773',
    '_nk_': 'NhOVmlLYn22Ov9IJnn3S0Tqw6USkkqX2',
    '_tb_token_': '50157dce50c8b',
    '_tmp_ck_0': '"1bobU%2FQQBazWq9KhE%2BxkP3OXnus7BfMzR4Qw%2BwZxclCIXwsqXqfflFnBTUFwF4dJfmcrGLfJ7Kc60FklwaLLmxo9yJ3DVNnCE3BokxfGZbc242%2BEkyvV3dx3drM%2F92BxlFhI8RLWLv0mL6H3xmabRsUibRgABUwGIZUmRZZwG2D92UVUUe6iM8nEMfvnSVsRBKVn2rJWs6nPgAz47Iezk1VyQYHjBw44KZjgwPjPDS%2FYbmOKP6Hw%2B5UWQqCBD6w7RYzdwt2TAzl8gSrZu3GN4o2%2FVL7W7G52Qzm3XdI4IdttRdNDyaeUTwapXuzTQJ7HDhqxEItDGXPBz6qaMHcPIpvLN9iVbbya78ThBrH3Kg02wZSHOWNSoEfmwFozvxMzax9g03kA5rsonWI6ctxHHM1eXSzj%2FKSOb3S5BPZl%2FZ6y0PYE0UyufDTbYomf6h%2F9pCikMTYvee5PxkeZ5AQqgoZbcehgOX06Eq%2B8R%2BBM%2BZOt4SHGpvcoG9JEz3%2Fdc4Yd1tRxiKACBK%2FNkgsKAolz5Q4Un0EdBUUh"',
    '_uab_collina': '150760550070324942244726',
    '_umdata': '85957DF9A4B3B3E86E12BBB8FE63C0081D64AE1805F13C65ED7DA1D2A0053FAE32B67FF65DEB420ACD43AD3E795C914C8E827AB9F2B91EED4B24459DE3CB643B',
    'ad_prefer': '"2017/10/10 12:47:15"',
    'ali_ab': '113.215.177.167.1507605865937.5',
    'ali_apache_track': '"c_ms',
    'ali_apache_tracktmp': '"c_w_signed',
    'alicnweb': 'touch_tb_at%3D1507675371593%7Clastlogonid%3D%25E6%2588%2591%25E6%2598%25AF%25E5%25B7%25A5%25E5%258F%25B79527%25E6%259C%25AC%25E4%25BA%25BA',
    'cn_tmp': '"Z28mC+GqtZ2INLnWg2jSa2e3CGk80yHNd0P50kQ54H1LE3aoyIbBLInC65atnrS47Cm8qnjwqH8NnvM/L/PL3M3ckvhJcfAbNgV3+US7GrtkOzFLC/CSF4++rSxHK6Fo/jTlmfORMg2Q79Fnu8gEiBzs0k3Pd5EhGJ7VfNBsq1RzzEGZp0FlxAYus1RNoFYl9hk9857Faqlf1S93Iva1u/2uC+lMOjQAZ3Vhyytvl+8UWn5mTuqIJxD7nt6cWDYx"',
    'cna': 'K15iEs43VRgCAXyga5ql43kH',
    'cookie2': '1aab948501559f4b3605eed3c3111dc8',
    'isg': 'AuXl0CwS0DkJpTTkYfflrM3f9KezMpn4xdsgSOfKnJwr_gVwr3KphHOe_lRz',
    'last_mid': 'b2b-2242024317',
    't': 'de28003d0ed0d8fe9267742728fa8a56',
    'tbsnid': 'ME9H9ciGVM0gMy572a3vcZazHoeE%2FfhTv2%2BcQQ0LQNQ6sOlEpJKl9g%3D%3D',
    'userID': '"0eSDLTAmofsL67RXnSBAFwkwpsuwsEP%2BAU5n2L44pVU6sOlEpJKl9g%3D%3D"',
    'userIDNum': 'JG1hTHTu5MzRqUsxcJimIg%3D%3D'
}


# url = 'https://login.1688.com/member/jump.htm?target=https%3A%2F%2Flogin.1688.com%2Fmember%2FmarketSigninJump.htm%3FDone%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688'
# url = 'http%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688'
# print(unquote(url))

# https://login.1688.com/member/jump.htm?target=https://login.1688.com/member/marketSigninJump.htm?Done=

a = '<img src="//img.alicdn.com/tfscom/TB11tpQk3oQMeJjy0Fowu3ShVXa.png"/>'
tmp = re.compile(r'<img src=\"(.*?)\"\/>').findall(a)[0]
print(tmp)

print('-' * 100)

# url = 'https://laputa.1688.com/offer/ajax/widgetList.do?callback=jQuery17206144434704995889_1507648557637&blocks=&data=offerdetail_ditto_title%2Cofferdetail_common_report%2Cofferdetail_ditto_serviceDesc%2Cofferdetail_ditto_preferential%2Cofferdetail_ditto_postage%2Cofferdetail_ditto_offerSatisfaction%2Cofferdetail_w1190_guarantee%2Cofferdetail_w1190_tradeWay%2Cofferdetail_w1190_samplePromotion&offerId=556500145489&pageId=laputa20140721212446'
url = 'https://laputa.1688.com/offer/ajax/widgetList.do?callback=jQuery172024277864202167332_1507648647184&blocks=&data=offerdetail_ditto_title%2Cofferdetail_common_report%2Cofferdetail_ditto_serviceDesc%2Cofferdetail_ditto_preferential%2Cofferdetail_ditto_postage%2Cofferdetail_ditto_offerSatisfaction%2Cofferdetail_w1190_guarantee%2Cofferdetail_w1190_tradeWay%2Cofferdetail_w1190_samplePromotion&offerId=526362847506&pageId=laputa20140721212446'
response = requests.get(url).content.decode('gbk')
# print(response)
# data = re.compile(r'jQuery17203296817124306102_1507628878836\((.*?)\)').findall(response)[0]
data = re.compile(r'.*?\((.*?)\)').findall(response)[0]
data = json.loads(data)['data']['data']
data['offerdetail_ditto_preferential'] = ''
# pprint(data)

print('-' * 100)

# detail_url = data['offerdetail_ditto_postage']['offerExtends']['detail_url']
# detail_response = requests.get(detail_url).content.decode('gbk')
# pprint(detail_response)
# detail_data = re.compile(r'var offer_details=(.*?);').findall(detail_response)[0].replace('\\', '')
# print(detail_data)
# detail_data = json.loads(detail_data)['content']
# pprint(detail_url)
# 起送数量及价格  offerdetail_ditto_postage  beginAmount起送件数  price对应价格
# 图片链接在  offerdetail_ditto_postage  offerExtends
# pprint(data_json)

# https://order.1688.com/order/smart_make_order.htm?cssUrl=&isOfferSupportOnlineTrade=True&isUseFlow=True&offerId=556500145489&showType=type-1

login_cookies = [{'domain': '.1688.com', 'expiry': 1523230683, 'httpOnly': False, 'name': 'isg', 'path': '/', 'secure': False, 'value': 'AsvLHqNbFk8Qf0qbdCMOzK2vWmm1YN_if3n-1j3Ip4phXOu-xTBvMml_QCtI'}, {'domain': '.1688.com', 'expiry': 2524579200, 'httpOnly': False, 'name': 'alicnweb', 'path': '/', 'secure': False, 'value': 'lastlogonid%3D%25E6%2588%2591%25E6%2598%25AF%25E5%25B7%25A5%25E5%258F%25B79527%25E6%259C%25AC%25E4%25BA%25BA%7Ctouch_tb_at%3D1507678682369'}, {'domain': '.1688.com', 'expiry': 1507685880.913939, 'httpOnly': False, 'name': '_show_user_unbind_div_', 'path': '/', 'secure': False, 'value': 'b2b-2242024317_false'}, {'domain': '.1688.com', 'expiry': 1507685880.912297, 'httpOnly': False, 'name': '_show_force_unbind_div_', 'path': '/', 'secure': False, 'value': 'b2b-2242024317_false'}, {'domain': '.1688.com', 'expiry': 1523403479, 'httpOnly': False, 'name': 'UM_distinctid', 'path': '/', 'secure': False, 'value': '15f08a6f17c32c-00b407851abae2-31657c00-fa000-15f08a6f17d6cb'}, {'domain': '.1688.com', 'httpOnly': False, 'name': '_nk_', 'path': '/', 'secure': False, 'value': 'NhOVmlLYn22Ov9IJnn3S0Tqw6USkkqX2'}, {'domain': '.1688.com', 'expiry': 2138398679, 'httpOnly': False, 'name': 'cna', 'path': '/', 'secure': False, 'value': 'yUdkEjFwFXoCAXyga5oQQ169'}, {'domain': '.work.1688.com', 'expiry': 1507765078.989422, 'httpOnly': False, 'name': 'landingPage', 'path': '/', 'secure': False, 'value': 'home'}, {'domain': '.1688.com', 'httpOnly': False, 'name': 'userIDNum', 'path': '/', 'secure': False, 'value': 'JG1hTHTu5MzRqUsxcJimIg%3D%3D'}, {'domain': '.1688.com', 'httpOnly': False, 'name': 'login', 'path': '/', 'secure': False, 'value': '"kFeyVBJLQQI%3D"'}, {'domain': '.1688.com', 'expiry': 1539214678.468795, 'httpOnly': False, 'name': '__last_loginid__', 'path': '/', 'secure': False, 'value': '"%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA"'}, {'domain': '.1688.com', 'expiry': 1539214678.468468, 'httpOnly': False, 'name': 'last_mid', 'path': '/', 'secure': False, 'value': 'b2b-2242024317'}, {'domain': '.1688.com', 'expiry': 1507685881.047296, 'httpOnly': False, 'name': '__rn_alert__', 'path': '/', 'secure': False, 'value': 'false'}, {'domain': '.1688.com', 'expiry': 1507685880.913153, 'httpOnly': False, 'name': '_show_sys_unbind_div_', 'path': '/', 'secure': False, 'value': 'b2b-2242024317_false'}, {'domain': '.1688.com', 'expiry': 1507685880.697289, 'httpOnly': False, 'name': '_is_show_loginId_change_block_', 'path': '/', 'secure': False, 'value': 'b2b-2242024317_false'}, {'domain': '.1688.com', 'httpOnly': True, 'name': 'tbsnid', 'path': '/', 'secure': False, 'value': 'DnUMHgFCdFaoziLBVBtc01v1JV3lIoJHm0UzfQedzJ46sOlEpJKl9g%3D%3D'}, {'domain': '.1688.com', 'httpOnly': False, 'name': '_csrf_token', 'path': '/', 'secure': False, 'value': '1507678679868'}, {'domain': '.1688.com', 'httpOnly': True, 'name': 'cookie1', 'path': '/', 'secure': False, 'value': 'UR3Wq2iKhDJHTTOd%2FGn4oh0oxwBK8EUqK%2Bm%2Bxv62FEM%3D'}, {'domain': '.1688.com', 'expiry': 1539214678.467922, 'httpOnly': False, 'name': '_cn_slid_', 'path': '/', 'secure': False, 'value': '"eEqvacXW%2FQ"'}, {'domain': '.1688.com', 'httpOnly': True, 'name': 'unb', 'path': '/', 'secure': False, 'value': '2242024317'}, {'domain': '.1688.com', 'httpOnly': False, 'name': 'sg', 'path': '/', 'secure': False, 'value': '%E4%BA%BA73'}, {'domain': '.1688.com', 'httpOnly': False, 'name': '__cn_logon_id__', 'path': '/', 'secure': False, 'value': '%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA'}, {'domain': '.1688.com', 'httpOnly': False, 'name': 'LoginUmid', 'path': '/', 'secure': False, 'value': '"uoPP%2FwcICEU%2BvCOLbNBazma7%2F95UnztUcfOUw5NS2ZHmkdAiNY8Cqw%3D%3D"'}, {'domain': '.1688.com', 'httpOnly': False, 'name': 't', 'path': '/', 'secure': False, 'value': 'b7ef169ba16adc7e3567351f57130498'}, {'domain': '.1688.com', 'httpOnly': False, 'name': 'JSESSIONID', 'path': '/', 'secure': False, 'value': '8L78QCuu1-1lRYO2905I0gxTCxDB-qe5KhXQ-bBRv'}, {'domain': '.1688.com', 'httpOnly': False, 'name': 'ali_apache_tracktmp', 'path': '/', 'secure': False, 'value': '"c_w_signed=Y"'}, {'domain': 'work.1688.com', 'expiry': 1523403479, 'httpOnly': False, 'name': 'CNZZDATA1253645563', 'path': '/', 'secure': False, 'value': '362945326-1507676060-%7C1507676060'}, {'domain': '.1688.com', 'httpOnly': False, 'name': 'userID', 'path': '/', 'secure': False, 'value': '"0eSDLTAmofsL67RXnSBAFwkwpsuwsEP%2BAU5n2L44pVU6sOlEpJKl9g%3D%3D"'}, {'domain': '.1688.com', 'httpOnly': True, 'name': 'cn_tmp', 'path': '/', 'secure': False, 'value': '"Z28mC+GqtZ2INLnWg2jSa2e3CGk80yHNd0P50kQ54H1LE3aoyIbBLInC65atnrS47Cm8qnjwqH8NnvM/L/PL3M3ckvhJcfAb57d58fb1u+9Xb5NUYrsDEp/P+6ne6dJqvPFz2jGBGW9XDNWtPSX+xjSJUMFTvXcKwE77M2WASUoL6Su4/MtxGue4xaM9ThXMcVZnbDz8Uzh2wxEOgvBjdSXRDO2FUeqaQvXvnQzBaib+ut0BP5v/0OMViZmFdvYw"'}, {'domain': '.1688.com', 'expiry': 1823038681.252842, 'httpOnly': False, 'name': 'ali_ab', 'path': '/', 'secure': False, 'value': '124.160.107.154.1507678682402.6'}, {'domain': '.1688.com', 'httpOnly': True, 'name': 'cookie2', 'path': '/', 'secure': False, 'value': '1f353ea59dc373c059567da20862335c'}, {'domain': '.1688.com', 'httpOnly': False, 'name': '_tmp_ck_0', 'path': '/', 'secure': False, 'value': '"p4QP8IN8C6XZJfIFreKiqdwVXZ4iVJjCdI20o%2BA%2FFw6Hww7SQb%2BEYwLsxOXADgWhYft%2FXASHqTrdQTC45LnmkaYws1ghtYMXPud4LRWR1SzrZrXtZeHVEZFG%2Bh4yUQsE7197RqApVohf1zQ4A6i1tIXWWznYQ96bAi%2BUthfmewXpv10cbTRu5fHhDHJB1K8G3gZeedvcGP%2Bp1iojGPY3uYpV7qouuhtsFPcI4UrbD7FDFCGA9tzbtvkyAvyMaVnSFDxqNs5sDXpGOKPlFBEjyHLPKogcz8mUXohpKGaEcFJZjvXScaLxu3ZxW%2Fpsz9FpdSHWvSJzJGJKrQSiMHQnNpR3KkkwU%2FUWH3ht5vQvKbJCHzwmFPUi1C8jLPkgmPj4Vqv%2F4ROttOPIsxq484Kwa0T%2Fm90pIPmON2Yy3SOxFnoeWxmFmL4bTcLHED1XCI1lwgxq6KLtxftOcNhnKBVkw7mMqLU2b7dpZ8PuNj5usBRK25rFc210cZ%2Fs26au97KdNnjHBr%2FJxOCcr8%2FTQlT5HG760c%2FEvxgoA1DeqstU%2B%2BA%3D"'}, {'domain': '.1688.com', 'expiry': 1607678677.467805, 'httpOnly': False, 'name': 'ali_apache_track', 'path': '/', 'secure': False, 'value': '"c_ms=1|c_mid=b2b-2242024317|c_lid=%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA"'}, {'domain': '.1688.com', 'httpOnly': False, 'name': '_tb_token_', 'path': '/', 'secure': False, 'value': '33ee31ee56164'}, {'domain': '.1688.com', 'httpOnly': False, 'name': '__cn_logon__', 'path': '/', 'secure': False, 'value': 'true'}, {'domain': '.1688.com', 'httpOnly': True, 'name': 'cookie17', 'path': '/', 'secure': False, 'value': 'UUplY9Ft9xwldQ%3D%3D'}]

def get_qrcode_cookies(login_cookies):
    cookies = {}
    tmp_key = ''
    tmp_value = ''
    for item in login_cookies:
        for key in item.keys():
            if 'name' == key:
                # print(item[key])
                tmp_key = item[key]
            if 'value' == key:
                tmp_value = item[key]

            if tmp_key != '' and tmp_value != '':
                cookies[tmp_key] = tmp_value
    return cookies

def cookies_to_str(cookies):
    cookie = [str(key) + "=" + str(value) for key, value in cookies.items()]
    # print cookie

    cookiestr = ';'.join(item for item in cookie)
    return cookiestr

cookies = get_qrcode_cookies(login_cookies)
cookies_str = cookies_to_str(cookies)
print(cookies_str)

print('-' * 100)

dd_url = 'https://order.1688.com/order/smart_make_order.htm'
dd = requests.get(dd_url, headers=headers, cookies=cookies)
# print(dd.content.decode('gbk'))