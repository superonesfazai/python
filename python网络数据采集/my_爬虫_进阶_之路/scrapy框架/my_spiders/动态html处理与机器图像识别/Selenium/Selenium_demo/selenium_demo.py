# coding = utf-8

'''
@author = super_fazai
@File    : selenium_demo.py
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver      # 导入webdriver
# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys

# 调用环境变量指定的PhantomJS浏览器创建浏览对象
driver = webdriver.PhantomJS()

# 如果没有在环境变量设置指定PhantomJS位置
# driver = webdriver.PhantomJS(executable_path="./phantomjs"))

# get会等页面加载完毕才继续执行,通常测试会在这里选择time.sleep(2), 即为阻塞状态
driver.get('http://www.baidu.com/')

# 获取页面名为wrapper的id标签的文本内容
data = driver.find_element_by_id('wrapper').text

print(data)
# 打印页面标题 "百度一下, 你就知道"
print(driver.title)

# 生成当前页面快照并保存
driver.save_screenshot('baidu.png')

# id="kw"是百度搜索输入框, 输入字符串"长城"
driver.find_element_by_id('kw').send_keys('长城')

# id="su"是百度搜素按钮, click()是模拟点击
# TODO 注意：定位准确，但是当.click()失效时，推荐使用.send_keys(Keys.ENTER)
# driver.find_element_by_id('su').click()
from selenium.webdriver.common.keys import Keys
driver.find_element_by_id('su').send_keys(Keys.ENTER)

# 获取新的页面快照
driver.save_screenshot('长城.png')

# 打印页面渲染后的源代码
print(driver.page_source)

# 获取当前页面的cookies
print(driver.get_cookies())

# ctrl+a全选输入框内容
driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'a')

# ctrl+x 剪切输入框内容
driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'x')

# 输入框重新输入内容
driver.find_element_by_id('kw').send_keys('阿发')

# 模拟enter回车键
driver.find_element_by_id('su').send_keys(Keys.RETURN)

# 清除输入框内容
driver.save_screenshot('kw').clear()

# 生成新的页面快照
driver.save_screenshot('阿发.png')

# 获取当前url
print(driver.current_url)

# 关闭当前页面，如果只有一个页面，会关闭浏览器
# driver.close()

# 关闭浏览器
driver.quit()