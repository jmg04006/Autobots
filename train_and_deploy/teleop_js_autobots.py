#import necessary libraries 
import pygame
from pygame.locals import *
from pygame import event, display, joystick
from gpiozero import PhaseEnableMotor
from gpiozero import AngularServo
import json
import sys
import os 

#Check to make sure robot is in a suitable space for testing
is_lifted = input("Is any tire having contact with the ground or other objects? [yes/no]")
assert is_lifted=="no"
is_ready = input("Are you ready to start motor test? [yes/no]")
assert is_ready=="yes"


def get_numControllers():
    return joystick.get_count()

display.init()
joystick.init()
print(f"{get_numControllers()} joystick connected")
#Create an instance of the joystick object
js = joystick.Joystick(0)
pygame.display.init()
pygame.joystick.init()

# load configs
config_path = os.path.join(sys.path[0], "config.json")
f = open(config_path)
data = json.load(f)
steering_center = data['steering_center']
steering_range = data['steering_range']

#Create an instance of the motor and servo objects 
motor = PhaseEnableMotor(phase=19, enable=26)
servo = AngularServo(17, min_angle=-90, max_angle=90)

#Assign default value of 0 for the motor PWM and the steering angle 
throttle = 0
steer = 0
try:
    while(True):
        for e in pygame.event.get():
            if e.type == pygame.JOYAXISMOTION:
                #Get joystick throttle value from joystick and save it to a variable 
                throttle = -js.get_axis(1)  # throttle input: -1: max forward, 1: max backward
                #Get joystick steeing angle value from joystick and save it to a variable 
                steer = -js.get_axis(3)  # steer_input: -1: left, 1: right

                #Conditions for throttling the motor 
                if (throttle < 0.05 and throttle > -0.05):
                    motor.stop()
                elif (throttle > 0.05):
                    motor.forward(throttle)
                elif (throttle < -0.05):
                    motor.backward(-throttle)
                #Conditions for steering the servo
                ang = steering_center + steer * steering_range
                servo.angle = ang



except KeyboardInterrupt:
    motor.stop()
    motor.close()
    print("Test interrupted!")

    motor.stop()
    motor.close()
    print("Test completed!")