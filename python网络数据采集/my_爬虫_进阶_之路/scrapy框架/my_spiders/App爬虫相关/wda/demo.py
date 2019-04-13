# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

import wda

wda.DEBUG = True        # default False
wda.HTTP_TIMEOUT = 60.0 # default 60.0 seconds

# Enable debug will see http Request and Response
c = wda.Client('http://localhost:8100')

# get env from $DEVICE_URL if no arguments pass to wda.Client
# http://localhost:8100 is the default value if $DEVICE_URL is empty
# c = wda.Client()

c.healthcheck()