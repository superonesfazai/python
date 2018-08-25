# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@Time    : 2017/10/11 14:24
@connect : superonesfazai@gmail.com
'''

import sys
sys.path.append('..')

from fzutils.spider.fz_requests import MyRequests
from fzutils.internet_utils import get_random_pc_ua
from settings import CHROME_DRIVER_PATH

import os, shutil
import zipfile
from selenium import webdriver

class ChromeExtensioner(object):
    '''chrome扩展插件'''
    def __init__(self):
        self.extension_dir = './extensions'
        self.ip_pools_info = {
            'schema': 'http',
            'host': '127.0.0.1',
            'port': '8000',
            'username': '',
            'password': ''
        }

    def get_extension_dir_path(self):
        '''
        本地先生成插件内容, 再返回插件路径
        :return:
        '''
        path = "{0}/{1}_{2}".format(self.extension_dir, self.ip_pools_info['host'], self.ip_pools_info['port'])
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

        with open(path + '/manifest.json', 'w') as f:
            f.write(self.get_manifest_content())
        with open(path + '/background.js', 'w') as f:
            f.write(self.get_background_content())

        return os.path.abspath(path)

    def get_extension_file_path(self):
        '''
        从.zip文件中读取插件, 再返回插件路径
        :return:
        '''
        path = "{0}/{1}_{2}.zip".format(self.extension_dir, self.ip_pools_info['host'], self.ip_pools_info['port'])
        if os.path.exists(path):
            os.remove(path)

        zf = zipfile.ZipFile(path, mode='w')
        zf.writestr('manifest.json', self.get_manifest_content())
        zf.writestr('background.js', self.get_background_content())
        zf.close()

        return os.path.abspath(path)

    def get_manifest_content(self):
        '''
        mainfest.json内容
        :return:
        '''
        return '''
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        '''

    def get_background_content(self):
        '''
        background.js内容(关键内容)
        :return:
        '''
        return '''
        chrome.proxy.settings.set({{
            value: {{
                mode: "fixed_servers",
                rules: {{
                    singleProxy: {{
                        scheme: "{0}",
                        host: "{1}",
                        port: {2}
                    }},
                    bypassList: ["foobar.com"]
                }}
            }},
            scope: "regular"
        }}, function() {{}});

        chrome.webRequest.onAuthRequired.addListener(
            function (details) {{
                return {{
                    authCredentials: {{
                        username: "{3}",
                        password: "{4}"
                    }}
                }};
            }},
            {{ urls: ["<all_urls>"] }},
            [ 'blocking' ]
        );
        '''.format(self.ip_pools_info['schema'], self.ip_pools_info['host'], self.ip_pools_info['port'], self.ip_pools_info['username'], self.ip_pools_info['password'])

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_extension(get_extension_file_path())
ext = ChromeExtensioner()
chrome_options.add_argument('--load-extension={0}'.format(ext.get_extension_dir_path()))

browser = webdriver.Chrome(
    executable_path=CHROME_DRIVER_PATH,
    chrome_options=chrome_options
)
# browser.get('http://ip138.com')
browser.get('https://www.baidu.com')     # 本机ip查询