# import pygame
from pygame.locals import *
from pygame import event, display, joystick
from time import sleep


def get_numControllers():
    return joystick.get_count()

display.init()
joystick.init()
print(f"{get_numControllers()} joystick connected")
js = joystick.Joystick(0)
while True:
    for e in event.get():
        if e.type == JOYAXISMOTION:
            print(-js.get_axis(1))
    sleep(.5)

