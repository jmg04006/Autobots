from gpiozero import AngularServo
from time import sleep

servo = AngularServo(17, min_angle=-90, max_angle=90)

i = 0

for ang in range(-90, 91, 5):
    servo.angle = ang
    print (ang)
    sleep(.5)

# while True:
#     servo.angle = i
#     print (i)
#     sleep(1)
#     i += 5
#     if (i > 130):
#         break

