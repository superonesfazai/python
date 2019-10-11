# 树莓派
Raspbian 是专门用于 ARM 卡片式计算机 Raspberry Pi® “树莓派”的操作系统。

Raspberry Pi® “树莓派”是 2012 年问世的 ARM 计算机，旨在为儿童和所有的计算机爱好者提供一套廉价的编程学习与硬件 DIY 平台。树莓派基于 ARM11，具有 1080P 高清视频解析能力，附带用于硬件开发的 GPIO 接口，使用Linux操作系统。售价仅 $25~$35。

Raspbian 系统是 Debian 7.0/wheezy 的定制版本。得益于 Debian从7.0/wheezy 开始引入的“带硬件浮点加速的ARM架构”(armhf)，Debian 7.0 在树莓派上的运行性能有了很大提升。Raspbian 默认使用 LXDE 桌面，内置 C 和 Python 编译器。

Raspbian 是树莓派的开发与维护机构 The Raspbeery Pi Foundation “树莓派基金会”，推荐用于树莓派的首选系统。

由于以下原因，Raspbian 需要单独组建软件仓库，而不能使用 Debian 的仓库：

 Debian下所有的软件包都需要用 armhf 重新编译。
 树莓派有部分特有的软件包，例如 BCM2835 CPU 的 GPIO 底层操作库。
 树莓派用户倾向于探索、尝试最新的软件。这与 Debian 软件源的策略完全不同。
 
[树莓派官网](https://www.raspberrypi.org/)

## sd卡系统刻录相关
[balenaEtcher下载](https://www.balena.io/etcher/)

![](https://i.loli.net/2019/08/24/ZeGpJaqwzThXS4m.gif)

## 树莓派Raspbian系统启用ROOT用户
树莓派的Raspbian系统root用户默认是禁用状态，且没有密码，所以要先设置个密码，然后开启才能正常使用。

```
使用pi账户进行登陆命令行，执行命令
$ sudo passwd root
新的 密码：
重新输入新的 密码：
passwd：已成功更新密码

设置root用户密码，然后在执行
$ sudo passwd --unlock root
passwd：密码过期信息已更改。

pi账户下测试是否生效root账户
$ sudo su root
```

## enable ssh
```bash
$ ssh pi@192.168.2.114
```

### 开启远程root登录(必须先在上面设置root密码)
```bash
$ sudo vi /etc/ssh/sshd_config
# 再将配置项PermitRootLoginwithout-password修改为PermitRootLogin yes，重启系统之后就可以登录
$ sudo reboot
```

```bash
$ ssh root@192.168.2.114
```

## enable vnc

## 更改密码
用户名是: pi
```bash
$ passwd
```

## vnc远程桌面连接
VNC就是一款可以让你通过手机或者电脑远程控制另一台主机的软件，在我们操作树莓派的时候，就可以通过VNC远程控制，而不再需要另外配置显示器和键盘。

现在的树莓派都默认安装VNC服务的，所以我们很简单就能通过命令行开启VNC。

首先进入系统，打开终端，或者通过远程SSH登陆树莓派。

### 开启vnc
1. 进入树莓派配置界面
```bash
$ sudo raspi-config
```
![](https://i.loli.net/2019/08/22/OE1FyNjiPzcxQvq.png)

2. 选择「5 Interfacing Options」，按回车
![](https://i.loli.net/2019/08/22/ceXR6n8mOdl2Psq.png)

3. 选择「P3 VNC」，按回车
![](https://i.loli.net/2019/08/22/ygAMwUex6JNTPiB.png)

4. 这里问你是否开启VNC服务，选择「Yes」，按回车
![](https://i.loli.net/2019/08/22/L4mzj7g29vZbAF8.png)

5. 提示已经开启VNC服务，按回车确认，之后退出树莓派配置界面
![](https://i.loli.net/2019/08/22/uty6QkzrpneObXL.png)

至此我们已经打开了树莓派的VNC服务，接下来，是通过软件进行VNC远程桌面控制。

### 使用VNC Viewer连接树莓派(vnc 除非设置内网穿透，固定公网IP或者花生壳动态域名解析，才可外网访问)
推荐使用：VNC Viewer，免费易用。[下载地址](https://www.realvnc.com/en/connect/download/viewer/)

(vnc账户 已存在Chrome vnc书签)

1. 打开VNC Viewer
2. 在地址栏上面输入树莓派的IP地址(eg: 192.168.2.114)，按回车, 即可登录进入树莓派ui页

## teamviewer
teamviewer 则可实现内网穿透 让外网访问

而teamviewer则登陆账户设置连接密码则可被世界上任意一台主机访问

## 树莓派 Raspberry Pi 更换清华大学源更新源方法
```bash
$ sudo vim /etc/apt/sources.list
# 进入编辑界面，注释原有的内容，粘贴如下内容：
deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib
deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib

$ sudo vim /etc/apt/sources.list.d/raspi.list
# 注释原文件所有内容，用以下内容取代：
deb http://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ buster main ui

$ sudo apt-get update && sudo apt-get upgrade
```

## 树莓派python开发环境搭建(下面权限都是root基础上: 先切换至root)
```bash
$ sudo su root
```

其python3版本默认是最新版

## oh-my-zsh
地址: https://github.com/robbyrussell/oh-my-zsh
```
$ sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
# 当前用户设置为zsh
chsh -s /bin/zsh

# 改变主题
vi ~/.zshrc
# 修改为pygmalion
```

### 安装python3.6.3
```bash
# 依赖安装(必须)
$ sudo apt-get install wget make gcc build-essential curl zlib* bzip2-devel openssl openssl-devel libssl-dev ncurses-devel git vim python-cffi python3-cffi libffi-dev libxml2 libxslt1.1 libxml2-dev libxslt1-dev python-libxml2 python-libxslt1 freetds-dev tmux sqlite3 libsqlite3-dev -y --fix-missing
$ wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz
$ tar -zxvf Python-3.6.3.tgz
$ cd Python-3.6.3
$ ./configure --prefix=/usr/local/python3 --enable-loadable-sqlite-extensions
$ make && make install

# 并将/usr/local/python3/bin加入PATH
$ vim ~/.zshrc
# 加入PATH=$PATH:$HOME/bin:/usr/local/python3/bin
$ source ~/.zshrc

$ pip3 install --upgrade pip
```

### python3安装opencv(非编译方式)
```
$ sudo apt-get install python-opencv libopencv-dev
```

### 安装fzutils
```bash
$ cd ~ && mkdir myFiles && cd myFiles && mkdir python

# 速度较快
$ pip3 install -i http://pypi.douban.com/simple/ numpy --trusted-host pypi.douban.com
# 安装pymssql必备
$ pip3 install -i http://pypi.douban.com/simple/ Cython --trusted-host pypi.douban.com
$ pip3 install -i http://pypi.douban.com/simple/ pillow wheel pysocks requests requests_oauthlib requests_toolbelt selenium==3.8.0 uvloop asyncio nest_asyncio psutil pyexecjs setuptools numpy pprint chardet scrapy greenlet==0.4.14 gevent aiohttp celery flower pyexcel pyexcel-xlsx fabric jieba appium-python-client elasticsearch elasticsearch_dsl salt baidu-aip fonttools xmltodict ftfy tenacity pyzbar termcolor pypinyin bitarray click websockets==7.0 pyppeteer bunch better_exceptions scapy scapy-http demjson jsonpath pytz python-dateutil sqlalchemy pymongo redis mongoengine prettytable pika pymssql --trusted-host pypi.douban.com
$ pip3 install -i http://pypi.douban.com/simple/ flask flask_login --trusted-host pypi.douban.com
$ pip3 install -i http://pypi.douban.com/simple/ fzutils --trusted-host pypi.douban.com
```

### 包报错处理

#### requests

```bash
# rasp报错: Caused by SSLError(SSLError("bad handshake: Error([('SSL routines', 'ssl_choose_client_version', 'unsupported protocol')]
# 导致原因: 系统tls安全性提高了
# 解决方案: 修改协议最低版本
# $ vi /etc/ssl/openssl.cnf
# [system_default_sect]
# MinProtocol = TLSv1.2
# CipherString = DEFAULT@SECLEVEL = 2
# 修改为
# [system_default_sect]
# MinProtocol = TLSv1.0
# CipherString = DEFAULT@SECLEVEL = 1
```

### 常用shell
```bash
# 查看cpu温度
$ watch -n 0.1 echo CPU: $[$(cat /sys/class/thermal/thermal_zone0/temp)/1000]°
or 
$ vcgencmd measure_temp

# 查看某文件最后几行
$ tail -n 200 xx.log
```

### man (查看某个命令用法)
```bash
$ man unzip
```

#### fzf (超快的命令行模糊查找器)(强烈推荐, 相见恨晚!!)
```bash
# github: https://github.com/junegunn/fzf
$ apt-get install fzf
# 用法
$ fzf 

# 切换当前工作目录
# 通过下面方式进入fzf, 选中目标目录回车即可进入
$ cd $(find * -type d | fzf)
```

#### cloc
```bash
# 代码统计工具
$ apt-get install cloc
# use
$ cloc xxx.py
```

#### thefuck (纠正您控制台命令错误)(强烈推荐, 详见恨晚!!)
```bash
# github: https://github.com/nvbn/thefuck
$ pip3 install thefuck
$ vi ~/.zshrc 
# 加入这行
eval $(thefuck --alias)
$ source ~/.zshrc

# 用法
root@raspberrypi:~|⇒  aptget update
zsh: command not found: aptget
root@raspberrypi:~|⇒  fuck
apt-get update [enter/↑/↓/ctrl+c]
```

#### nload (查看主机网络流量)
```bash
$ apt-get install nload
# use
$ nload
```

### git 加速
[blog](https://blog.csdn.net/w958660278/article/details/81161224)

打开https://www.ipaddress.com/

查询以下三个链接的DNS解析地址 (修改下方的ip, 再存入)
1. github.com 
2. assets-cdn.github.com 
3. github.global.ssl.fastly.net

```bash
$ vi /etc/hosts
# 加入下方
192.30.253.112     github.com
185.199.108.153    assets-cdn.github.com
151.101.185.194    github.global.ssl.fastly.net
# 刷新dns
$ sudo /etc/init.d/networking restart
```

然后速度起飞!

### 驱动

#### chromedriver
```bash
# 否则无法启动chromedriver
$ apt-get install chromium-browser libnss3 libgconf-2-4 
正在读取软件包列表... 完成
正在分析软件包的依赖关系树       
正在读取状态信息... 完成       
libgconf-2-4 已经是最新版 (3.2.6-5)。
libnss3 已经是最新版 (2:3.42.1-1)。
chromium-browser 已经是最新版 (74.0.3729.157-rpt5)。
升级了 0 个软件包，新安装了 0 个软件包，要卸载 0 个软件包，有 0 个软件包未被升级。

# 从上面可知当前安装的chromium-browser版本为74.0.3729.157-rpt5
# 找到对应版本的chromedriver进行下载
# 官网下载地址: https://chromedriver.chromium.org/downloads

# ** 推荐
# 下载驱动包 chromium-chromedriver(注意: 必须下载对应版本)
1. 打开google搜索chromium-chromedriver_74.0.3729.157
3. 选择下载指定的deb文件。
# 注意树莓派4必须是尾缀armhf.deb的, 否则报错软件包体系结构(arm64)与本机系统体系结构(armhf)不符
# todo 树莓派上下载慢的话可以本地下载deb, 再上传安装
$ wget https://archive.raspberrypi.org/debian/pool/main/c/chromium-browser/chromium-chromedriver_74.0.3729.157-rpt5_armhf.deb
$ dpkg -i chromium-chromedriver_74.0.3729.157-rpt5_armhf.deb 
正在选中未选择的软件包 chromium-chromedriver。
(正在读取数据库 ... 系统当前共安装有 96406 个文件和目录。)
准备解压 chromium-chromedriver_74.0.3729.157-rpt5_armhf.deb  ...
正在解压 chromium-chromedriver (74.0.3729.157-rpt5) ...
正在设置 chromium-chromedriver (74.0.3729.157-rpt5) ...
# 拷贝到我的目录下
$ cp /usr/bin/chromedriver /root/myFiles/linux_drivers 
$ cd /root/myFiles/linux_drivers 
# 成功
$ ./chromedriver 
Starting ChromeDriver 74.0.3729.157 (7b16107ab85c5364cdcd0b2dea2539a1f2dc327a-refs/branch-heads/3729@{#998}) on port 9515
Only local connections are allowed.
Please protect ports used by ChromeDriver and related test frameworks to prevent access by malicious code.
# 安装虚拟桌面
$ apt-get install xvfb

# todo 在树莓派上用chromedriver经常报错如下， 偶尔会成功, 推荐用firefoz or phantomjs
# 正常现象, 在高并发的情况下成功率还行
报错如下:  Message: chrome not reachable
```

#### firefox 
```bash
# 树莓派安装firefox
# 否则无法启动firefoxdriver
$ sudo apt-get install firefox-esr
# 查看版本
$ firefox --version
Mozilla Firefox 60.8.0

# geckodriver github: https://github.com/mozilla/geckodriver
# 选择arm7hf的下载
$ wget https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-arm7hf.tar.gz
$ tar -xzvf geckodriver-v0.21.0-arm7hf.tar.gz
# 成功
$ ./geckodriver 
1566968312048	geckodriver	INFO	geckodriver 0.21.0
1566968312107	geckodriver	INFO	Listening on 127.0.0.1:4444
```

#### phantomjs
```bash
# 树莓派安装phantomjs(我已下载到本地直接运行即可)
# 装2.1.1 gitHub: https://github.com/ApioLab/phantomjs-2.1.1-linux-arm
$ apt-get install chrpath git-core libfontconfig1-dev libxft-dev 
$ cd ~/myFiles/linux_drivers
$ wget https://raw.githubusercontent.com/ApioLab/phantomjs-2.1.1-linux-arm/master/phantomjs-2.1.1-linux-arm.tar.bz2
# 解压即可得到在树莓派上能运行的phantomjs
$ tar -jxvf phantomjs-2.1.1-linux-arm.tar.bz2
# 更改路径至(文件名得一致) '/root/myFiles/linux_drivers/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'

# 运行./phantomjs 报错:
# ./phantomjs: error while loading shared libraries: libssl.so.1.0.0: cannot open shared object file: No such file or directory
# google 搜索libssl1.0.0 for 64bit发现解决方案
$  vi /etc/apt/sources.list
# 加入下面这行
deb http://security.debian.org/debian-security jessie/updates main
$ apt-get update
# 报错
获取:1 http://security.debian.org/debian-security jessie/updates InRelease [44.9 kB]
错误:1 http://security.debian.org/debian-security jessie/updates InRelease               
  由于没有公钥，无法验证下列签名： NO_PUBKEY 9D6D8F6BC857C906 NO_PUBKEY AA8E81B4331F7F50
命中:2 http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian buster InRelease
命中:3 http://mirrors.tuna.tsinghua.edu.cn/raspberrypi buster InRelease
正在读取软件包列表... 完成
W: GPG 错误：http://security.debian.org/debian-security jessie/updates InRelease: 由于没有公钥，无法验证下列签名： NO_PUBKEY 9D6D8F6BC857C906 NO_PUBKEY AA8E81B4331F7F50
E: 仓库 “http://security.debian.org/debian-security jessie/updates InRelease” 没有数字签名。
N: 无法安全地用该源进行更新，所以默认禁用该源。
N: 参见 apt-secure(8) 手册以了解仓库创建和用户配置方面的细节。
# 解决方法很简单，下载导入公钥就行，下载导入key的命令如下:
# 此处6AF0E1940624A220需要是错误提示的key
$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 9D6D8F6BC857C906 
$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys AA8E81B4331F7F50
# 成功
$ apt-get update
# 搜索libssl1.0.0
$ apt-cache search libssl1
libssl1.0-dev - Secure Sockets Layer toolkit - development files
libssl1.0.2 - Secure Sockets Layer toolkit - shared libraries
libssl1.1 - Secure Sockets Layer toolkit - shared libraries
libssl1.0.0 - Secure Sockets Layer toolkit - shared libraries
libssl1.0.0-dbg - Secure Sockets Layer toolkit - debug information
$ apt-get install libssl1.0.0

# 再运行./phantomjs 报错:
./phantomjs: error while loading shared libraries: libicui18n.so.52: cannot open shared object file: No such file or directory
$ apt-get install libicu52
```

### 安装redis-server
```bash
$ apt-get install redis-server
$ 设置可被外网访问
# 找到bind 127.0.0.1将其注释, 改成bind 0.0.0.0
# 修改密码(只供内网访问可以不设置!)
# 找到 requirepass foobared, 把注释去掉然后设置新密码 eg: requirepass 654321yy
$ vi /etc/redis/redis.conf

# 以配置文件启动redis
$ redis-server /etc/redis/redis.conf 
```

### 禁用wifi
```bash
$ vi /etc/modprobe.d/raspi-blacklist.conf
# 加上
# wifi
blacklist brcmfmac
blacklist brcmutil
# 蓝牙
# blacklist btbcm
# blacklist hci_uart
$ reboot
```

### 解决树莓派使用HDMI-VGA转换器黑屏的方案(如果外接显示器的话, 一般不设置已cli模式)
设置树莓派默认启动页(desktop/shell)
```bash
$ sudo raspi-config
# 1. 选择Boot Options
# 2. 选择Desktop/cli
# 3. 选择B3 Desktop
# 4. 回车, 保存更改并reboot即可
```

### vim 变成IDE
代码自动补全神器

[YouCompleteMe](https://github.com/ycm-core/YouCompleteMe)

#### 安装
```bash
# 检查一下vim对python的支持
# 因为用sudo安装的vim默认是不支持python的，这样会导致需要python支持的插件无法运行
# 但如果你是遇到python导致无法运行的话，也是有方法的，在下面会提到。
# ‘-’就证明是没有支持python的
$ vim --version | grep python 
+comments          +libcall           -python            +visualextra
+conceal           +linebreak         -python3           +viminfo

# ** 很麻烦不推荐
# 下载官网源码重新编译安装vim
$ apt-get install libncurses5-dev
# 100多M下载较慢的话, 可在本地先下载再上传
$ git clone https://github.com/vim/vim.git
$ unzip master.zip
$ cd vim-master/src
$ make clean
$ which python2.7
/usr/bin/python2.7
# 指定python 路径
# --with-python-config-dir=/usr/lib/python2.7/config-arm-linux-gnueabihf/ 
$ which python3.6
/usr/local/python3/bin/python3.6
# 指定python3.6路径
# --with-python-config-dir=/usr/local/python3/lib/python3.6/config-3.6m-arm-linux-gnueabihf/ 

$ cd vim-master
$ ./configure --with-features=huge --enable-python3interp --enable-pythoninterp --with-python-config-dir=/usr/local/python3/lib/python3.6/config-3.6m-arm-linux-gnueabihf/ --enable-rubyinterp --enable-luainterp --enable-perlinterp --with-python-config-dir=/usr/lib/python2.7/config-arm-linux-gnueabihf/ --enable-multibyte --enable-cscopec --prefix=/usr/local/vim/
# 备注说明
--with-features=huge：支持最大特性
--enable-rubyinterp：打开对ruby编写的插件的支持
--enable-pythoninterp：打开对python编写的插件的支持
--enable-python3interp：打开对python3编写的插件的支持
--enable-luainterp：打开对lua编写的插件的支持
--enable-perlinterp：打开对perl编写的插件的支持
--enable-multibyte：打开多字节支持，可以在Vim中输入中文
--enable-cscope：打开对cscope的支持
--with-python-config-dir=/usr/lib/python2.7/config-arm-linux-gnueabihf/ 指定python 路径
--with-python-config-dir=/usr/local/python3/lib/python3.6/config-3.6m-arm-linux-gnueabihf/ 指定python3路径
--prefix=/usr/local/vim：指定将要安装到的路径(自行创建)

$ make install
```

### spacemacs
Spacemacs 是一份 Emacs 的配置文件，将 Vim 的快捷键移植到了 Emacs 上，可以提供 Vimer 至 Emacs 的无缝衔接。有了 Spacemacs，你不需要花那么多时间去学习 Emacs 就可以真正用 Spacemacs 开始做一些事情。

[github](https://github.com/syl20bnr/spacemacs)

#### 安装
```bash
# 先安装emacs
$ apt-get install emacs
$ emacs --version

# 安装spacemacs
$ mv ~/.emacs.d ~/.emacs.d.bak
$ git clone https://github.com/syl20bnr/spacemacs ~/.emacs.d
# Clone 至本地后，第一次使用 Spacemacs 时要加载一些 Package，以及根据你的喜好所生成的配置，建议一路回车。
$ emacs

# 安装 layer 依赖
# spacemacs 中相关功能的插件/扩展包以 layer 的形式聚合在一起。
# 以 Python layer 为例，其文档（位于~/.emacs.d/layers/+lang/python/README.org）明确指出了它的外部依赖。比如，获取自动补全功能，需要 anaconda-mode：
# 请跟据你开启的 layer 自行补充所需的外部依赖
$ pip install --upgrade "jedi>=0.9.0" "json-rpc>=1.8.1" "service_factory>=0.1.5"

# dotspacemacs-configuration-layers 是启用的 layer 列表。
# 初始列举的 layer 大多被双引号注释掉了，你可以移除注释使用它们，同时自行添加其他的 layer
# ** 一定要启用 auto-completion 和 heml，它们是 spacemacs 的灵魂所在。另外可使用 themes-megapack 下载各类皮肤。

# 第一次打开py文件, 会提示是否安装py插件, 选yes
$ emacs test.py

# python自动补全
# 方法1(推荐)
$ emacs
# 打开配置文件(SPC f e d) or vi ~/.spacemacs, 找到python, 把下面注释去掉, 重启(就会自动安装相应包)就有代码补全了
;; auto-completion
;; spell-checking
;; syntax-checking
$ 依赖安装
$ pip install -i http://pypi.douban.com/simple/ flake8 importmagic autopep8 yapf virtualenv --trusted-host pypi.douban.com

# 方法2
$ vi ~/.spacemacs
# 找到dotspacemacs-additional-package, 把epc  deferred  auto-complete  jedi写进括号(如下面图片), 保存退出
$ emacs
# 在emacs中安装install-server
$ SPC+ M-X:  Jedi:install-server
# 添加以下配置到emacs的配置文件(.emacs.d/init.el)里
$ vi ~/.emacs.d/init.el
(autoload 'jedi:setup "jedi" nil t)
(add-hook 'python-mode-hook 'jedi:setup)
(setq jedi:setup-keys t)                      ; optional
(setq jedi:complete-on-dot t)                 ; optional
# 大功告成
```
![](https://i.loli.net/2019/09/02/tgyzDhxNs5TV2K9.png)

#### spacemacs 快捷键
Spacemacs 基本可以使用的是原生 Vim 的快捷键

```bash
F1                          帮助

配置文件
SPC f e d                   快速打开配置文件
SPC f e R                   同步配置文件
SPC q q                     退出 Emacs
SPC q R                     重启 Emacs
```

#### emacs 快键键(原生的emacs)
[Emacs快捷键列表](https://aifreedom.com/technology/112)

```bash
C = Control
M = Meta = Alt | Esc
Del = Backspace

C+h t                       打开emacs教程

C+x C+s                     保存文件
C+x C+c                     关闭emacs
C+a                         光标移动到行首
C+e                         光标移动到行尾
C+s                         向后搜索
C+r                         向前搜索
C+a C+k                     移除当前行
C+x u                       撤销上一个命令(操作)
C+g                         停止当前运行/输入的命令

# 窗口命令
C+x 2                       水平分割窗格
C+x 3                       垂直分割窗格
C+x o                       切换至其他窗格
C+x 0                       关闭光标所在窗格
C+x 4 f                     在其他窗格中打开某个文件
```

### linux 打开文件数 too many open files 解决方法
*之前高并发1500+时老报抓取失败, 最后发现是server.py 代理提供服务时, ulimit -n 限制所致!!!*

```bash
$ ulimit -a
-t: cpu time (seconds)              unlimited
-f: file size (blocks)              unlimited
-d: data seg size (kbytes)          unlimited
-s: stack size (kbytes)             8192
-c: core file size (blocks)         0
-m: resident set size (kbytes)      unlimited
-u: processes                       29184
-n: file descriptors                1024
-l: locked-in-memory size (kbytes)  65536
-v: address space (kbytes)          unlimited
-x: file locks                      unlimited
-i: pending signals                 29184
-q: bytes in POSIX msg queues       819200
-e: max nice                        0
-r: max rt priority                 0
-N 15:                              unlimited

# 非永久
$ ulimit -n 65536

# 永久
# 查找文件的具体的位置
$ find / -name pam_limits.so
/lib/arm-linux-gnueabihf/security/pam_limits.so 
# /etc/pam.d/login 添加pam_limits.so (有时候系统默认添加)
# 添加 session required /lib/arm-linux-gnueabihf/security/pam_limits.so 
$ vi /etc/pam.d/login

$ vim /etc/security/limits.conf
# 在最后加入
root soft nofile 65536
root hard nofile 65536
# root表示用户 可用*表示所有用户，可根据需要设置某一用户(eg: root), 设置的数值与硬件配置有关，别设置太大了。

# 添加 echo 8061540 > /proc/sys/fs/file-max
$ vi /etc/rc.local

# 改完后注销一下就能生效。
$ logout
$ reboot
```

#### 查看进程文件打开数
```bash
# 查看所有进程的文件打开数
$ lsof | wc -l
30989
# 查看某个进程打开的文件数
$ lsof -p pid | wc -f
```

## jupyter notebook
[doc](https://jupyter.readthedocs.io/en/latest/running.html#running)

### 运行
```bash
$ jupyter notebook --port 9999 --allow-root
# 允许远程得先进行下面的设置可远程访问
$ jupyter notebook --port 9999 --allow-root --config=/root/.jupyter/jupyter_notebook_config.py
```

### 修改密码
```bash
$ jupyter notebook password
Enter password: 
Verify password: 
[NotebookPasswordApp] Wrote hashed password to /root/.jupyter/jupyter_notebook_config.json
```

### 设置可远程访问
默认情况下，配置文件 ~/.jupyter/jupyter_notebook_config.py 并不存在，需要自行创建。使用下列命令生成配置文件：
```bash
$ jupyter notebook --generate-config --allow-root
Writing default config to: /root/.jupyter/jupyter_notebook_config.py
$ vi ~/.jupyter/jupyter_notebook_config.py
# 在 jupyter_notebook_config.py 中找到下面的行，取消注释并修改。
c.NotebookApp.ip='*'
c.NotebookApp.password = u'sha:ce...刚才复制的那个密文 or vi /root/.jupyter/jupyter_notebook_config.json 赋值里面的信息'
```

## 外网访问树莓派

### cpolar(推荐)
如果你曾尝试将树莓派（Raspberry Pi）设置成为物联网设备，你就会知道，除非你跳过一大堆恼人的内网穿透问题，否则你就无法在本地网络上提供网页和数据。从家庭或本地网络外部访问树莓派可能是一项挑战。

cpolar是一种安全的隧道服务，可以在任何地方在线提供您的设备。 隧道是一种在两台计算机之间通过互联网等公共网络建立专线的方法。 当您在两台计算机之间设置隧道时，它应该是安全且私有的，并且能够通过网络障碍，如端口阻塞路由器和防火墙。 这是一个方便的服务，允许您在安全的无线网络或防火墙后面将请求从公共互联网连接到本地计算机。 使用此平台，您可以通过非常简单的方式从家庭或本地网络外部访问Raspberry Pi。

[开始页](https://dashboard.cpolar.com/get-started)

#### 安装
```bash
$ sudo wget https://www.cpolar.com/static/downloads/cpolar-stable-linux-arm.zip
$ sudo unzip cpolar-stable-linux-arm.zip && rm -rf cpolar-stable-linux-arm.zip
```

#### 注册
免费版的cpolar允许您一次访问一个终端，并在每次启动cpolar时分配随机网址。 使用免费版本，您每次希望建立远程连接并与远程用户共享地址时，都必须从Pi生成主机地址。

要创建cpolar帐户，请单击此处，然后单击注册以获取authtoken密钥。 如果您希望自己的自定义域执行联机SSH，则此令牌是必需的。

登录到cpolar网站后，您将获得一个authtoken密钥，其中包含许多字符的组合。 您需要保密此令牌：拥有此令牌的任何人都可以访问您的Raspberry Pi。

[获取自己账户的认证代码](https://dashboard.cpolar.com/get-started)

使用您从cpolar网站获得的令牌更改yourauthtoken字符串。 您只需要为Raspberry pi执行一次认证，它就会存储在配置文件中。

```bash
$ ./cpolar authtoken xxxxx[你的账号的认证代码]
Authtoken saved to configuration file: /root/.cpolar/cpolar.yml
```

#### 远程连接

##### 使用ssh从远程网络访问Pi
在Raspberry Pi终端中键入以下命令以启用从远程访问Putty终端。
```bash
$ ./cpolar tcp 22
```

![](https://i.loli.net/2019/08/27/dn8XS5BmUPjuC2s.png)

如果你的隧道状态为“online”，你可以在任何地方使用Putty打开你的Raspberry Pi终端。 注意下图所示的主机地址和端口号; 你将使用它们来访问Raspberry Pi。

远程ssh
```bash
$ ssh <树莓派用户名@1.tcp.cpolar.io> -p <cpolar公网端口号>  

# 本例子
$ ssh root@1.tcp.cpolar.io -p 10012
参数说明：
-p 参数 指定服务器端口号
10012 是上图cpolar分配给你的服务器端口号，每次会变化
1.tcp.cpolar.io 是服务器分配给你的服务器主机地址，每次会变化
root 是树莓派默认用户名
```

##### http访问pi
要在端口80上启动HTTP隧道
```bash
$ ./cpolar http 80
```
![](https://i.loli.net/2019/08/27/ipgJnWKuZfFT7vk.png)

如果你的隧道状态为“online”，你可以在任何地方使用浏览器连接Raspberry Pi终端

浏览器访问
```bash
# 例子
http://4e9c5588.cpolar.io
https://4e9c5588.cpolar.io
```

### 花生壳内网穿透(收费不推荐)
进入[花生壳官网下载页面](https://hsk.oray.com/download/)，选择树莓派

![](https://i.loli.net/2019/08/28/sionHPpVEGXzfdI.png)

#### 安装
```bash
$ wget http://download.oray.com/peanuthull/embed/phddns_3.0.3_systemd.deb
$ dpkg -i phddns_3.0.3_systemd.deb 
正在选中未选择的软件包 phddns。
(正在读取数据库 ... 系统当前共安装有 96419 个文件和目录。)
准备解压 phddns_3.0.3_systemd.deb  ...
正在解压 phddns (3.0.3) ...
正在设置 phddns (3.0.3) ...
Created symlink /etc/systemd/system/default.target.wants/phddns.service → /lib/systemd/system/phddns.service.
Phddns Service install success.                           

+--------------------------------------------------+
|             Oray PeanutHull Linux 3.0            |
+--------------------------------------------------+
|  SN: xxxxxxxxxxxxxxxx   Default password: admin  |
+--------------------------------------------------+
|    Remote Management Address http://b.oray.com   |
+--------------------------------------------------+
```

#### 卸载
```bash
$ dpkg -r phddns
(正在读取数据库 ... 系统当前共安装有 96431 个文件和目录。)
正在卸载 phddns (3.0.3) ...
Remove Phddns Service Success.
```

#### 启动/停止/重启
```bash
$ phddns start
$ phddns stop
$ phddns restart
```