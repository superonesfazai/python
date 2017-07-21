#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function 

i = 1
while i <= 9:
    j = 1
    while j <= i:
        print("%d*%d " % (i, j), end='')
        j += 1
    i += 1
    print('')
