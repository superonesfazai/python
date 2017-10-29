### 原理是执行js脚本进行动态添加

```python
from selenium import webdriver
driver = webdriver.PhantomJS()
driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
driver.execute('executePhantomScript', {'script': 'phantom.setProxy("10.0.0.1", 80);', 'args' : [] })
```