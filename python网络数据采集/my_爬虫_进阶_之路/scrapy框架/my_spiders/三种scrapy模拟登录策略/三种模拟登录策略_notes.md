#### 注意: 模拟登录时, 必须保证settings.py里的COOKIES_ENABLED(Cookies中间件)处于开启状态
```python
COOKIES_ENABLED = True 
# 或 
# COOKIES_ENABLED = False
```

### 策略一: 直接post数据(比如需要登录的账户信息)
```python
只要是需要提供post数据的, 就可以用这种方法
```
(post的数据可以是账户密码)

### 策略二: 标准的模拟登录步骤
```python
正统模拟登录方法:
    1. 要想实现登录就需要表单提交, 查看登录页, 然后使用浏览器调试工具来得到登录时需要提交什么东西!
    2. 然后发送登录页面的get请求, 获取到页面里的登录必须的参数(比如说zhihu登录界面的_xsrf)
    3. 然后和账户密码一起post到服务器, 登录成功
```

### 策略三: 直接使用保存在登录状态的cookies模拟登录
```python
如果实在没办法了, 可用这种方法模拟登录, 虽然麻烦一点, 但是成功率100%
```
```
切记：先把从浏览器copy的cookies转换为能被python使用的dict
```

