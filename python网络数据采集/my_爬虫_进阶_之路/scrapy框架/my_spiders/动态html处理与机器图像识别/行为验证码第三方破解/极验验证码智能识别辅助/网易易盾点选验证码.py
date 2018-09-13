# coding:utf-8

'''
@author = super_fazai
@File    : 网易易盾点选验证码.py
@connect : superonesfazai@gmail.com
'''

from urllib.parse import unquote
from fzutils.common_utils import json_2_dict
from fzutils.spider.fz_requests import Requests
from fzutils.internet_utils import get_random_pc_ua

id = '1f6f8f8dc15b4f378c3134eec0c5f564'     # id是固定的值
referer = 'http://120.26.119.135/Login.aspx'
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
    def crack_wy_text_captcha():
        '''
        获取第三方validate
        :return:
        '''
        url = 'http://wyydapi.c2567.com:10001/wyyd/shibie'
        params = (
            ('username', username),
            ('password', pwd),
            ('id', id),
            ('referer', referer),
            ('supportclick', ''),  # 内置汉字点选, 无需第三方点选, 如需点选下方设置三方打码
            ('supportuser', ''),  # 打码平台账号
            ('supportpass', ''),  # 打码平台pwd
        )
        body = Requests.get_url_body(url=url, use_proxy=False, params=params)
        # print(body)
        res = json_2_dict(body)
        status = res.get('status', 'fail')
        validate = ''
        if status == 'ok':
            validate = res.get('validate', '')

        return validate

    cookies = {
        '_9755xjdesxxd_': '32',
        'gdxidpyhxdE': 'gjKCnDWASVwyJpOSGKLIaqHXYt0Qjq7Ycs7JzzLNWoZV2S%5CTam6fybIabIljeoL4JpfrI%2Bl6Xp9wLy5bHanMUDVPQdC3%2B3ihW%2BrP1cH6ktTTEvKfaPLQSHkkL5Wn7BpLALiek4J2Bq9nan1om%2B8dA%2FYyoxxDwX7vLusi5dLf%2Bni%2Fyrot%3A1536833525662',
    }
    validate = crack_wy_text_captcha()
    validate = '' if validate == '' else unquote(validate)
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
    url = 'http://120.26.119.135/Login.aspx'
    body = Requests.get_url_body(method='post', url=url, headers=headers, cookies=cookies, data=data, use_proxy=False)
    print(body)

    return body

bg_username = ''
bg_pwd = ''
bg_login(bg_username, bg_pwd)