# coding:utf-8

'''
@author = super_fazai
@File    : login.py
@connect : superonesfazai@gmail.com
'''

"""
适用于网易云盾滑动验证码破解
"""

from PIL import Image
from gc import collect
from fzutils.spider.fz_driver import (
    BaseDriver,
    PHONE,
    FIREFOX,
    CHROME,)
from fzutils.img_utils import save_img_through_url
from fzutils.spider.selenium_always import *
from fzutils.ocr_utils import (
    get_tracks_based_on_distance,
    dichotomy_match_gap_distance,)

FIREFOX_DRIVER_PATH = '/Users/afa/myFiles/tools/geckodriver'

class CrackSlider():
    """
    通过浏览器截图，识别验证码中缺口位置，获取需要滑动距离，并模仿人类行为破解滑动验证码
    """
    def __init__(self):
        super(CrackSlider, self).__init__()
        # 实际地址
        # self.url = 'http://dun.163.com/trial/jigsaw'
        self.url = 'https://m.yiuxiu.com/Activity/GuidePage?ReturnUrl=https%3a%2f%2fm.yiuxiu.com%2fUser%2fAccountManage'
        self.driver = webdriver.Firefox(executable_path=FIREFOX_DRIVER_PATH)
        # self.driver = BaseDriver(
        #     type=FIREFOX,
        #     executable_path=FIREFOX_DRIVER_PATH,
        #     driver_use_proxy=True,
        #     user_agent_type=PHONE,
        #     headless=False,
        #     load_images=True,).driver
        # self.driver = _._get_driver()
        self.wait = WebDriverWait(self.driver, 20)
        self.zoom = 1
        self.save_bg_img_path = './images/bg.png'
        self.save_slide_img_path = './images/slide.png'

    def _before_act(self):
        '''
        未出现滑动验证码前的行为集合(可重载)
        :return:
        '''
        self.driver.get(self.url)
        self.driver.find_element_by_id('yzmRadio').click()
        self.driver.find_element_by_id("phone2").send_keys('18698570079')
        sleep(1)
        self.driver.find_element_by_id("getYZM").send_keys(Keys.ENTER)
        sleep(1)

        return

    def crack_slider(self,
                     before_text_css_selector='yidun_tips__text',
                     before_text_content='向右滑动滑块填充拼图',
                     last_move_x=-6):
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
        tracks = get_tracks_based_on_distance((distance + 7 ) * self.zoom)       # 对位移的缩放计算
        print(tracks)
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'yidun_slider')))
        ActionChains(self.driver).click_and_hold(slider).perform()

        for track in tracks['forward_tracks']:
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()

        sleep(0.5)
        for back_tracks in tracks['back_tracks']:
            ActionChains(self.driver).move_by_offset(xoffset=back_tracks, yoffset=0).perform()

        sleep(1)
        # 下面用于最后的微调, 可修改
        ActionChains(self.driver).move_by_offset(xoffset=last_move_x, yoffset=0).perform()
        # ActionChains(self.driver).move_by_offset(xoffset=1, yoffset=0).perform()
        sleep(0.5)
        ActionChains(self.driver).release().perform()
        try:    # 验证是否成功!
            failure = self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, before_text_css_selector), before_text_content))
            print(failure)
        except:
            print('验证成功')
            return None

        if failure:
            self.crack_slider()

    def get_slide_captcha_img(self,
                              bg_css_selector='yidun_jigsaw',
                              slide_css_selector='yidun_bg-img') -> None:
        sleep(2)
        bg = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, bg_css_selector)))
        slide = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, slide_css_selector)))
        slide_url = slide.get_attribute('src')
        bg_url = bg.get_attribute('src')
        print('背景:{}'.format(bg_url))
        print('滑块:{}'.format(slide_url))

        save_img_through_url(img_url=bg_url, save_path=self.save_bg_img_path)
        save_img_through_url(img_url=slide_url, save_path=self.save_slide_img_path)
        size_orign = slide.size
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
    c = CrackSlider()
    c.crack_slider()