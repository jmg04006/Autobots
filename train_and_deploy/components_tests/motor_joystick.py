import pygame
from pygame.locals import *
from pygame import event, display, joystick
from gpiozero import PhaseEnableMotor

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

throttle = 0
try:
    while(True):
        for e in pygame.event.get():
            if e.type == pygame.JOYAXISMOTION:
                throttle = -js.get_axis(1)  # throttle input: -1: max forward, 1: max backward
                print(throttle)
                if (throttle < 0.05 and throttle > -0.05):
                    motor.stop()
                elif (throttle > 0.05):
                    motor.foward(throttle)
                elif (throttle < -0.05):
                    motor.backward(throttle)

    # motor = PhaseEnableMotor(phase=19, enable=26)
    # for i in range(100):
    #     motor.forward(i*0.01)
    #     print(f"Forward at {i*0.01}")
    #     sleep(0.2)
    # for i in reversed(range(100)):
    #     motor.forward(i*0.01)
    #     print(f"Forward at {i*0.01}")
    #     sleep(0.2)
    # print("Stop")
    # motor.stop()
    # sleep(1)
    # for i in range(100):
    #     motor.backward(i*0.01)
    #     print(f"Backward at {i*0.01}")
    #     sleep(0.2)
    # for i in reversed(range(100)):
    #     motor.backward(i*0.01)
    #     print(f"Backward at {i*0.01}")
    #     sleep(0.2)
except KeyboardInterrupt:
    motor.stop()
    motor.close()
    print("Test interrupted!")

    motor.stop()
    motor.close()
    print("Test completed!")
# while True:
#     for e in event.get():
#         if e.type == JOYAXISMOTION:
#             print(e)