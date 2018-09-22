# coding:utf-8

'''
@author = super_fazai
@File    : setup.py
@Time    : 2016/7/13 18:42
@connect : superonesfazai@gmail.com
'''

from __future__ import print_function
from setuptools import (
    setup,
    find_packages,
)
import sys
import os
import codecs
from requires import install_requires

"""
发布新包步骤:
    1. 现在从setup.py位于的同一目录运行此命令
    $ python3 setup.py sdist bdist_wheel
    
    2. upload
    $ twine upload dist/* --skip-existing
    
    3. 本地更新(发布完后过会才能更新Release)[注意: pycharm可能要单独更新]
    $ pip3 install fzutils -U
    
    4. 服务器上安装install fzutils解决方案(更新最后加个'-U')
    $ pip3 install -i http://pypi.douban.com/simple/ fzutils --trusted-host pypi.douban.com
    
报错及其解决方案:
    1. error: invalid command 'bdist_wheel'
        $ pip3 install pip setuptools -U && pip3 install wheel
"""

def read(f_name):
    """
    用来读取目录下的长描述
    我们一般是将README文件中的内容读取出来作为长描述，这个会在PyPI中你这个包的页面上展现出来，
    你也可以不用这个方法，自己手动写内容即可，
    PyPI上支持.rst格式的文件。暂不支持.md格式的文件，<BR>.rst文件PyPI会自动把它转为HTML形式显示在你包的信息页面上。
    """
    return codecs.open(os.path.join(os.path.dirname(__file__), f_name)).read()

long_description = read('README.md')

classifiers = [
    'Programming Language :: Python :: 3 :: Only',
    'License :: OSI Approved :: MIT License',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
]

# 可被导入的包(写最外层的就可以)
py_modules = [
    'fzutils',
]

setup(
    name="fzutils",
    version="0.1.8.9",
    author="super_fazai",
    author_email="superonesfazai@gmail.com",
    description="A Python utils for spider",
    py_modules=py_modules,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://www.github.com/superonesfazai",
    packages=find_packages(),
    platforms=['linux/Windows/Mac'],
    classifiers=classifiers,
    install_requires=install_requires,
    include_package_data=True,
    python_requires='>=3',
    zip_safe=True,
)



