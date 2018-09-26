# android连接

将Android手机(或者安卓虚拟机)通过数据线和运行Appium的PC相连，同时打开USB调试功能，确保PC可以连接到手机。

可以输入adb命令来测试连接情况，如下所示：
```angular2html
adb devices -l
```

如果出现类似如下结果，这就说明PC已经正确连接手机。
```angular2html
List of devices attached
2da42ac0 device usb:336592896X product:leo model:MI_NOTE_Pro device:leo
```

model是设备的名称，就是后文需要用到的deviceName变量。我使用的是小米Note顶配版，所以此处名称为MI_NOTE_Pro。

接下来用Appium内置的驱动器打开App，点击Appium中的Start New Session按钮

这时会出现一个配置页面

需要配置启动App时的Desired Capabilities参数，它们分别是platformName、deviceName、appPackage、appActivity。
- platformName：它是平台名称，需要区分Android或iOS，此处填写Android。
- deviceName：它是设备名称，此处是手机的具体类型。
- appPackage：它是App程序包名。
- appActivity：它是入口Activity名，这里通常需要以 . 开头。

我们在Appium中加入上面4个配置，如下图所示。
![](../images/1.png)

appPackage可以从如下找到(先开模拟器点开需要抓取的应用找到package即可)：
![](../images/2.png)

点击保存按钮，保存下来，我们以后可以继续使用这个配置。

点击右下角的Start Session按钮，即可启动Android手机上的微信App并进入到启动页面。同时PC上会弹出一个调试窗口，从这个窗口我们可以预览当前手机页面，并可以查看页面的源码，如下图所示。

点击左栏中屏幕的某个元素，如选中登录按钮，它就会高亮显示。这时中间栏就显示了当前选中的按钮对应的源代码，右栏则显示了该元素的基本信息，如元素的id、class、text等，以及可以执行的操作，如Tap、Send Keys、Clear，如下图所示。

## mac adb无法识别海马玩模拟器解决方法
```angular2html
mac上用这个ip:

 adb connect 192.168.56.101
```

### 点击
点击可以使用tap()方法，该方法可以模拟手指点击（最多五个手指），可设置按时长短（毫秒），代码如下所示：
```angular2html
tap(self, positions, duration=None)
```

其中后两个参数如下。
- positions：它是点击的位置组成的列表。
- duration：它是点击持续时间。

eg:
```angular2html
driver.tap([(100, 20), (100, 60), (100, 100)], 500)
```
这样就可以模拟点击屏幕的某几个点。

### 屏幕拖动
可以使用scroll()方法模拟屏幕滚动，用法如下所示：
```angular2html
scroll(self, origin_el, destination_el)
```

可以实现从元素origin_el滚动至元素destination_el。

它的后两个参数如下。
- original_el：它是被操作的元素。
- destination_el：它是目标元素。

eg: 
```angular2html
driver.scroll(el1,el2)
```
可以使用swipe()模拟从A点滑动到B点，用法如下所示：
```angular2html
swipe(self, start_x, start_y, end_x, end_y, duration=None)
```

后面几个参数说明如下
- start_x：它是开始位置的横坐标。
- start_y：它是开始位置的纵坐标。
- end_x：它是终止位置的横坐标。
- end_y：它是终止位置的纵坐标。
- duration：它是持续时间，单位是毫秒。

eg: 
```angular2html
driver.swipe(100, 100, 100, 400, 5000)
```
这样可以实现在5s时间内，由(100, 100)滑动到 (100, 400)。

可以使用flick()方法模拟从A点快速滑动到B点，用法如下所示：
```angular2html
flick(self, start_x, start_y, end_x, end_y)
```
几个参数说明如下。
- start_x：它是开始位置的横坐标。
- start_y：它是开始位置的纵坐标。
- end_x：它是终止位置的横坐标。
- end_y：它是终止位置的纵坐标。

eg:
```angular2html
driver.flick(100, 100, 100, 400)
```

### 文本输入
可以使用set_text()方法实现文本输入，如下所示：
```angular2html
el = find_element_by_id('com.tencent.mm:id/cjk')
el.set_text('Hello')
```

### 动作链
与Selenium中的ActionChains类似，Appium中的TouchAction可支持的方法有tap()、press()、long_press()、release()、move_to()、wait()、cancel()等，实例如下所示：
```angular2html
el = self.driver.find_element_by_accessibility_id('Animation')
action = TouchAction(self.driver)
action.tap(el).perform()
```

首先选中一个元素，然后利用TouchAction实现点击操作。

如果想要实现拖动操作，可以用如下方式：
```angular2html
els = self.driver.find_elements_by_class_name('listView')
a1 = TouchAction()
a1.press(els[0]).move_to(x=10, y=0).move_to(x=10, y=-75).move_to(x=10, y=-600).release()
a2 = TouchAction()
a2.press(els[1]).move_to(x=10, y=10).move_to(x=10, y=-300).move_to(x=10, y=-600).release()
```

#### 利用以上API，我们就可以完成绝大部分操作。更多的API操作可以参考：https://testerhome.com/topics/3711。

