# coding:utf-8

'''
@author = super_fazai
@File    : 网易易盾点选验证码.py
@connect : superonesfazai@gmail.com
'''

from fzutils.common_utils import json_2_dict
from fzutils.spider.fz_requests import Requests
from fzutils.internet_utils import get_random_pc_ua
from fzutils.ocr_utils import crack_wy_point_select_captcha
from fzutils.url_utils import unquote_plus

id = '1f6f8f8dc15b4f378c3134eec0c5f564'     # id是固定的值
referer = 'http://admin.k85u.com/index.aspx'
with open('/Users/afa/myFiles/pwd/act_captcha_helper_pwd.json', 'r') as f:
    helper_info = json_2_dict(f.read())

with open('/Users/afa/myFiles/pwd/ruokuai_pwd.json', 'r') as f:
    ruokuai_info = json_2_dict(f.read())

username = helper_info['username']
pwd = helper_info['pwd']

r_username = ruokuai_info['username']
r_pwd = ruokuai_info['pwd']

def bg_login(bg_username, bg_pwd):
    '''
    后台login
    :param validate:
    :return:
    '''
    cookies = {
        '_9755xjdesxxd_': '32',
        'gdxidpyhxdE': 'gjKCnDWASVwyJpOSGKLIaqHXYt0Qjq7Ycs7JzzLNWoZV2S%5CTam6fybIabIljeoL4JpfrI%2Bl6Xp9wLy5bHanMUDVPQdC3%2B3ihW%2BrP1cH6ktTTEvKfaPLQSHkkL5Wn7BpLALiek4J2Bq9nan1om%2B8dA%2FYyoxxDwX7vLusi5dLf%2Bni%2Fyrot%3A1536833525662',
    }
    validate = crack_wy_point_select_captcha(
        username=username,
        pwd=pwd,
        id=id,
        referer=referer)
    validate = '' if validate == '' else unquote_plus(validate)
    print('获取到的validate:{}'.format(validate))
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Origin': 'http://120.26.119.135',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': get_random_pc_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://120.26.119.135/Login.aspx',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    data = {
        '__VIEWSTATE': '/wEPDwUKLTUwOTQ0NDQ3MWRk/ffecNvOMZIyPoiGxLPop3/5ERoE5/VlszxMMNbpijg=',
        '__VIEWSTATEGENERATOR': 'C2EE9ABB',
        'txtUserName': bg_username,
        'txtPwd': bg_pwd,
        # 验证码认证str
        # 'NECaptchaValidate': 'jrhSRTTEM4fZR9oXGRxtC4oiups4od-qu7zvHUkrheMvtGBDV-UPUNmpcigljb2adxT.49aFGB6.Ez2EfgTbMvjMLp54AF9KAmfNAjVoN7.UWqxQac6zbtrU-nWbFc-22a_E85FotOmPBIQFb1U68mRGd0.xBv_N5BIqAFqi495WKS0XQwyQE7frGovtg0OQoah9eXFaLall-rRlaWQrHe6ifSAGnCrLYpfU7P1W561gIUssJJ0Jfs_BGSQshsQ_XivpGyt84K9ISOTijZ45h1NQbaSwupv_EGXSgkXv4T8gnJHao1E9d5e7rqeGw_YgYLQiEzhm1.uuG2xQVPPdYbYVdk0kbQDyTDTTfyMrVkfMdwnjh.XupVrShm1vEPI9YHJGFuh.GwezkeQJCLb1BwbJ_gXPLE9evLEUGa.R4mvLZuxjkzS28qksNpyzFSs0NDobMc18Y81Vr_XiRZu.mGCmfemIE.yWSmgNnPpS.IbY6w6laJkEF1oT5sI3',
        'NECaptchaValidate': validate,
        'btnLogin': '登    录',
    }
    url = 'http://admin.k85u.com/index.aspx'
    body = Requests.get_url_body(method='post', url=url, headers=headers, cookies=cookies, data=data, use_proxy=False)
    print(body)

    return body

bg_username = ''
bg_pwd = ''
bg_login(bg_username, bg_pwd)