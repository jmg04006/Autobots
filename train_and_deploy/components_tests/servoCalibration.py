from gpiozero import AngularServo
from time import sleep

servo = AngularServo(17, min_angle=-130, max_angle=130)

i = -130

while True:
    servo.angle = i
    print (i)
    sleep(3)
    i += 5
    if (i > 130):
        break

