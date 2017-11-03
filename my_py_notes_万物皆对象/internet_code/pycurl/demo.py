# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@Time    : 2017/11/3 07:02
@connect : superonesfazai@gmail.com
'''
import traceback
import pycurl
from io import BytesIO

def get_html(url, referer='', verbose=False, protocol='https'):
    if not url.startswith(protocol):
        url = protocol + '://' + url
    url = str(url)
    print('url:', [url])
    html = ''
    headers = ['Cache-control: max-age=0', ]
    try:
        crl = pycurl.Curl()
        crl.setopt(pycurl.VERBOSE, 1)
        crl.setopt(pycurl.FOLLOWLOCATION, 1)
        crl.setopt(pycurl.MAXREDIRS, 5)
        crl.setopt(pycurl.CONNECTTIMEOUT, 8)
        crl.setopt(pycurl.TIMEOUT, 30)
        crl.setopt(pycurl.VERBOSE, verbose)
        crl.setopt(pycurl.MAXREDIRS, 15)
        crl.setopt(pycurl.USERAGENT, '一个user-agent')
        # crl.setopt(pycurl.HTTPHEADER,headers)
        if referer:
            crl.setopt(pycurl.REFERER, referer)
        crl.setopt(pycurl.URL, url)
        crl.fp = BytesIO()
        crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
        crl.perform()
        html = crl.fp.getvalue().decode('UTF-8')
        crl.close()
    except Exception as e:
        print('\n' * 9)
        traceback.print_exc()
        print('\n' * 9)
        return []
    return html

url = ''
get_html(url=url)