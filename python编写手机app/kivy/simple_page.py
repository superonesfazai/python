# coding:utf-8

'''
@author = super_fazai
@File    : simple_page.py
@Time    : 2017/2/16 17:54
@connect : superonesfazai@gmail.com
'''

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__()
        self.cols = 2
        self.add_widget(Label(text='username:'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        self.add_widget(Label(text='password:'))
        self.passwd = TextInput(password=True, multiline=False)
        self.add_widget(self.passwd)

class MyApp(App):
    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    MyApp().run()