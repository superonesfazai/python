# atx
ATX(AutomatorX) 是一款开源的自动化测试工具，支持测试iOS平台和Android平台的原生应用、游戏、Web应用。 使用Python来编写测试用例，混合使用图像识别，控件定位技术来完成游戏的自动化。附加专用的IDE来完成脚本的快速编写。

[github](https://github.com/NetEaseGame/ATX)

[uiautomator2 github](https://github.com/openatx/uiautomator2)

## 重要说明
新版本以采用新的uiautomator2替换到原来的atx-uiautomator. 历史版本可以通过Tag查看tag:1.1.3 测试安卓应用前，需要先进行init操作
```bash
$ python3 -muiautomator2 init
```

用于安卓和iOS原生应用测试的库已经分离出来，可以单独使用（强烈推荐单独使用，一来依赖少、稳定性高，二来写代码的时候还能自动补全）

- 对于Android应用的测试，如果不需要用到图像识别，推荐使用这个项目uiautomator2
- 对于iOS应用的测试，如果不需要用到图像识别，推荐使用这个项目facebook-wda

## 安装
```bash
$ pip3 install --upgrade --pre atx
$ pip3 install opencv_contrib_python
$ pip3 install uiautomator
$ pip3 install --pre -U uiautomator2
# 手机接到电脑上之后，需要先运行一下命令 python3 -m uiautomator2 init将需要的程序部署到手机上，以便后续的自动化（PS：每个手机初始化一次就够了）

# ATX Weditor是一个python库
$ pip3 install --pre weditor

# AppetizerIO 所见即所得脚本编辑器
# AppetizerIO 提供了对uiautomator2的深度集成，可以图形化管理ATX设备，还有所见即所得脚本编辑器
https://www.appetizer.io/
```

## 使用
1. python3 -m weditor 
2. python3 -m uiautomator2 init 

(启动atx代理，uiautomator代理 如果启动推送安装失败 则 $ cd ~/.uiautomator2 然后在该目录下 $ rm -rf * 最后重跑python3 -m uiautomator2 init)

### 检查是否安装成功
```bash
$ python3 -m atx version
# 检查环境配置是否正常
$ python3 -m atx doctor
```

### 热键
返回上一页
```python
d.press("back")
```
返回主页
```python
d.press('home')
```
屏幕解锁
```python
d.unlock()
# 1. launch activity: com.github.uiautomator.ACTION_IDENTIFY
# 2. press "home"
```
app启动
```python
d.app_start('包名')
```
xpath 用法
```python
d.xpath('//android.widget.TextView').all()[2].text
```
元素的文字内容获取
```python
d.xpath('//android.widget.TextView').info.get('contentDescription', '')
```
d(text='Clock', className='android.widget.TextView')中可用参数

[java doc](https://developer.android.com/reference/android/support/test/uiautomator/UiSelector)
```bash
- text, textContains, textMatches, textStartsWith
- className, classNameMatches
- description, descriptionContains, descriptionMatches, descriptionStartsWith
- checkable, checked, clickable, longClickable
- scrollable, enabled,focusable, focused, selected
- packageName, packageNameMatches
- resourceId, resourceIdMatches
- index, instance
```

滑动

![](https://i.loli.net/2019/03/02/5c7a24c360d07.png)

watcher

![](https://i.loli.net/2019/03/02/5c7a24d38a9d1.png)

ATX的图片识别,是支持分辨率缩放匹配的,前提就是,在保存截图的时候要注明是在哪个分辨率下面截的图,命名方式如下:

![](https://i.loli.net/2019/03/06/5c7f2d36ec620.png)

原理大概就是:从文件名获取源分辨率,从设备获取设备分辨率,然后将图片按照比例缩放

### 测试过程报告
因为ATX集成了测试报告，所以生成响应的测试报告也很简单 在第3行代码之后加入以下代码
```python
from atx.ext.report import Report
rp = Report(d)
rp.patch_wda()
```
再次运行一遍代码，在当前脚本所在目录下就可以看到一个report目录，里面有一个image目录，里面是每一步的截图