from gpiozero import AngularServo
from time import sleep

servo = AngularServo(17, min_angle=-100, max_angle=100)

while True:
    i = -100
    servo.angle = i
    i += i + 5
    print (i)
    sleep(3)
    if (i > 100):
        break

