#!/usr/bin/python2.7
#coding: utf-8

from distutils.core import setup, Extension

MOD = "避免死锁.md"

setup(name = MOD, ext_modules = [Extension(MOD, sources = ['避免死锁.md.c', 'testc_wrapper.c'])])
