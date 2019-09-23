# pybluez
PyBluez模块允许Python代码访问主机的蓝牙资源

[github](https://github.com/pybluez/pybluez)

## install 
```bash
# linux
$ apt-get install libbluetooth-dev mercurial 
# 安装gattlib(安装失败!!)
$ hg clone https://bitbucket.org/OscarAcena/pygattlib
$ cd pygattlib
$ cat DEPENDS
# 安装上面查看到的依赖
$ apt-get install libboost-python-dev libboost-thread-dev libboost-all-dev libglib2.0-dev libbluetooth-dev
$ pip3 download gattlib
$ tar xvzf ./gattlib-0.20150805.tar.gz
# 增加python36, 原先只支持python34
$ sed -ie 's/boost_python-py34/boost_python-py36/' setup.py
$ pip3 install .
$ pip3 install pybluez

# mac 
$ pip3 install git+https://github.com/pybluez/pybluez.git
```