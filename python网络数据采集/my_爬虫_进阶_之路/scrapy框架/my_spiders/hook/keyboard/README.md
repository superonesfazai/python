# keyboard
使用这个小型Python库完全控制您的键盘。挂钩全局事件，注册热键，模拟按键等等。

[github](https://github.com/boppreh/keyboard)

[doc](https://github.com/boppreh/keyboard#api)

## 安装
`pip3 install keyboard`

## 特征
- 所有键盘上的全局事件挂钩（无论焦点如何都捕获键）。
- 收听并发送键盘事件。
- 适用于Windows和Linux（需要sudo），支持实验性OS X
- 纯Python，没有要编译的C模块。
- 零依赖。安装和部署很简单，只需复制文件即可。
- Python 2和3。
- ctrl+shift+m, ctrl+space具有可控超时的复杂热键支持（例如）。
- 包括高级API（例如记录和播放，add_abbreviation）。
- 映射键实际上位于您的布局中，具有完全的国际化支持（例如Ctrl+ç）。
- 事件自动在单独的线程中捕获，不会阻塞主程序。
- 经过测试和记录。
- 不打破重音死键（我在看你，pyHook）。
- 通过项目鼠标（pip install mouse）提供鼠标支持。