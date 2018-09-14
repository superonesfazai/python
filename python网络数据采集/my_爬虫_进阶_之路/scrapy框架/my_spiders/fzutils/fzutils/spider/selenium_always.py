# coding:utf-8

'''
@author = super_fazai
@File    : selenium_always.py
@connect : superonesfazai@gmail.com
'''

"""
预导入selenium常用的包

使用只需: from fzutils.spider.selenium_always import *
"""

from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchElementException,)