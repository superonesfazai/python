#!/usr/bin/python3.5
#coding: utf-8

import requests
import json

mydata = {'wd':'Linux', 'name':'xwp'}
r = requests.post('http://httpbin.org/post', data = json.dumps(mydata))
print(r.text)
