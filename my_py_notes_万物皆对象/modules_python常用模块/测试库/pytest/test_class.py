# coding:utf-8

'''
@author = super_fazai
@File    : test_class.py
@connect : superonesfazai@gmail.com
'''

"""
simple use:
$ pytest -q test_class.py
"""

import pytest

class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")