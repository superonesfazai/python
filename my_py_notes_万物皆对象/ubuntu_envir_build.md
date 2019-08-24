# 环境配置
```shell
$ apt-get update && apt-get upgrade -y
$ sudo apt-get install wget make gcc build-essential curl zlib* openssl libssl-dev zsh git vim --fix-missing
$ cd ~ && mkdir myFiles && cd myFiles 
# 安装
$ sudo apt-get install python3.6
# 对应删除
$ apt autoremove python3.6

# 并将/usr/local/python3/bin加入PATH
$ vim ~/.bash_profile
# 加入PATH=$PATH:$HOME/bin:/usr/local/python3/bin
$ source ~/.bash_profile
```