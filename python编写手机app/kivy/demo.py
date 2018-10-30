# coding:utf-8

'''
@author = super_fazai
@File    : tasks.py
@Time    : 2017/2/16 17:44
@connect : superonesfazai@gmail.com
'''

from kivy.app import App
from kivy.uix.button import Button

class DemoApp(App):
    def build(self):
        return Button(text='hello, kivy!')

if __name__ == '__main__':
    DemoApp().run()