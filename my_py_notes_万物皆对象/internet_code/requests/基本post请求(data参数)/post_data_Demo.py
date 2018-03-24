#!/usr/bin/python3.5
#coding: utf-8

import requests
mydata = {'wd':'Linux', 'name':'xwp'}
r = requests.post('http://httpbin.org/post', data = mydata)
print(r.text)
