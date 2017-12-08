#!/usr/bin/python3.5
#coding: utf-8

import requests

files = {'file':open('imagespython.jpg', 'rb')} 
r = requests.post('https://www.slideshare.net/upload', files = files)
print(r.text)
