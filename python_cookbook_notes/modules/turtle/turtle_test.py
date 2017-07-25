# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-25 下午4:12
# @File    : turtle_test.py

import turtle
import time

print(turtle.position())
turtle.setx(10)
turtle.sety(10)
print(turtle.position())
print(turtle.xcor(), turtle.ycor())

turtle.home()
turtle.seth(90)        # 角度, 顺时针开始
turtle.forward(200)
turtle.setx(-200)
turtle.sety(-200)
# turtle.setx(400)

turtle.home()

# turtle.setx(-200)
# turtle.sety(-200)
# turtle.setposition(-200, -200)
turtle.goto(-150, -150)
print(turtle.towards(-200, -200))      # 返回两点之间的角度
turtle.pensize(10)
turtle.pencolor('green')
turtle.speed(1)

turtle.circle(20)

turtle.dot(20, 'red')
turtle.pensize(1)
turtle.pencolor('black')
turtle.speed('normal')
time.sleep(2)

turtle.home()
turtle.pensize(1)
turtle.dot()
turtle.fd(50)
turtle.dot(20, 'blue')
turtle.fd(50)
time.sleep(2)

turtle.mainloop()
turtle.clear()
time.sleep(1)


