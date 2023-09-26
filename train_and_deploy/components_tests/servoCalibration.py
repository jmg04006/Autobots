from gpiozero import AngularServo
from time import sleep

servo = AngularServo(17, min_angle=-90, max_angle=90)

while True:
    i = -100
    servo.angle = i
    i += i + 5
    print (i)
    sleep(3)

