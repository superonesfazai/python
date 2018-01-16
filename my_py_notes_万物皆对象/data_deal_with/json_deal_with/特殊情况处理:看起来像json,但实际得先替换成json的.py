# coding:utf-8

'''
@author = super_fazai
@File    : 特殊情况处理:看起来像json,但实际得先替换成json的.py
@Time    : 2018/1/13 19:06
@connect : superonesfazai@gmail.com
'''

import sys, json

response_json = r"""'{"2445513":{"id":"2445513","code_color":"\u73ab\u7ea2"},"2445514":{"id":"2445514","code_color":"\u67a3\u7ea2"},"2445515":{"id":"2445515","code_color":"\u84dd\u8272"},"2445516":{"id":"2445516","code_color":"\u85cf\u9752"},"2445517":{"id":"2445517","code_color":"\u767d\u8272"},"2445518":{"id":"2445518","code_color":"\u9ed1\u8272"},"2565172":{"id":"2565172","code_color":"\u52a0\u7ed2\u9ed1\u8272"}}'"""

try:
  try: #try parsing to dict
    dataform = str(response_json).strip("'<>() ").replace('\'', '\"')
    struct = json.loads(dataform)
    print(struct)
  except:
    print(repr(response_json))
    print(sys.exc_info())
except:
    pass

