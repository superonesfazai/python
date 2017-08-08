# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-25 下午5:00
# @File    : write_my_name.py

import turtle
# import curses.panel

class WriteMyName(object):
    def __init__(self):
        super().__init__()
        turtle.setup(width=600, height=600, startx=0, starty=0)
        turtle.title('练字格')
        turtle.speed(6)

    def write_table(self):
        # 绘制x-y轴, 用于后期对称绘字
        turtle.setx(-600)
        turtle.setx(600)
        turtle.home()
        turtle.sety(-600)
        turtle.sety(600)
        turtle.home()
        turtle.dot('red')

        turtle.seth(135)
        turtle.setpos(-600, 600)

        turtle.home()
        turtle.seth(45)
        turtle.setpos(600, 600)

        turtle.home()
        turtle.seth(45)
        turtle.setpos(600, -600)

        turtle.home()
        turtle.seth(45)
        turtle.setpos(-600, -600)

        turtle.home()
        print(turtle.xcor())  # xcor()   return x的位置
        print(turtle.ycor())
        # turtle.forward(20)        # forward(distance) 移动distance的距离

        turtle.up()     # 移到某位值而不绘制路线
        turtle.goto(20, 30)

        turtle.bgcolor('orange')
        turtle.mainloop()


_w = WriteMyName()
_w.write_table()
