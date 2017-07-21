#!/usr/bin/python2.7
#coding: utf-8

from distutils.core import setup, Extension

MOD = "test"

setup(name = MOD, ext_modules = [Extension(MOD, sources = ['test.c', 'testc_wrapper.c'])])
