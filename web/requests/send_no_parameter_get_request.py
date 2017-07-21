#!/usr/bin/python3.5
#coding: utf-8

import requests

r = requests.get('http://httpbin.org/get')
print(r.text)
