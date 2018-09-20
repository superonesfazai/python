# coding:utf-8

'''
@author = super_fazai
@File    : curl_utils.py
@connect : superonesfazai@gmail.com
'''

"""
curl utils
"""

import execjs

__all__ = [
    'curl_cmd_2_py_code',       # curl cmd to py code
]

def curl_cmd_2_py_code(curl_cmd:str) -> str:
    '''
    curl cmd to py code
        使用前提:
            已安装: npm install --save curlconverter
        github: https://github.com/NickCarneiro/curlconverter
        demo url: https://curl.trillworks.com
    :param curl_cmd:
    :return:
    '''
    js = r'''
    function a(curl_cmd){
        var curlconverter = require('curlconverter');
        var tmp = curlconverter.toPython(curl_cmd);
        
        return tmp;
    }
    '''
    js_parser = execjs.compile(js)
    res = js_parser.call('a', curl_cmd)

    return res