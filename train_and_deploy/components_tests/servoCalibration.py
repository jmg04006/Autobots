from gpiozero import AngularServo
from time import sleep

servo = AngularServo(17, min_angle=-100, max_angle=100)

i = -100

while True:
    servo.angle = i
    print (i)
    sleep(3)
    i += 5
    if (i > 100):
        break

