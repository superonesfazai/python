# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-25 下午6:15
# @File    : wuziqi_test.py

import turtle
import threading
import time

screen = turtle.Screen()
pen = turtle.Pen

class WuZiQi(object):
    def __init__(self):
        super().__init__()
        screen.setup(width=450, height=450, startx=0, starty=0)
        screen.title('五子棋game')
        turtle.speed(1000000)

    def draw_table(self):
        turtle.setx(200)
        turtle.setx(-200)
        turtle.home()
        turtle.sety(200)
        turtle.sety(-200)
        turtle.home()
        turtle.dot('black')

        for i in range(0, 11):  # 11来包含边界
            pos_x = i * 20
            turtle.setx(pos_x)
            turtle.sety(200)
            turtle.sety(-200)

        turtle.up()  # 移动不绘制路线
        turtle.goto(0, 0)
        turtle.down()  # 这步为使下面的操作继续绘制路线

        for j in range(0, 11):
            pos_x = j * 20
            turtle.setx(-pos_x)
            turtle.sety(200)
            turtle.sety(-200)

        turtle.up()
        turtle.goto(0, 0)
        turtle.down()

        for k in range(0, 11):
            pos_y = k * 20
            turtle.sety(-pos_y)
            turtle.setx(200)
            turtle.setx(-200)

        turtle.up()
        turtle.goto(0, 0)
        turtle.down()

        for l in range(0, 11):
            pos_y = l * 20
            turtle.sety(pos_y)
            turtle.setx(200)
            turtle.setx(-200)

        turtle.up()
        turtle.goto(0, 0)
        turtle.down()

        # turtle.mainloop()

    def draw_dian(self):
        turtle.up()
        turtle.goto(0, 0)
        # print(turtle.xcor())
        turtle.down()

        for i in range(0, 10):  # 0 来包含x,y轴
            pos_x = i * 20
            for j in range(0, 10):
                pos_y = j * 20
                turtle.up()
                turtle.goto(pos_x, pos_y)
                # print(turtle.xcor())
                turtle.dot('black')
                turtle.down()

        turtle.up()
        turtle.goto(0, 0)
        turtle.down()

        for i in range(0, 10):
            pos_x = i * 20
            for j in range(0, 10):
                pos_y = -(j * 20)
                turtle.up()
                turtle.goto(pos_x, pos_y)
                # print(turtle.xcor())
                turtle.dot('black')
                turtle.down()

        turtle.up()
        turtle.goto(0, 0)
        turtle.down()

        for i in range(0, 10):
            pos_x = -(i * 20)
            for j in range(0, 10):
                pos_y = j * 20
                turtle.up()
                turtle.goto(pos_x, pos_y)
                # print(turtle.xcor())
                turtle.dot('black')
                turtle.down()

        turtle.up()
        turtle.goto(0, 0)
        turtle.down()

        for i in range(0, 10):
            pos_x = -(i * 20)
            for j in range(0, 10):
                pos_y = -(j * 20)
                turtle.up()
                turtle.goto(pos_x, pos_y)
                # print(turtle.xcor())
                turtle.dot('black')
                turtle.down()

        turtle.up()
        turtle.goto(0, 0)
        turtle.down()

        turtle.mainloop()


_w = WuZiQi()
_w.draw_table()
_w.draw_dian()
