import pygame
from pygame.locals import *
from pygame import event, display, joystick
from gpiozero import PhaseEnableMotor
from gpiozero import AngularServo


is_lifted = input("Is any tire having contact with the ground or other objects? [yes/no]")
assert is_lifted=="no"
is_ready = input("Are you ready to start motor test? [yes/no]")
assert is_ready=="yes"

def get_numControllers():
    return joystick.get_count()

display.init()
joystick.init()
print(f"{get_numControllers()} joystick connected")
js = joystick.Joystick(0)
pygame.display.init()
pygame.joystick.init()

motor = PhaseEnableMotor(phase=19, enable=26)
servo = AngularServo(17, min_angle=-90, max_angle=90)


throttle = 0
steer = 0
try:
    while(True):
        for e in pygame.event.get():
            if e.type == pygame.JOYAXISMOTION:
                throttle = -js.get_axis(1)  # throttle input: -1: max forward, 1: max backward
                steer = -js.get_axis(3)  # steer_input: -1: left, 1: right

                print(steer)
                if (throttle < 0.05 and throttle > -0.05):
                    motor.stop()
                elif (throttle > 0.05):
                    motor.forward(throttle)
                elif (throttle < -0.05):
                    motor.backward(-throttle)

                if (steer < 0.05 and steer > -0.05):
                    servo.angle = 45
                elif (steer > 0.05):
                    servo.angle = steer * 90
                elif (steer < -0.05):
                    servo.angle = steer * 90


except KeyboardInterrupt:
    motor.stop()
    motor.close()
    print("Test interrupted!")

    motor.stop()
    motor.close()
    print("Test completed!")