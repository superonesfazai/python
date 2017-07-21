#!/usr/bin/python3.5
#coding: utf-8

import requests

myparams = {'q':'Linux'}
r = requests.get('http://www.haosou.com/s', params = myparams)
r.url
f = open('linux.html', 'wb')
f.write(r.content)
f.close()
#print(r.content)
