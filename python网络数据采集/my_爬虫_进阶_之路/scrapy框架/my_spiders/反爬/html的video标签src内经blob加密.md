# html的video标签src内经blob加密
现在很多主流的视频网站几乎都是用到了blob的加密（其实也不算是加密），效果是隐藏了视频源的地址，其背后的本质还是通过一段执行一段js拿到视频的切片文件，然后进行拼接播放。
![](https://img-blog.csdn.net/20180614231004461?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hpbmd5dW44OTExNA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

## 方法1
编辑video标签，将链接放入到a标签内获取源地址
![](https://img-blog.csdnimg.cn/20181117175942977.png)

确定后网页即会自动获得源地址（src），如图：
![](https://img-blog.csdnimg.cn/20181117175909602.png)

## 方法2(可行)
chrome 扩展搜索adobe hls(目前收费) 或者 HLS Downloader 下载扩展安装, 其在加载某个带video blog的url即可获取其m3u8的下载地址

![](https://i.loli.net/2019/08/08/9zRoT7yEVdvgOlP.png)

刷新当前页面，插件就会自动获取后缀为.m3u8的地址
![](https://i.loli.net/2019/08/08/hizO7PE4HrWLbSX.png)

hls downloader

![](https://i.loli.net/2019/08/08/O6b9YqjDPWHrcx8.png)