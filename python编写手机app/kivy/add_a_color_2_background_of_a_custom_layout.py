# coding:utf-8

'''
@author = super_fazai
@File    : add_a_color_2_background_of_a_custom_layout.py
@Time    : 2017/2/16 18:13
@connect : superonesfazai@gmail.com
'''

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_string('''
<CustomLayout>
    canvas.before:
        Color:
            rgba: 0, 1, 0, 1
        Rectangle:
            pos: self.pos
            size: self.size

<RootWidget>
    CustomLayout:
        AsyncImage:
            source: 'http://img.ivsky.com/img/bizhi/slides/201805/03/siamese-005.jpg'
            size_hint: 1, .5
            pos_hint: {'center_x':.5, 'center_y': .5}
    AsyncImage:
        source: 'http://img.ivsky.com/img/bizhi/slides/201805/10/the_incredibles_2.jpg'
    CustomLayout
        AsyncImage:
            source: 'http://img.ivsky.com/img/bizhi/co/201804/28/pubg-004.jpg'
            size_hint: 1, .5
            pos_hint: {'center_x':.5, 'center_y': .5}
''')

class RootWidget(BoxLayout):
    pass

class CustomLayout(FloatLayout):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    MainApp().run()