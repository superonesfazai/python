# lxhToolHTTPDecrypt
利用HTTP协议 远程加解密数据包，实现Burp一条龙服务。

## 背景
在做APP渗透测试的时候，通常通信协议基本都做了加解密功能，每次都需要去逆向APP并寻找到加解密算法后，针对写Burp插件，这么一个流程下来花费了一大堆的时间，万一遇到加固，又要耗时间去脱壳，这尼玛遇到壳又脱不了，咋怎，最后利用几分钟来抓包改包，然后发现0高0中0低...我枯了，你们呢。

HTTP Decrypt 提供了Finds Hooks模块，可以在不逆向不脱壳的情况下快速的找到APP所使用的加解密算法，而toBurp模块提供了直接使用APP内的方法进行加解密，而不需自己动手敲代码，对于整体POST加密更是提供了自动化加解密功能，可以实现Burp一条龙，Burp Scanner ，Intruder自动加解密。

[github](https://github.com/lyxhh/lxhToolHTTPDecrypt)