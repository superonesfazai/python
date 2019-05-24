# poium
基于 selenium/appium 的 Page Objects 设计模式测试库。

完全兼容原生selenium/appium API。
提供了一组基于JavaScript的API，实现部分selenium 不支持的操作。

[github](https://github.com/defnngj/poium)

## example
```python
from poium import Page, PageElement
from selenium import webdriver


class BaiduIndexPage(Page):
    search_input = PageElement(css='#kw')
    search_button = PageElement(css='#su')


driver = webdriver.Chrome()

page = BaiduIndexPage(driver)
page.get("https://www.baidu.com")

page.search_input = "poium"
page.search_button.click()

driver.quit()
```

```python
from poium import Page, PageElement
from appium import webdriver

class CalculatorPage(Page):
    number_1 = PageElement(id_="com.android.calculator2:id/digit_1")
    number_2 = PageElement(id_="com.android.calculator2:id/digit_2")
    add = PageElement(id_="com.android.calculator2:id/op_add")
    eq = PageElement(id_="com.android.calculator2:id/eq")

# APP定义运行环境
desired_caps = {
    'deviceName': 'Android Emulator',
    'automationName': 'appium',
    'platformName': 'Android',
    'platformVersion': '7.0',
    'appPackage': 'com.android.calculator2',
    'appActivity': '.Calculator',
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

page = CalculatorPage(driver)
page.number_1.click()
page.add.click()
page.number_2.click()
page.eq.click()

driver.quit()
```