# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-26 下午2:43
# @File    : functools_test.py

import functools
from urllib.request import urlopen
from urllib.error import HTTPError

@functools.lru_cache(maxsize=32)
def get_pep(num):
    'retrieve text of a python enhancement proposal'
    resource = 'http://www.python.org/dev/peps/pep-%04d/' % num
    try:
        with urlopen(resource) as s:
            return s.read()
    except HTTPError:
        return 'Not Found'

for n in 8, 290, 308, 320, 8, 218:
    pep = get_pep(n)
    print(n, len(pep))

print(get_pep.cache_info())

# efficiently computing Fibonacci numbers using a cache
# to implement a dynamic programming technique
@functools.lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

print([fib(n) for n in range(16)])
print(fib.cache_info())

@functools.singledispatch
def fun(arg, verbose=False):
    if verbose:
        print("Let me just say,", end=" ")
    print(arg)

fun()