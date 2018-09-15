# coding:utf-8

'''
@author = super_fazai
@File    : login.py
@connect : superonesfazai@gmail.com
'''

"""
模拟登陆qq邮箱m站
    滑动验证码之暴力破解版
"""

from PIL import Image
from gc import collect

from fzutils.img_utils import save_img_through_url
from fzutils.spider.selenium_always import *
from fzutils.ocr_utils import (
    get_tracks_based_on_distance,
    dichotomy_match_gap_distance,)

CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'

class QQMailLogin(object):
    '''qq m站登陆'''
    def __init__(self):
        self.url = 'https://ui.ptlogin2.qq.com/cgi-bin/login?style=9&appid=522005705&daid=4&s_url=https%3A%2F%2Fw.mail.qq.com%2Fcgi-bin%2Flogin%3Fvt%3Dpassport%26vm%3Dwsk%26delegate_url%3D%26f%3Dxhtml%26target%3D&hln_css=http%3A%2F%2Fmail.qq.com%2Fzh_CN%2Fhtmledition%2Fimages%2Flogo%2Fqqmail%2Fqqmail_logo_default_200h.png&low_login=1&hln_autologin=%E8%AE%B0%E4%BD%8F%E7%99%BB%E5%BD%95%E7%8A%B6%E6%80%81&pt_no_onekey=1'
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        self.wait = WebDriverWait(self.driver, 20)
        self.zoom = 1
        self.save_bg_img_path = './images/bg.png'
        self.save_slide_img_path = './images/slide.png'

    def _before_act(self):
        self.driver.get(self.url)
        sleep(5)
        self.driver.find_element_by_id("u").clear()
        self.driver.find_element_by_id("p").clear()
        self.driver.find_element_by_id('u').send_keys('2939161688@qq.com')      # 故意输错, 强制出现滑动验证码, 并暴力破解之
        self.driver.find_element_by_id('p').send_keys('xxxxxxxx')
        self.driver.find_element_by_id('go').click()
        sleep(3)

        return

    def crack_slider(self,
                     before_text_css_selector='yidun_tips__text',
                     before_text_content='向右滑动滑块填充拼图',
                     last_move_x=0):
        '''
        模拟拖动滑块
        :param before_text_css_selector: 滑块未被拖动前其中文字的css选择器
        :param before_text_content: 该文字的内容
        :param last_move_x: 最后的x方向微调距离
        :return:
        '''
        self._before_act()
        self.get_slide_captcha_img()
        distance = dichotomy_match_gap_distance(
            bg_img_path=self.save_bg_img_path,
            slide_img_path=self.save_slide_img_path,)
        new_distance = (distance + 7) * self.zoom * .2
        if new_distance > 198 or new_distance < 32:
            print('new_distance: {}, 未在执行范围跳过!'.format(float(new_distance).__round__(2)))
            self.crack_slider()

        print('new_dictance: {}'.format(new_distance))
        tracks = get_tracks_based_on_distance(new_distance)       # 对位移的缩放计算
        # print(tracks)
        slider = self.wait.until(EC.element_to_be_clickable((By.ID, 'tcaptcha_drag_thumb')))
        ActionChains(self.driver).click_and_hold(slider).perform()

        for track in tracks['forward_tracks']:
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()

        sleep(.5)
        for back_tracks in tracks['back_tracks']:
            ActionChains(self.driver).move_by_offset(xoffset=back_tracks, yoffset=0).perform()

        sleep(1)
        # 下面用于最后的微调, 可修改
        ActionChains(self.driver).move_by_offset(xoffset=last_move_x, yoffset=0).perform()
        sleep(0.5)
        ActionChains(self.driver).release().perform()
        sleep(1.5)
        before_url = self.driver.current_url
        if before_url != self.driver.current_url:
            print('验证成功')
        else:
            self.crack_slider()

    def get_slide_captcha_img(self,
                              bg_css_selector='bkBlock',
                              slide_css_selector='slideBlock') -> None:
        sleep(2)
        '''腾讯滑动验证码比较狗, 得先切换iframe'''
        # 根据id
        self.driver.switch_to.frame('tcaptcha_iframe')
        bg = self.driver.find_element_by_id(bg_css_selector)
        slide = self.driver.find_element_by_id(slide_css_selector)
        slide_url = slide.get_attribute('src')
        bg_url = bg.get_attribute('src')
        print('背景:{}'.format(bg_url))
        print('滑块:{}'.format(slide_url))

        save_img_through_url(img_url=bg_url, save_path=self.save_bg_img_path)
        save_img_through_url(img_url=slide_url, save_path=self.save_slide_img_path)
        # size_orign = slide.size
        local_img = Image.open(fp=self.save_slide_img_path)
        size_loc = local_img.size
        self.zoom = 320 / int(size_loc[0])

        return None

    def __del__(self):
        try:
            del self.driver
        except:
            pass
        collect()

if __name__ == '__main__':
    c = QQMailLogin()
    c.crack_slider()