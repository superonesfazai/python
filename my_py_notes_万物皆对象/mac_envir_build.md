# 送给老是换mac的人 

## 安装sublime3
http://www.sublimetext.com/3

## 安装搜狗输入法
地址：https://pinyin.sogou.com/mac/ 
- 换肤
	- 偏好设置 -> 外观 -> 更多皮肤
	- 选择World Earth Day皮肤下载, 然后双击打开即可
	- 接着选 候选词个数: 7个，卷轴模式

## 安装latern
https://github.com/getlantern/download/wiki

## 安装Alfred3
https://www.alfredapp.com/

## 安装chrome(最新版)

## 安装pycharm
- 2018破解(https://blog.csdn.net/u014044812/article/details/78727496)
- 主题地址(http://www.themesmap.com/details.html?id=56af4d27333ecc1800c392b3)
- keymap设置为Eclipse(Mac os X) | 加个command+F为查找, command+option+r为替换 | 
- Editor->Font->Size: 14

## shell
- 设置背景色(终端->偏好设置->描述文件->Grass 字体15磅->点击默认)

## brew(网速要求较高)
```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

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

## vimplus(强大的vim)
https://github.com/chxuan/vimplus
```
$ git clone https://github.com/chxuan/vimplus.git ~/.vimplus
$ cd ~/.vimplus
$ ./install.sh
```

## 安装FileZilla
https://filezilla-project.org/download.php?type=client


## appstore 安装Dr.Cleaner

## 安装appcleaner
http://freemacsoft.net/appcleaner/

## python环境搭建(最好是直接brew install python3::但是这样下载的是最新版本3.7, 坑非常多!! 还是用下面的方法安装python3.6.3)因为会附带安装pip3
python3.6.3 下载

https://www.python.org/ftp/python/3.6.3/python-3.6.3-macosx10.6.pkg

### 安装Xcode command line tool(可以先不装)
```
$ xcode-select --install
```

### 安装pip3
```
$ wget https://bootstrap.pypa.io/get-pip.py
$ python3 get-pip.py
```

### IPProxyPool
https://github.com/qiyeboy/IPProxyPool
```
pip3 install requests chardet web.py==0.40.dev1 sqlalchemy gevent psutil
```

### 安装fzutils
```
$ pip3 install fzutils

# 安装pymssql, 先安装freetds
$ brew unlink freetds
$ brew install freetds@0.91
$ brew link --force freetds@0.91
$ pip3 install pymssql
```

## appstore安装Magnet

## 安装charlesproxy
https://www.charlesproxy.com/latest-release/download.do

- 注册码: https://www.jianshu.com/p/89111882fa99
- https抓取设置: https://www.jianshu.com/p/ec0a38d9a8cf

注意：在iOS 10.3之前,当你将安装一个自定义证书,iOS会默认信任,不需要进一步的设置。而iOS 10.3之后,安装新的自定义证书默认是不受信任的。如果要信任已安装的自定义证书,需要手动打开开关以信任证书。

## 安装mitmproxy
```
# 会附带安装mitmdump
pip3 install mitmproxy

# 并在手机上安装mitmproxy的证书
```

## 安装cheatsheet (mac快键键提示工具)
https://cheatsheet-mac.en.softonic.com/mac

## 安装Navicat Premium破解版
http://www.sdifen.com/navicatpremium11215.html

## 安装wps
http://www.wps.cn/product/wpsmac/

## 安装docker

## 安装Caffeine

## 安装网易云音乐
https://music.163.com/#/download