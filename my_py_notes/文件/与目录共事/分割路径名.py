#!/usr/bin/python3.5
#coding: utf-8

#分割路径名

import os

print(os.path.split('~/避免死锁.txt'))

(filepath, filename) = os.path.split('~/避免死锁.txt')

print(filepath, ' ', filename)

(shortname, extension) = os.path.splitext(filename)

print(shortname, ' ', extension)