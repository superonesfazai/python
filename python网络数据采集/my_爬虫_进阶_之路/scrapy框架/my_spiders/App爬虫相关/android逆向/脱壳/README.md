# android脱壳
[blog](https://blog.csdn.net/jiangwei0910410003/article/details/78548069)

[blog](https://zhuanlan.zhihu.com/p/45591754)

## 脱壳工具FDex2
通过Hook ClassLoader的loadClass方法，反射调用getDex方法取得Dex(com.android.dex.Dex类对象)，在将里面的dex写出。

[下载地址, 提取码:xk5c](https://pan.baidu.com/s/1zD1Xa68d4NsrVgXcXvJoAA)

1. 在VirtualXposed中安装FDex2
2. Xposed中激活FDex2框架, 并软重启xposed
3. 启动VirtualXposed中的FDex2，并配置要脱壳的应用。

## drizzleDumper(need root)
[github](https://github.com/DrizzleRisk/drizzleDumper)

[使用](https://blog.csdn.net/suwenlai/article/details/80021667)

## 通过xposed内部框架DumpDex进行脱壳
1. 下载安装[dumpdex](https://pan.baidu.com/s/1Rv9CbvoOlj7TTXyDmbCh-g#list/path=%2F)
2. 在xposed里面软重启，激活。就好了。
3. 点击app打开, 这个时候WrBug会自动的帮我们脱壳完成。 此时此刻我们只需要去对应目录找dex文件就好了。

## 终极方法
在模拟器(本身就是root的)里面进行相应脱壳即可!
