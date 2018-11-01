# coding:utf-8

'''
@author = super_fazai
@File    : bilibili_spider.py
@connect : superonesfazai@gmail.com
'''

"""
极验滑动验证码破解之bilibili
"""

from gc import collect
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from os.path import exists
from os import mkdir
from PIL import Image
from random import uniform
from fzutils.spider.crawler import AsyncCrawler
from fzutils.spider.async_always import *
from fzutils.spider.selenium_always import *

CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'

class CrackGeetest():
    def __init__(self):
        self.url = 'https://passport.bilibili.com/login'
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        self.wait = WebDriverWait(self.driver, 10)

    def mk_img_dir(self):
        """
        创建图片目录文件
        :return:
        """
        if not exists('images'):
            mkdir('images')

    def get_geetest_image(self):
        """
        获取验证码图片
        :return: 图片location信息
        """
        bg = []
        fullgb = []
        while bg == [] and fullgb == []:
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            bg = soup.find_all('div', class_='gt_cut_bg_slice')
            fullgb = soup.find_all('div', class_='gt_cut_fullbg_slice')

        bg_url = re.findall('url\(\"(.*?)\"\);', bg[0].get('style'))[0].replace('webp', 'jpg')
        fullgb_url = re.findall('url\(\"(.*?)\"\);', fullgb[0].get('style'))[0].replace('webp', 'jpg')
        bg_location_list = []
        fullgb_location_list = []

        for each_bg in bg:
            location = {}
            location['x'] = int(re.findall('background-position: (.*)px (.*)px;', each_bg.get('style'))[0][0])
            location['y'] = int(re.findall('background-position: (.*)px (.*)px;', each_bg.get('style'))[0][1])
            bg_location_list.append(location)

        for each_fullgb in fullgb:
            location = {}
            location['x'] = int(re.findall('background-position: (.*)px (.*)px;', each_fullgb.get('style'))[0][0])
            location['y'] = int(re.findall('background-position: (.*)px (.*)px;', each_fullgb.get('style'))[0][1])
            fullgb_location_list.append(location)

        self.mk_img_dir()
        urlretrieve(url=bg_url, filename='images/bg.jpg')
        print('缺口图片下载完成！')
        urlretrieve(url=fullgb_url, filename='images/fullgb.jpg')
        print('背景图片下载完成！')

        return bg_location_list, fullgb_location_list

    def _get_merge_image(self, filename, location_list):
        """
        根据图片位置合并还原
        :param filename: 图片
        :param location: 位置
        :return:合并后的图片对象
        """
        im = Image.open(filename)
        new_im = Image.new('RGB',(260,116))
        im_list_upper = []
        im_list_lower = []

        for location in location_list:
            if location['y'] == -58:
                im_list_upper.append(im.crop((abs(location['x']), 58, abs(location['x'])+10,116)))
            if location['y'] == 0:
                im_list_lower.append(im.crop((abs(location['x']), 0, abs(location['x'])+10,58)))

        x_offset = 0
        for img in im_list_upper:
            new_im.paste(img, (x_offset, 0))
            x_offset+=img.size[0]

        x_offset = 0
        for img in im_list_lower:
            new_im.paste(img, (x_offset, 58))
            x_offset+=img.size[0]

        new_im.save('images/' + re.split('[./]', filename)[1] + '1.jpg')

        return new_im

    def is_px_equal(self, img1, img2, x, y):
        """
        判断两个像素是否相同
        :param img1: 图片1
        :param img2:图片2
        :param x:位置1
        :param y:位置2
        :return:像素是否相同
        """
        pix1 = img1.load()[x,y]
        pix2 = img2.load()[x,y]
        threshold = 60

        if abs(pix1[0]-pix2[0]) < threshold and abs(pix1[1]-pix2[1]) < threshold and abs(pix1[2]-pix2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self, img1, img2):
        """
        获取缺口偏移量
        :param img1: 不带缺口图片
        :param img2: 带缺口图片
        :return:
        """
        left = 60
        for i in range(left, img1.size[0]):
            for j in range(img1.size[1]):
                if not self.is_px_equal(img1, img2, i, j):
                    left = i
                    return left

        return left

    def get_track(self, distance):
        """
        根据偏移量和手动操作模拟计算移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        tracks = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 时间间隔
        t = 0.2
        # 初始速度
        v = 0
        while current < distance:
            if current < mid:
                a = uniform(2, 5)
            else:
                a = -(uniform(12.5, 13.5))
            v0 = v
            v = v0 + a * t
            x = v0 * t + 1 / 2 * a * t * t
            current += x

            if 0.6 < current - distance < 1:
                x = x - 0.53
                tracks.append(round(x, 2))

            elif 1 < current - distance < 1.5:
                x = x - 1.4
                tracks.append(round(x, 2))
            elif 1.5 < current - distance < 3:
                x = x - 1.8
                tracks.append(round(x, 2))

            else:
                tracks.append(round(x, 2))

        return tracks

    def get_slider(self):
        """
        获取滑块
        :return:滑块对象
        """
        try:
            slider = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="gt_slider"]/div[contains(@class,"gt_slider_knob")]')))
            return slider
        except TimeoutError:
            print('加载超时...')

    def move_to_gap(self, slider, tracks):
        """
        将滑块移动至偏移量处
        :param slider: 滑块
        :param tracks: 移动轨迹
        :return:
        """
        action = ActionChains(self.driver)
        action.click_and_hold(slider).perform()
        for x in tracks:
            action.move_by_offset(xoffset=x,yoffset=-1).perform()
            action = ActionChains(self.driver)
        sleep(0.6)
        action.release().perform()

    def success_check(self):
        """
        验证是否成功
        :return:
        """
        try:
            if re.findall('gt_success', self.driver.page_source, re.S):
                print('验证成功！')
                return True
            else:
                print('验证失败！')
                return False
        except TimeoutError:
            print('加载超时...')
        finally:
            self.driver.close()
            
    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
        collect()

class BiliBiliSpider(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(self, *params, **kwargs)

    async def _login(self):
        while True:
            try:
                check = CrackGeetest()
                check.driver.get(check.url)
                bg_location_list, fullgb_location_list = check.get_geetest_image()
                img1 = check._get_merge_image('images/fullgb.jpg', fullgb_location_list)
                img2 = check._get_merge_image('images/bg.jpg', bg_location_list)
                # distance应根据实际情况做微调
                distance = check.get_gap(img1, img2) * 1.138
                slider = check.get_slider()
                tracks = check.get_track(distance)
                check.move_to_gap(slider, tracks)
                sleep(0.5)
                CHECK = check.success_check()
                if CHECK == True:
                    break
            except Exception as e:
                print(e)

        return True

    async def _download_movie(self):
        '''
        下载视频到本地
        :return:
        '''
        headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        url = ''
        res = Requests._download_file(url=url, file_save_path='/Users/afa/Desktop/github/bili.mp4', headers=headers,)

    async def _get_movie_url_info(self):
        '''
        获取movie url的info
        :return:
        '''
        # pc 的视频在playurl这个接口中
        pass

    async def _fck_run(self):
        # login_res = await self._login()
        await self._download_movie()

    def __del__(self):
        collect()

if __name__ == '__main__':
    _ = BiliBiliSpider()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())
