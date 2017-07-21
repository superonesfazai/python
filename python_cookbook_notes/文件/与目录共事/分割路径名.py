#!/usr/bin/python3.5
#coding: utf-8

#分割路径名

import os

print(os.path.split('~/test.txt'))

(filepath, filename) = os.path.split('~/test.txt')

print(filepath, ' ', filename)

(shortname, extension) = os.path.splitext(filename)

print(shortname, ' ', extension)