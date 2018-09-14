# coding:utf-8

'''
@author = super_fazai
@File    : crack.py
@connect : superonesfazai@gmail.com
'''

from gc import collect
from fzutils.spider.selenium_always import *
from fzutils.ocr_utils import get_tracks_based_on_distance

FIREFOX_DRIVER_PATH = '/Users/afa/myFiles/tools/geckodriver'

class CrackALiActCapycha(object):
    def __init__(self):
        self.url = 'https://www.chenky.com/just4fun/verification-code-test/php/aliyun'
        self.driver = webdriver.Firefox(executable_path=FIREFOX_DRIVER_PATH)
        self.wait = WebDriverWait(self.driver, 20)

    def crack_captcha(self):
        self.driver.get(self.url)
        # NO.1 先滑块拖动
        try:
            slider = self.wait.until(EC.element_to_be_clickable((By.ID, 'nc_1_n1z')))
            ActionChains(self.driver).click_and_hold(slider).perform()

            tracks = get_tracks_based_on_distance(distance=300 - 42)
            for track in tracks['forward_tracks']:
                ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()
        except (TimeoutException,) as e:
            print(e)

        sleep(.5)
        try:    # 验证是否成功!
            failure = self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'nc-lang-cnt'), '请按住滑块，拖动到最右边'))
            print(failure)
        except:
            sleep(5)
            print('验证成功')
            return None

        # NO.2 再处理文字识别然后点击

        sleep(60)

    def __call__(self, *args, **kwargs):
        return self.crack_captcha()

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
        collect()

if __name__ == '__main__':
    CrackALiActCapycha()()


