## apktool用法


## dex2jar用法
a.下载 dex2jar，并解压
b.下载class反编译工具 jd-gui，并解压
c.将测试的安装包xxx.apk后缀改为.zip，解压后拷贝classes.dex文件到dex2jar文件目录下，cmd进入改目录，执行dex2jar.bat classes.dex命令，会生成classes-dex2jar.jar文件；
d.打开jd-gui工具，然后将生成的classes-dex2jar.jar文件拖进去，即可看见反编译的文件
