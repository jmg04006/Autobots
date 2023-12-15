# Vision-Based Autonomous Driving Using Neural Networks
> All comments are in gray.

![image0 (8)](https://github.com/jmg04006/Autobots/assets/112110593/9116daa2-f7d0-4688-be8b-25208634bf0b) 

## Project Overview 
> - You have a very good introduction on the backgrounds.
> - Briefly describe the big picture of the approach. Formats of the data, or how the model is trained is trivial in this section. You can expand the theoretical/technical details in the later section (e.g. in **Approaches**).
> - State the most notable achievement (which should be a functional protype that completed the *CCCS Clipper* track in the final race).

Our team designed a small autonomous vehicle with the goal of autonomously navigating various mazes set up throughout Lewis Science Center (LSC) and the Conway Corporation Center for Sciences (CCCS). The setup of the tracks is loosely based on two robotics competitions that last year's teams competed in:  (1) the Autonomous Vehicle Challenge at the [National Robotics Challenge](https://www.thenrc.org/) (NRC) and (2) the Intelligent Vehicle Challenge at the annual [Arkansas Space Grant Consortium](https://arkansasspacegrant.org/) (ASGC) Symposium. However, on our version of the tracks, there are multiple different variables at play that will be described below. By the end of next semester, we plan to have the ability to autonomously navigate all five possible tracks.

We created our autonomous process using vision-based supervised maching learning, and we continues the work of Team WHAM from last semester (who took inspiration from the open-source [Donkey Car](https://docs.donkeycar.com/) project. Our robot's navigational process starts with data collected when we drive it around the preset course multiple times. The bot records both images from a mounted camera and the driving command inputs, and this data is used to optimize a convolutional neural network. Then, when we start the vehicle autonomous navigation process, it will take in new images and use the previous data to determine how and where to drive the bot through a course. We are still figuring out how to fine-tune the process, but our bot has been able to effectively navigate the maze.


## Circuit Diagram
> 1. Add powerbank.
> 2. The name "Voltage Divider" is misleading, it is just a wire splitter.
> 3. The DC motor has no polarity difference.
> 4. It is better to indicate the webcam is connecting to the USB port on RPi.
> 5. If possible, indicate input/output voltage for each device.

![image0 (9)](https://github.com/jmg04006/Autobots/assets/112110593/7134de64-b7ed-44d5-8c11-16c3c8ebdef3)


## Repository Contents
> Make this section as **Project Instructions** section. You'll want to describe the workflow of collecting data, train a model, deploy the autopilot model workflow in this section. And you'll want to keep the instructions up to date.
> 1. It is essential to introduce the usage of `collect_data.py`, `train.py` and `autopilot.py`. Instructions on other scripts or directories (e.g. `component_tests`, `/data`) are welcome but not necessary.
> 2. You'll need to clean up this repository. Archive or delete files that no longer using or not compatible. No need to explain the usage of WHAM's code here.
> 3. You can include technical details here (basically, grab some of the most important techniques from your notes and the wiki pages. e.g. remote access RPi, transfer data, etc.).

This `train_and_deploy` folder contains all of the software for our autonomous vehicle, including:
- a [config.json](https://github.com/willward20/WHAM/blob/main/train_and_deploy/config.json) file that limits the vehicle's maximum throttle and defines the vehicle's steering trim;
- [motor.py](https://github.com/willward20/WHAM/blob/main/train_and_deploy/motor.py), [servo.py](https://github.com/willward20/WHAM/blob/main/train_and_deploy/servo.py), [camera.py](https://github.com/jmg04006/Autobots/blob/main/train_and_deploy/components_tests/camera.py), and [joystick.py](https://github.com/jmg04006/Autobots/blob/main/train_and_deploy/components_tests/joystick.py) are team WHAM's scripts that verify that the individual components work by themselves;
- [camera_joystick.py](https://github.com/jmg04006/Autobots/blob/main/train_and_deploy/components_tests/camera_joystick.py), [joystick_servo.py](https://github.com/jmg04006/Autobots/blob/main/train_and_deploy/components_tests/joystick_servo.py), and [motor_joystick.py](https://github.com/jmg04006/Autobots/blob/main/train_and_deploy/components_tests/motor_joystick.py) are team Autobots scripts to make sure the joytick works with the motor, servo, and camera individually. [servoCalibration.py](https://github.com/jmg04006/Autobots/blob/main/train_and_deploy/components_tests/servoCalibration.py) is an AutoBot script to make sure the servo is calibrated correctly.;
- [collect_data.py](https://github.com/willward20/WHAM/blob/main/train_and_deploy/collect_data.py) is team WHAM's script that is used to manually drive the vehicle with a wireless controller while collecting steering, throttle, and camera data. [collect_data_autobots.py](https://github.com/jmg04006/Autobots/blob/main/train_and_deploy/collect_data_autobots.py) is team Autobots version of collect data; 
- a [train.py](https://github.com/willward20/WHAM/blob/main/train_and_deploy/train.py) script that trains a CNN using PyTorch and generates a .pth autopilot file containing the trained parameters; 
- [autopilot.py](https://github.com/willward20/WHAM/blob/main/train_and_deploy/autopilot.py) is team WHAM's script that drives the vehicle autonomously using a .pth autopilot file. [autopilot_autobots.py](https://github.com/jmg04006/Autobots/blob/main/train_and_deploy/autopilot_autobots.py) is team Autobots version of autopilot using the GPIOZERO library; 
- and a [cnn_network.py](https://github.com/willward20/WHAM/blob/main/train_and_deploy/cnn_network.py) file that defines the neural network architectures accessed by the train.py and autopilot.py scripts.; 
- [teleop_js.py](https://github.com/jmg04006/Autobots/blob/main/train_and_deploy/teleop_js.py) is team WHAM's script that integrates motor, servo, and joystick functionality, so the robot can be driven manually. [teleop_js_autobots.py](https://github.com/jmg04006/Autobots/blob/main/train_and_deploy/teleop_js_autobots.py) is team Autobots version of teleop_js.


## Approaches
> Make this section as **Approaches** section. Use your knowledge learned from deep learning class to explain how the autopilot model works under the hood. Assuming you are explaining everything to high school students. Diagrams and more illustrative methods are welcome here. 

After testing several variations of CNN architectures, we had the most success with Donkey Car's [fastai](https://github.com/autorope/donkeycar/blob/main/donkeycar/parts/fastai.py) architecture (see the "Linear" class). The figure below shows how we modified the CNN structure to accomodate for our input image size and achieve the best results.  Our network architecture has five convolution layers and three fully connected layers. Each image in the network has an input size of 3x120x160 (3 color channels, 120 pixel horizontal width, and 160 pixel vertical height) and an output size of 2 prediction values: steering and throttle. When a dataset is loaded, the recorded images are split into training images (90-95% of the data) and test images (10-5%). During the training process, the network uses the Mean Square Error (MSE) loss function, Adam optimizer, a learning rate of 1E-3, and batch sizes of 125 (train) and 125 (test). The neural network iteratively trains for typically 10-20 epochs. We found the most success when using datasets with a size between 15-20k images.

<img src="https://github.com/willward20/WHAM/blob/main/media/cnn_architecture.png"/>


### Track Possibilities & Conditions
> This section could be a sub-section in the previous **Approaches** section.

#### Indoor Tracks:
- **The Basement:** LSC's basement: Large, involves one-direction turns, scenery is repetitive.
- **Office Connection:** LSC's first floor: Medium-sized, involves one-direction turns, slopes, and a narrow passage.
- **CCCS Clipper:** CCCS' main entrance: Small, involves two-direction turns, narrow passages, and sharp turns. Additionally, it needs buckets to set up.

#### Outdoor Tracks
- **Ants Nests:** CCCS' west entrance: Small, involves two-direction turns and slopes.
- **LSC Plaza:** Parking lot between LSC and Annex: Medium-sized, partially offroad, involves two-direction turns and slopes.

For our final project, we decided to navigate the CCCS' main entrance, since it incorporates the most challenges.

![cccs_clipper](https://github.com/jmg04006/Autobots/assets/112110593/8777682c-2be3-484f-b12c-3af9f5e686a5)


## Autonomous Vehicle Performance
> You can try to answer the following questions:
> 1. How much data did you collected for the final test?
> 2. How did your model look like? (size? number of parameters? etc.)
> 3. How good is your model training?
> 4. How long it took to finish a lap?
> 5. Any issues observed?

This is the [final navigation](https://youtu.be/jehrM9FV0Xk) from December 12, 2023!


## Project Conclusions
> Somehow too detailed. Please summarize only the most important milestones in this section. In my opinion, they are:
> 1. Upgraded hardware configurations (added? subtracted?)
> 2. Updated software (added? subtracted? modified?)
> 3. Performance of the final race. 

Throughout this project, we built an autonomous robot using the modified RC car and parts left by Team WHAM from last year. Then, we constructed our own vision-based neural network by taking some of WHAM's original code and instating functions of our own to ensure that the Bluetooth controller and the Raspberry Pi were functioning exactly how we wanted.  To accomplish this, we made sure that the joystick could indepently control the steering and the throttle while taking in data using a camera. Using this process, we would drive the robot around the course multiple times (around 20), to collect data, and then, we'd input the images into our neural network. Lastly, we used the data in conjunction with our _autopilot_ file in order to have the bot autonomously navigate the track. We were able to get the robot to effectively pilot itself through the maze, especially once we fixed our hardware issues.


## Goals for Next Semester
Going into next semester, there are three main avenues that we would like to explore with our robot. First, we would like to investigate the lighting factos and their influence on sensors. This could include the time of day and the angle of the sun. These effects have also been explored by team Flashfire this semester, so we should reach out to them and discuss their findings. Additionally, we would also like with more safety features, particularly a roll cage, and make sure that we are following all safety standards. Lastly, we would like to explore a new network structure for our robot's navigation training to fine tune the process and make it more accurate.


## Important Link(s)
- [Arkansas Space Grant Consortium](https://arkansasspacegrant.org/)


## Contributors
During our final year at the University of Central Arkansas, we built on the work previously done by Team [WHAM](https://github.com/willward20/WHAM) and, with guidance from Dr. Zhang, made our own adjustments to the bot. We will continue working on this senior design project until May 2024, when we are slated to graduate with B.S. in [Engineering Physics](https://uca.edu/physics/engineering-physics/). 
- [Josiah Goode](https://github.com/jmg04006)
- [Masai Olowokere](https://github.com/Masai618)
- [Simon Podsiadlik](https://github.com/spodsiadlik)

## Advisor
- [Dr. Lin Zhang](https://github.com/linzhangUCA) (Thank you for your constant support, guidance, and enthusiasm!)



# Appendix

## Robot Properties

| Property | Quantity |
| --- | --- |
| Weight | 3.2 kg |
| Dimension (Length x Width x Height) | 0.51 m x 0.305 m x 0.195 m |
| Wheel Radius | 5.7 cm |
| Wheel Separation (Width) | 21 cm |
| Wheel Separation (Length) | 33.2 cm |
| Ground Clearance | 4.5 cm |

## Parts List
| Name | Description | Quantity |
| --- | --- | --- |
| Raspberry Pi 4 | CPU Unit Used to Run Robot | 1 |
| Motor Driver Board (Cytron MD30C R2) | An Unit That Allows Motors to Be Controlled Using the Raspberry Pi | 1 |
| Injora 550 Waterproof Brushed Motor 12T | Used to Drive the Bot (Forward and Backward) | 1 |
| Miuzci 20kg Digital Servo | Used to Steer the Bot (Left and Right) | 1 |
| Voltage Divider | Used to Control the Voltage Entering the Motor/Servo | 1 |
| MH Voltage Regulator | Used to Regulate the Voltage Entering the Motor/Servo | 1 |
| Web Camera | Used to Guide the Robot and Analyze Surroundings | 1 |
| Bluetooth Gaming Controller | Used to Control the Movement of the Robot During Data Collection | 1 |
| Battery | 8000 mAh, 7.4  V Lithium Polymer Battery (Powers Motors) | 1 |
| Anker Power Bank | Serves as a Power Source for the Pi | 1 |
| 3-D Printed Frame | Used as a Base to Hold Attached Components | 1 |
| RC Car Frame | Used as a Base for the Overall Robot | 1 |
| Stand-off Screws | Used to Attach Parts to the Bot | 21 |
| Screws | Various Sized Screws Used to Attach Parts | 18 |

## Issues That We Ran Into & Solutions
When we began work on this project, the first aspect that we wanted to change was the design of the base. Previously, all of the electrical components were housed inside of a plastic box, and we had difficulty accessing the parts to make adjustments. Therefore, throughout the semester, we used FreeCAD to create and adjust a palstic base where all of the components are easily accessible. It also served as a great introduction to CAD software as a whole, which is a skill that I will continue to build over the coming semester.

We decided to interact with the steering servo directly instead of using a PWD board. When we made that change, we realized it would be better to use the gpiozero library to steer the robot and control the motor. The previous team used the adafruit library to handle those tanks. When we made the change, we had to update all the python scripts that involved steering and the motor, so they would work with the new library. We kept all the previous team's python scripts in our github in case a future team decides to switch back to the adafruit library. There were component tests to see if the motor, servo, camera, and joystick work properly. We created our own python scripts to ensure that the joystick would work with the motor, servo, and camera. We then created an Autobots version to teleop_js, so we could drive the robot manually. Finally, we made new Autobot versions of the collect_data and autopilot python scripts. We rewrote all the code to work with the gpiozero library using useful pieces of code from the previous team's python scripts. 

One final major issue that we encountered towards the end of the semester involved our I2 motors burning out. It would function properly until we executed our data collection program, during which the motor would overheat and start to smoke. This issue occurred twice, and after researching the type of motor, we found out that this was a recurring issue with the part. Therefore, we replaced the motor with a new model (Injora 550) and it now seems to work effectively.
