#Get camera and joystick to work together

#!/usr/bin/python3
import sys
import os
import cv2 as cv
import pygame
import time
import json
from time import time

# SETUP

# init controller
pygame.display.init()
pygame.joystick.init()
js = pygame.joystick.Joystick(0)
# init variables
throttle, steer = 0., 0.

# init camera
cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FPS, 20)
for i in reversed(range(60)):
    if not i % 20:
        print(i/20)
    ret, frame = cap.read()
# init timer
start_stamp = time()
frame_counts = 0
ave_frame_rate = 0.

try:

    while True:
        ret, frame = cap.read()
        #Start camera
        cv2.imshow("Camera", frame)
        for e in pygame.event.get():
            if e.type == pygame.JOYAXISMOTION:
                throttle = -round((js.get_axis(1)), 2)  # throttle input: -1: max forward, 1: max backward
                steer = -round((js.get_axis(3)), 2)  # steer_input: -1: left, 1: right
            
        action = [steer, throttle]
        print(f"action: {action}")
        frame_counts += 1
        duration_since_start = time() - start_stamp
        ave_frame_rate = frame_counts / duration_since_start
        # print(f"frame rate: {ave_frame_rate}")
        if cv.waitKey(1)==ord('q'):
            cv.destroyAllWindows()
            pygame.quit()
            sys.exit()
except KeyboardInterrupt:
    cv.destroyAllWindows()
    pygame.quit()
    sys.exit()