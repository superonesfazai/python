# coding:utf-8

'''
@author = super_fazai
@File    : 每日幸运大转盘.py
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

cookies = {'CNZZDATA1253659577': '1148026705-1508656403-null%7C1508742803',
 'JSESSIONID': 'yS3Zvub-uxYYgD3TCXFcjTKID5-V4XdlYQ-Zmb',
 'LoginUmid': '"uoPP%2FwcICEU%2BvCOLbNBazma7%2F95UnztUcfOUw5NS2ZHmkdAiNY8Cqw%3D%3D"',
 'UM_distinctid': '15f430e953225c-0995179d5e4ade-31657c00-fa000-15f430e95334e1',
 '__cn_logon__': 'true',
 '__cn_logon_id__': '%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA',
 '__last_loginid__': '"%E6%88%91%E6%98%AF%E5%B7%A5%E5%8F%B79527%E6%9C%AC%E4%BA%BA"',
 '__rn_alert__': 'false',
 '_cn_slid_': '"eEqvacXW%2FQ"',
 '_csrf_token': '1508743237918',
 '_is_show_loginId_change_block_': 'b2b-2242024317_false',
 '_nk_': 'NhOVmlLYn22Ov9IJnn3S0Tqw6USkkqX2',
 '_show_force_unbind_div_': 'b2b-2242024317_false',
 '_show_sys_unbind_div_': 'b2b-2242024317_false',
 '_show_user_unbind_div_': 'b2b-2242024317_false',
 '_tb_token_': 'e3e6e76303e81',
 '_tmp_ck_0': '"HYP1z9lZIkgNFcWPRAlCNdNqD96zipOUNBWMlwWtrc1m075Ap6h2JgvHpx%2BqvEw4SuxRSoXXVMBZJz4wPEJt7GlbDClwiHq4bxpcaBxdDIfV3iYR2Y3l4rDH5rAMutV%2BA0qINBMfSTKKjSJw2QmRiYlGWFDLlkpPf2ol2y8nyJ3bg4635veAsyofRs40D2up7Kzo7n%2FpQco3UNFkYhKkbUXMcKxhyjk1GSRltfPJpvsrQNHdEMjHKAd4CY3%2Byfc1DbhuDRcWdl%2BztGo4tfT6x47Bc%2BVIkVFvb0lVhEKn0e0oB8JZaJi84mWsmL%2FSg5mVjHcuP2%2FRmvGI7zLuHtORdZPuXufa75gEiB%2Frgh3BkhXwcHNuGZogO7xqUNCrulcfNcFIAUqn2%2BIiCPnLruyWpooyJi%2B0G0OdMRXIdFAue%2By8ERTdmY7Q1gJTLHC5NeU49vX7NAOy01gKqEcUi3qfYl2vuBBpIgzdBLT4K1auf5vEioM2kYlwq0aZ7N2VLPW8dYjCP7%2Bm1CvUTSHHExF%2FhRsUoydUjQwa"',
 '_uab_collina': '150865866624817348375888',
 '_umdata': '55F3A8BFC9C50DDA5A9113682A1E2B5E3A0F7BE3E5975FD935A9BB9BF81F537B37E54122A90113A9CD43AD3E795C914CDDC048A671562E32B38D9FE9E8361227',
 'ad_prefer': '"2017/10/22 16:51:13"',
 'ali_ab': '218.108.97.82.1508658639482.0',
 'ali_apache_track': '"c_ms',
 'ali_apache_tracktmp': '"c_w_signed',
 'alicnweb': 'touch_tb_at%3D1508741818652',
 'cn_tmp': '"Z28mC+GqtZ2INLnWg2jSa2e3CGk80yHNd0P50kQ54H1LE3aoyIbBLInC65atnrS47Cm8qnjwqH8NnvM/L/PL3M3ckvhJcfAbSClVCF95xpX5gZHXUJezyLTpxmALODaSB3xuPedti9ekkGfpeJZ0cNJvXRMPjqzybzbivF89XTkz0ptY+votZaNSBgGskzxVQfB7faJuuUiGOF8xTOCElWTWZT8nkIPz06suCmcy5BvYKfDEY4zEvX+v2pSeyuvJ"',
 'cna': 'djtzEjGArAoCAdpsYVInKSbN',
 'cookie1': 'UR3Wq2iKhDJHTTOd%2FGn4oh0oxwBK8EUqK%2Bm%2Bxv62FEM%3D',
 'cookie17': 'UUplY9Ft9xwldQ%3D%3D',
 'cookie2': '1d7f072008e7b4382f4de1c39715c413',
 'h_keys': '"%u4e0b%u67b6"',
 'hng': 'CN%7Czh-CN%7CCNY%7C156',
 'isg': 'Al5e5W8Qi2R8Ht-GGJxz3EA5r_JgtyPmku6LPQjnyKGcK_4Fca9yqYTJVQHc',
 'last_mid': 'b2b-2242024317',
 'login': '"kFeyVBJLQQI%3D"',
 'sg': '%E4%BA%BA73',
 't': '39c31685a5f4ebc8b58fb9f880a2c9e9',
 'tbsnid': 'gmYiKIGv7Mf%2B7J6E%2B1Zn89pjrLzx15zALQxPUPhDotY6sOlEpJKl9g%3D%3D',
 'unb': '2242024317',
 'userID': '"0eSDLTAmofsL67RXnSBAFwkwpsuwsEP%2BAU5n2L44pVU6sOlEpJKl9g%3D%3D"',
 'userIDNum': 'JG1hTHTu5MzRqUsxcJimIg%3D%3D'}


# url = 'https://login.1688.com/member/jump.htm?target=https%3A%2F%2Flogin.1688.com%2Fmember%2FmarketSigninJump.htm%3FDone%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688'
# url = 'http%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688'
# print(unquote(url))

# https://login.1688.com/member/jump.htm?target=https://login.1688.com/member/marketSigninJump.htm?Done=

a = '<img src="//img.alicdn.com/tfscom/TB11tpQk3oQMeJjy0Fowu3ShVXa.png"/>'
tmp = re.compile(r'<img src=\"(.*?)\"\/>').findall(a)[0]
print(tmp)

print('-' * 100)

# url = 'https://laputa.1688.com/offer/ajax/widgetList.do?callback=jQuery17206144434704995889_1507648557637&blocks=&data=offerdetail_ditto_title%2Cofferdetail_common_report%2Cofferdetail_ditto_serviceDesc%2Cofferdetail_ditto_preferential%2Cofferdetail_ditto_postage%2Cofferdetail_ditto_offerSatisfaction%2Cofferdetail_w1190_guarantee%2Cofferdetail_w1190_tradeWay%2Cofferdetail_w1190_samplePromotion&offerId=556500145489&pageId=laputa20140721212446'
url = 'https://laputa.1688.com/offer/ajax/widgetList.do?callback=jQuery17205927115502308771_1508742206359&blocks=&data=offerdetail_ditto_title%2Cofferdetail_common_report%2Cofferdetail_ditto_serviceDesc%2Cofferdetail_ditto_preferential%2Cofferdetail_ditto_postage%2Cofferdetail_ditto_offerSatisfaction%2Cofferdetail_w1190_guarantee%2Cofferdetail_w1190_tradeWay%2Cofferdetail_w1190_samplePromotion&offerId=559526148757&pageId=laputa20140721212446'
response = requests.get(url).content.decode('gbk')
# print(response)
data = re.compile(r'.*?\((.*?)\)').findall(response)[0]
data = json.loads(data)['data']['data']
# data = json.loads(data)['data']['data']
data['offerdetail_ditto_preferential'] = ''
pprint(data)

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