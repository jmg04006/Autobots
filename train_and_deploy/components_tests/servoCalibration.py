from gpiozero import AngularServo
from time import sleep

servo = AngularServo(17, min_angle=0, max_angle=180)

i = 0

for ang in range(181):
    servo.angle = ang
    print (ang)
    sleep(1)

# while True:
#     servo.angle = i
#     print (i)
#     sleep(1)
#     i += 5
#     if (i > 130):
#         break

