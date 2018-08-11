# coding:utf-8

'''
@author = super_fazai
@File    : 通过post表单模拟登录taobao.py
@Time    : 2018/4/15 10:21
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')


import json
from urllib.parse import urlencode
from urllib.request import ProxyHandler, HTTPCookieProcessor
from urllib.request import HTTPHandler
from urllib.request import build_opener
from urllib.request import Request
# import cookielib
from http.cookiejar import LWPCookieJar
import re
import webbrowser
from random import randint
import requests

from fzutils.internet_utils import get_random_pc_ua
from fzutils.spider.fz_requests import MyRequests

#模拟登录淘宝类
class Taobao:
    #初始化方法
    def __init__(self):
        #登录的URL
        self.loginURL = "https://login.taobao.com/member/login.jhtml"
        #代理IP地址，防止自己的IP被封禁
        # self.proxyURL = 'http://120.193.146.97:843'
        self.proxyURL = 'http://' + MyRequests._get_proxies()['http']

        #登录POST数据时发送的头部信息
        self.loginHeaders =  {
            'Host':'login.taobao.com',
            'User-Agent' : get_random_pc_ua(),
            'Referer' : 'https://login.taobao.com/member/login.jhtml',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection' : 'Keep-Alive'
        }
        self.headers = {
            '': 'path: /login.htm?_input_charset=utf-8&ttid=h5%40iframe',
            'content-length': '3015',
            'cache-control': 'max-age=0',
            'origin': 'https://login.m.taobao.com',
            'upgrade-insecure-requests': '1',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'referer': 'https://login.m.taobao.com/login.htm?from=sm&ttid=h5@iframe&tpl_redirect_url=https%3A%2F%2Fsec.taobao.com%2Fquery.htm%3Faction%3DQueryAction%26event_submit_do_login%3Dok%26smApp%3Dmalldetailskip%26smPolicy%3Dmalldetailskip-h5-anti_Spider-h5SS-checklogin%26smCharset%3DGBK%26smTag%3DMTgzLjE1OS4xNzcuMTMwLCxiY2Y0NWZkZjVlYmI0ZGE2OTlkZjNkZmUyYTA1ODc4Mg%253D%253D%26captcha%3Dhttps%253A%252F%252Fsec.taobao.com%252Fquery.htm%26smReturn%3Dhttps%253A%252F%252Fdetail.m.tmall.com%252Fitem.htm%253Fid%253D20739535568%26smSign%3DEh51d83i2uzo2b2zGtgKRg%253D%253D',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'isg=BAEBfhDFP4K9JlO2YSgx_sw0EEvbhnVHYzo4S2NWsohnSiMcoH_n8l8IKL4Mug1Y',
        }
        #用户名
        self.username = ''
        #ua字符串，经过淘宝ua算法计算得出，包含了时间戳,浏览器,屏幕分辨率,随机数,鼠标移动,鼠标点击,其实还有键盘输入记录,鼠标移动的记录、点击的记录等等的信息
        self.ua = '107#ssznSzS9s2xAImllPVytXzO1XnIggOmR9LcTi88ngXX9lXFu//94sFxKXrrOg/ZvsLFLTAtXgFXxxXGQ/CxRlaEJXq6nuVE9luz8TdFDyJB+BaUtsYc0P894xppFjjidAOaEIdSveZpfnD1iDG2n7ISDflmisXa8KMKMoU/xPqBLTYtnO8KQVMpYmoBPOShgsCbDNSCXXQGLbLURQXXlDI5M9IjfOd3dPUh9PEUyljo+bL1NmKqXt3/weVQb8v9QkE/6k9DzC5vWQJAec6+1aOnflejd87g7m9jYygKX3ccb1dbwQmh6qYOcuWlw3mQmKlYV2yr7t7xqEmG01vFkqYVr3/Lpu6tg29V22jXmoxcufdUbepynwC/HwUCiCgOKKZCNjE3OCy4bem2r8dEWdr9d3rhGvmt3jpiUK7XJCy4bek5r8dEmdrtGC3iUbfub25COijn8oEkDvpRIdDy/bqy48C+DCf3AiLpng9gn82splff8c6rjantrG/Cf81V6y9FAyii/Xf53Z5Zr0xMzheiteOnGC5FsmE/46EtzI5IZQkAdv7VYrrexvYMzGvQygi+OmTjae5dbF6w0EJjyE8T4lInDXvIvOoVYPyZ7XP1MbY38+FXEEITAla=='
        #密码，，淘宝对此密码进行了加密处理，256位
        self.password2 = '02d12254b4a503974749e4ee16f72e76081dce05e8fe449b487573ba72f14d47f9df56a8377afd48194afa7053aa1829cd9d3a55476a5510128244fea80fbed8a0c798146912122dcce4059be5ba85b39cc7d51fae6629a103d527256a3a48327c6e4cb1350806fa15e9ea07696cdce9c91658718f72b2f325b0d0784730e9fe'
        self.post = {
            'ua':self.ua,
            'TPL_checkcode':'',
            'CtrlVersion': '1,0,0,7',
            'TPL_password':'',
            'TPL_redirect_url':'http://i.taobao.com/my_taobao.htm?nekot=udm8087E1424147022443',
            'TPL_username':self.username,
            'loginsite':'0',
            'newlogin':'0',
            'from':'tb',
            'fc':'default',
            'style':'default',
            'css_style':'',
            'tid':'XOR_1_000000000000000000000000000000_625C4720470A0A050976770A',
            'support':'000001',
            'loginType':'4',
            'minititle':'',
            'minipara':'',
            'umto':'NaN',
            'pstrong':'3',
            'llnick':'',
            'sign':'',
            'need_sign':'',
            'isIgnore':'',
            'full_redirect':'',
            'popid':'',
            'callback':'',
            'guf':'',
            'not_duplite_str':'',
            'need_user_id':'',
            'poy':'',
            'gvfdcname':'10',
            'gvfdcre':'',
            'from_encoding ':'',
            'sub':'',
            'TPL_password_2':self.password2,
            'loginASR':'1',
            'loginASRSuc':'1',
            'allp':'',
            'oslanguage':'zh-CN',
            'sr':'1366*768',
            'osVer':'windows|6.1',
            'naviVer':'firefox|35'
        }
        #将POST的数据进行编码转换
        self.postData = urlencode(self.post)

        #设置代理
        self.proxy = ProxyHandler({'http':self.proxyURL})

        #设置cookie
        self.cookie = LWPCookieJar()

        #设置cookie处理器
        self.cookieHandler = HTTPCookieProcessor(self.cookie)

        #设置登录时用到的opener，它的open方法相当于urllib2.urlopen
        self.opener = build_opener(self.cookieHandler,self.proxy, HTTPHandler)

    #得到是否需要输入验证码，这次请求的相应有时会不同，有时需要验证有时不需要
    def needIdenCode(self):
        #第一次登录获取验证码尝试，构建request
        # request = Request(self.loginURL, self.postData, self.loginHeaders)
        # response = self.opener.open(request)        #得到第一次登录尝试的相应
        # content = response.read().decode('gbk')
        # status = response.getcode()           # 获取状态吗

        response = requests.post(url=self.loginURL, headers=self.loginHeaders, data=json.dumps(self.postData), proxies=MyRequests._get_proxies())
        content = response.content.decode('gbk')

        status = response.status_code

        #状态码为200，获取成功
        if status == 200:
            print("获取请求成功")
            #u8bf7u8f93u5165u9a8cu8bc1u7801这六个字是请输入验证码的utf-8编码
            pattern = re.compile(u'u8bf7u8f93u5165u9a8cu8bc1u7801',re.S)
            result = re.search(pattern,content)
            #如果找到该字符，代表需要输入验证码
            if result:
                print("此次安全验证异常，您需要输入验证码")
                return content
            #否则不需要
            else:
                print("此次安全验证通过，您这次不需要输入验证码")
                return False
        else:
            print("获取请求失败")

    #得到验证码图片
    def getIdenCode(self,page):
        #得到验证码的图片
        pattern = re.compile('<img id="J_StandardCode_m.*?data-src="(.*?)"',re.S)
        #匹配的结果
        matchResult = re.search(pattern,page)
        #已经匹配得到内容，并且验证码图片链接不为空
        if matchResult and matchResult.group(1):
            print(matchResult.group(1))
            return matchResult.group(1)
        else:
            print("没有找到验证码内容")
            return False

    #程序运行主干
    def main(self):
        #是否需要验证码，是则得到页面内容，不是则返回False
        needResult = self.needIdenCode()
        if needResult is not False:
            print("您需要手动输入验证码")
            idenCode = self.getIdenCode(needResult)
            #得到了验证码的链接
            if idenCode is not False:
                print("验证码获取成功")
                print("请在浏览器中输入您看到的验证码")
                webbrowser.open_new_tab(idenCode)
            #验证码链接为空，无效验证码
            else:
                print("验证码获取失败，请重试")
        else:
            print("不需要输入验证码")

# taobao = Taobao()
# taobao.main()

import requests

headers = {
    'content-length': '3015',
    'cache-control': 'max-age=0',
    'origin': 'https://login.m.taobao.com',
    'upgrade-insecure-requests': '1',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'referer': 'https://login.m.taobao.com/login.htm?from=sm&ttid=h5@iframe&tpl_redirect_url=https%3A%2F%2Fsec.taobao.com%2Fquery.htm%3Faction%3DQueryAction%26event_submit_do_login%3Dok%26smApp%3Dmalldetailskip%26smPolicy%3Dmalldetailskip-h5-anti_Spider-h5SS-checklogin%26smCharset%3DGBK%26smTag%3DMTgzLjE1OS4xNzcuMTMwLCxiY2Y0NWZkZjVlYmI0ZGE2OTlkZjNkZmUyYTA1ODc4Mg%253D%253D%26captcha%3Dhttps%253A%252F%252Fsec.taobao.com%252Fquery.htm%26smReturn%3Dhttps%253A%252F%252Fdetail.m.tmall.com%252Fitem.htm%253Fid%253D20739535568%26smSign%3DEh51d83i2uzo2b2zGtgKRg%253D%253D',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'isg=BAEBfhDFP4K9JlO2YSgx_sw0EEvbhnVHYzo4S2NWsohnSiMcoH_n8l8IKL4Mug1Y',
}

params = (
    ('_input_charset', 'utf-8'),
    ('ttid', 'h5@iframe'),
)

data = '_tb_token_=5eeeee60a4ae3&ttid=h5%40iframe&action=LoginAction&event_submit_do_login=1&TPL_redirect_url=https%3A%2F%2Fsec.taobao.com%2Fquery.htm%3Faction%3DQueryAction%26event_submit_do_login%3Dok%26smApp%3Dmalldetailskip%26smPolicy%3Dmalldetailskip-h5-anti_Spider-h5SS-checklogin%26smCharset%3DGBK%26smTag%3DMTgzLjE1OS4xNzcuMTMwLCxiY2Y0NWZkZjVlYmI0ZGE2OTlkZjNkZmUyYTA1ODc4Mg%253D%253D%26captcha%3Dhttps%253A%252F%252Fsec.taobao.com%252Fquery.htm%26smReturn%3Dhttps%253A%252F%252Fdetail.m.tmall.com%252Fitem.htm%253Fid%253D20739535568%26smSign%3DEh51d83i2uzo2b2zGtgKRg%253D%253D&loginFrom=WAP_TAOBAO&style=&bind_token=&assets_css=&assets_js=&ssottid=&nv=false&otherLoginUrl=https%3A%2F%2Flogin.m.taobao.com%2Fmsg_login.htm%3Ffrom%3Dsm%26ttid%3Dh5%2540iframe%26tpl_redirect_url%3Dhttps%253A%252F%252Fsec.taobao.com%252Fquery.htm%253Faction%253DQueryAction%2526event_submit_do_login%253Dok%2526smApp%253Dmalldetailskip%2526smPolicy%253Dmalldetailskip-h5-anti_Spider-h5SS-checklogin%2526smCharset%253DGBK%2526smTag%253DMTgzLjE1OS4xNzcuMTMwLCxiY2Y0NWZkZjVlYmI0ZGE2OTlkZjNkZmUyYTA1ODc4Mg%25253D%25253D%2526captcha%253Dhttps%25253A%25252F%25252Fsec.taobao.com%25252Fquery.htm%2526smReturn%253Dhttps%25253A%25252F%25252Fdetail.m.tmall.com%25252Fitem.htm%25253Fid%25253D20739535568%2526smSign%253DEh51d83i2uzo2b2zGtgKRg%25253D%25253D%26redirectURL%3Dhttps%253A%252F%252Fsec.taobao.com%252Fquery.htm%253Faction%253DQueryAction%2526event_submit_do_login%253Dok%2526smApp%253Dmalldetailskip%2526smPolicy%253Dmalldetailskip-h5-anti_Spider-h5SS-checklogin%2526smCharset%253DGBK%2526smTag%253DMTgzLjE1OS4xNzcuMTMwLCxiY2Y0NWZkZjVlYmI0ZGE2OTlkZjNkZmUyYTA1ODc4Mg%25253D%25253D%2526captcha%253Dhttps%25253A%25252F%25252Fsec.taobao.com%25252Fquery.htm%2526smReturn%253Dhttps%25253A%25252F%25252Fdetail.m.tmall.com%25252Fitem.htm%25253Fid%25253D20739535568%2526smSign%253DEh51d83i2uzo2b2zGtgKRg%25253D%25253D&TPL_timestamp=&TPL_password2=02d12254b4a503974749e4ee16f72e76081dce05e8fe449b487573ba72f14d47f9df56a8377afd48194afa7053aa1829cd9d3a55476a5510128244fea80fbed8a0c798146912122dcce4059be5ba85b39cc7d51fae6629a103d527256a3a48327c6e4cb1350806fa15e9ea07696cdce9c91658718f72b2f325b0d0784730e9fe&page=loginV3&ncoSig=&ncoSessionid=&ncoToken=034b80852bf10939ed237c7f67fd5ef4a3855720&TPL_username=zy118&um_token=C1523721251965735052899171523757663625204&ua=107%23ssznSzS9s2xAImllPVytXzO1XnIggOmR9LcTi88ngXX9lXFu%2F%2F94sFxKXrrOg%2FZvsLFLTAtXgFXxxXGQ%2FCxRlaEJXq6nuVE9luz8TdFDyJB%2BBaUtsYc0P894xppFjjidAOaEIdSveZpfnD1iDG2n7ISDflmisXa8KMKMoU%2FxPqBLTYtnO8KQVMpYmoBPOShgsCbDNSCXXQGLbLURQXXlDI5M9IjfOd3dPUh9PEUyljo%2BbL1NmKqXt3%2FweVQb8v9QkE%2F6k9DzC5vWQJAec6%2B1aOnflejd87g7m9jYygKX3ccb1dbwQmh6qYOcuWlw3mQmKlYV2yr7t7xqEmG01vFkqYVr3%2FLpu6tg29V22jXmoxcufdUbepynwC%2FHwUCiCgOKKZCNjE3OCy4bem2r8dEWdr9d3rhGvmt3jpiUK7XJCy4bek5r8dEmdrtGC3iUbfub25COijn8oEkDvpRIdDy%2Fbqy48C%2BDCf3AiLpng9gn82splff8c6rjantrG%2FCf81V6y9FAyii%2FXf53Z5Zr0xMzheiteOnGC5FsmE%2F46EtzI5IZQkAdv7VYrrexvYMzGvQygi%2BOmTjae5dbF6w0EJjyE8T4lInDXvIvOoVYPyZ7XP1MbY38%2BFXEEITAla%3D%3D'

response = requests.post('https://login.m.taobao.com/login.htm', headers=headers, params=params, data=data)
# print(response.text)
from time import sleep
sleep(5)
print(response.text)
print(str(response.cookies))

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://login.m.taobao.com/login.htm?_input_charset=utf-8&ttid=h5%40iframe', headers=headers, data=data)
