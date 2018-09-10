# coding:utf-8

'''
@author = super_fazai
@File    : demo_3.py
@Time    : 2017/7/10 15:28
@connect : superonesfazai@gmail.com
'''

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
import time
import gc

def _init_chrome(is_headless=True, is_pic=True, is_proxy=True):
    '''
    如果使用chrome请设置page_timeout=30
    :return:
    '''
    from selenium.webdriver.support import ui

    CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'
    print('--->>>初始化chrome驱动中<<<---')
    chrome_options = webdriver.ChromeOptions()
    if is_headless:
        chrome_options.add_argument('--headless')     # 注意: 设置headless无法访问网页
    # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')  # required when running as root user. otherwise you would get no sandbox errors.

    # chrome_options.add_argument('window-size=1200x600')   # 设置窗口大小

    # 设置无图模式
    if is_pic:
        prefs = {
            'profile.managed_default_content_settings.images': 2,
        }
        chrome_options.add_experimental_option("prefs", prefs)

    # 设置代理
    if is_proxy:
        ip_object = MyIpPools()
        proxy_ip = ip_object._get_random_proxy_ip().replace('http://', '') if isinstance(ip_object._get_random_proxy_ip(), str) else ''
        if proxy_ip != '':
            chrome_options.add_argument('--proxy-server={0}'.format(proxy_ip))

    '''无法打开https解决方案'''
    # 配置忽略ssl错误
    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    # 修改user-agent
    chrome_options.add_argument('--user-agent={0}'.format(user_agent))

    # 忽视证书错误
    chrome_options.add_experimental_option('excludeSwitches', ['ignore-certificate-errors'])

    driver = webdriver.Chrome(
        executable_path=CHROME_DRIVER_PATH,
        chrome_options=chrome_options,
        desired_capabilities=capabilities
    )
    wait = ui.WebDriverWait(driver, 30)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
    print('------->>>初始化完毕<<<-------')

    return driver

def get_snap(driver):
    driver.save_screenshot('full_snap.png')
    page_snap_obj = Image.open('full_snap.png')
    return page_snap_obj


def get_image(driver):
    img = driver.find_element_by_class_name('geetest_canvas_img')
    time.sleep(2)
    location = img.location
    size = img.size

    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = top + size['height']

    page_snap_obj = get_snap(driver)
    image_obj = page_snap_obj.crop((left, top, right, bottom))
    # image_obj.show()
    return image_obj


def get_distance(image1, image2):
    start = 57
    threhold = 60

    for i in range(start, image1.size[0]):
        for j in range(image1.size[1]):
            rgb1 = image1.load()[i, j]
            rgb2 = image2.load()[i, j]
            res1 = abs(rgb1[0] - rgb2[0])
            res2 = abs(rgb1[1] - rgb2[1])
            res3 = abs(rgb1[2] - rgb2[2])
            # print(res1,res2,res3)
            if not (res1 < threhold and res2 < threhold and res3 < threhold):
                return i - 7
    return i - 7


def get_tracks(distance):
    distance += 20  # 先滑过一点，最后再反着滑动回来
    v = 0
    t = 0.2
    forward_tracks = []

    current = 0
    mid = distance * 3 / 5
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3

        s = v * t + 0.5 * a * (t ** 2)
        v = v + a * t
        current += s
        forward_tracks.append(round(s))

    # 反着滑动到准确位置
    back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]  # 总共等于-20

    return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}


def crack(driver):  # 破解滑动认证
    # 1、点击按钮，得到没有缺口的图片
    button = driver.find_element_by_class_name('geetest_radar_tip')
    button.click()

    # 2、获取没有缺口的图片
    image1 = get_image(driver)

    # 3、点击滑动按钮，得到有缺口的图片
    button = driver.find_element_by_class_name('geetest_slider_button')
    button.click()

    # 4、获取有缺口的图片
    image2 = get_image(driver)

    # 5、对比两种图片的像素点，找出位移
    distance = get_distance(image1, image2)

    # 6、模拟人的行为习惯，根据总位移得到行为轨迹
    tracks = get_tracks(distance)
    print(tracks)

    # 7、按照行动轨迹先正向滑动，后反滑动
    button = driver.find_element_by_class_name('geetest_slider_button')
    ActionChains(driver).click_and_hold(button).perform()

    # 正常人类总是自信满满地开始正向滑动，自信地表现是疯狂加速
    for track in tracks['forward_tracks']:
        ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()

    # 结果傻逼了，正常的人类停顿了一下，回过神来发现，卧槽，滑过了,然后开始反向滑动
    time.sleep(0.5)
    for back_track in tracks['back_tracks']:
        ActionChains(driver).move_by_offset(xoffset=back_track, yoffset=0).perform()

    # 小范围震荡一下，进一步迷惑极验后台，这一步可以极大地提高成功率
    ActionChains(driver).move_by_offset(xoffset=-3, yoffset=0).perform()
    ActionChains(driver).move_by_offset(xoffset=3, yoffset=0).perform()

    # 成功后，骚包人类总喜欢默默地欣赏一下自己拼图的成果，然后恋恋不舍地松开那只脏手
    time.sleep(0.5)
    ActionChains(driver).release().perform()


def login_cnblogs(username, password):
    driver = _init_chrome(is_headless=False, is_pic=False, is_proxy=False)
    try:
        # 1、输入账号密码回车
        driver.implicitly_wait(3)
        driver.get('https://passport.cnblogs.com/user/signin')

        input_username = driver.find_element_by_id('input1')
        input_pwd = driver.find_element_by_id('input2')
        signin = driver.find_element_by_id('signin')

        input_username.send_keys(username)
        input_pwd.send_keys(password)
        signin.click()

        # 2、破解滑动认证
        crack(driver)

        time.sleep(10)  # 睡时间长一点，确定登录成功
    except Exception as e:
        print(e)

    finally:
        driver.close()
        gc.collect()

if __name__ == '__main__':
    login_cnblogs(username='linhaifeng', password='xxxx')

