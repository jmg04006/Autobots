# Vision-Based Autonomous Driving Using Neural Networks

![image0 (8)](https://github.com/jmg04006/Autobots/assets/112110593/9116daa2-f7d0-4688-be8b-25208634bf0b) 

## Project Overview
Our team designed a small autonomous vehicle with the goal of autonomously navigating various mazes set up throughout Lewis Science Center (LSC) and the Conway Corporation Center for Sciences (CCCS). The setup of the tracks is loosely based on two robotics competitions that last year's teams competed in:  (1) the Autonomous Vehicle Challenge at the [National Robotics Challenge](https://www.thenrc.org/) (NRC) and (2) the Intelligent Vehicle Challenge at the annual [Arkansas Space Grant Consortium](https://arkansasspacegrant.org/) (ASGC) Symposium. However, on our version of the tracks, there are multiple different variables at play that will be described below. By the end of next semester, we plan to have the ability to autonomously navigate all five possible tracks.

We created our autonomous process using vision-based supervised maching learning, and we continues the work of Team WHAM from last semester (who took inspiration from the open-source [Donkey Car](https://docs.donkeycar.com/) project. Our robot's navigational process starts with data collected when we drive it around the preset course multiple times. The bot records both images from a mounted camera and the driving command inputs, and this data is used to optimize a convolutional neural network. Then, when we start the vehicle autonomous navigation process, it will take in new images and use the previous data to determine how and where to drive the bot through a course. We are still figuring out how to fine-tune the process, but our bot has been able to effectively navigate the maze.


## Circuit Diagram


## Repository Contents
This `train_and_deploy` folder contains all of the software for our autonomous vehicle, including:
- a [config.json](https://github.com/willward20/WHAM/blob/main/train_and_deploy/config.json) file that limits the vehicle's maximum throttle and defines the vehicle's steering trim;
- [motor.py](https://github.com/willward20/WHAM/blob/main/train_and_deploy/motor.py) and [servo.py](https://github.com/willward20/WHAM/blob/main/train_and_deploy/servo.py) scripts that contain functions for initializing and deploying the vehicle's motor/motor driver and steering servo/PWM board;
- a [collect_data.py](https://github.com/willward20/WHAM/blob/main/train_and_deploy/collect_data.py) script that is used to manually drive the vehicle with a wireless controller while collecting steering, throttle, and camera data; 
- a [train.py](https://github.com/willward20/WHAM/blob/main/train_and_deploy/train.py) script that trains a CNN using PyTorch and generates a .pth autopilot file containing the trained parameters; 
- an [autopilot.py](https://github.com/willward20/WHAM/blob/main/train_and_deploy/autopilot.py) script that drives the vehicle autonomously using a .pth autopilot file; 
- and a [cnn_network.py](https://github.com/willward20/WHAM/blob/main/train_and_deploy/cnn_network.py) file that defines the neural network architectures accessed by the train.py and autopilot.py scripts.


## Convolutional Neural Network
After testing several variations of CNN architectures, we had the most success with Donkey Car's [fastai](https://github.com/autorope/donkeycar/blob/main/donkeycar/parts/fastai.py) architecture (see the "Linear" class). The figure below shows how we modified the CNN structure to accomodate for our input image size and achieve the best results.  Our network architecture has five convolution layers and three fully connected layers. Each image in the network has an input size of 3x120x160 (3 color channels, 120 pixel horizontal width, and 160 pixel vertical height) and an output size of 2 prediction values: steering and throttle. When a dataset is loaded, the recorded images are split into training images (90-95% of the data) and test images (10-5%). During the training process, the network uses the Mean Square Error (MSE) loss function, Adam optimizer, a learning rate of 1E-3, and batch sizes of 125 (train) and 125 (test). The neural network iteratively trains for typically 10-20 epochs. We found the most success when using datasets with a size between 15-20k images.

<img src="https://github.com/willward20/WHAM/blob/main/media/cnn_architecture.png"/>

## Issues That We Ran Into & Solutions
Design of Base

Previous code not working

Motors Burning Out

## Track Possibilities & Conditions
### Indoor Tracks:
- **The Basement:** LSC's basement: Large, involves one-direction turns, scenery is repetitive.
- **Office Connection:** LSC's first floor: Medium-sized, involves one-direction turns, slopes, and a narrow passage.
- **CCCS Clipper:** CCCS' main entrance: Small, involves two-direction turns, narrow passages, and sharp turns. Additionally, it needs buckets to set up.

### Outdoor Tracks
- **Ants Nests:** CCCS' west entrance: Small, involves two-direction turns and slopes.
- **LSC Plaza:** Parking lot between LSC and Annex: Medium-sized, partially offroad, involves two-direction turns and slopes.

For our final project, we decided to navigate the CCCS' main entrance, since it incorporates the most 

![cccs_clipper](https://github.com/jmg04006/Autobots/assets/112110593/8777682c-2be3-484f-b12c-3af9f5e686a5)


## Autonomous Vehicle Performance
Will upload a video after final test!!!


## Project Conclusions
Throughout this project, we built an autonomous robot using the modified RC car and parts left by Team WHAM from last year. Then, we constructed our own vision-based neural network by taking some of WHAM's original code and instating functions of our own to ensure that the Bluetooth controller and the Raspberry Pi were functioning exactly how we wanted.  To accomplish this, we made sure that the joystick could indepently control the steering and the throttle while taking in data using a camera. Using this process, we would drive the robot around the course multiple times (around 20), to collect data, and then, we'd input the images into our neural network. Lastly, we used the data in conjunction with our _autopilot_ file in order to have the bot autonomously navigate the track. We were able to get the robot to effectively pilot itself through the maze, especially once we fixed our hardware issues.


## Goals for Next Semester
Investigating lighting factors (angle of sun/time of day)

Navigate all other mazes, inclduing outdoor mazes

Incorporate new sensors/ design new safety features (roll cage, etc.)

One area of investigation that still needs work is determining the best method for training the neural network. Our most successful tests have been data sets collected continuously, usually with between 15 thousand and 20 thousand images. We would like to see this project taken to the next level, with a neural network model that is general enough to operate under changing conditions (background, weather, time of day) without additional data collection. We tried combining data collected on the course under these different circumstances and training a model, but they performed very poorly. New sensors could potentially help with this. There have been similar projects that use additional information like stereo depth vision and absolute GPS position data based on the start point to make more general models.

While we found a neural network architecture that produced functional models, it was very picky about the weather conditions. We only had successful models when the robot was out of sunlight, and the surroundings were not too bright. This could have been due to the camera itself creating image artifacting from the light, or it could have been because of the model putting too much weight on the brightness of colors. Either way, we recommend trying other neural network architectures to see if there are any that perform better than Donkey Car's fastai architecture.


## Important Links 
- [National Robotics Challenge](https://www.thenrc.org/)
- [Arkansas Space Grant Consortium](https://arkansasspacegrant.org/)
- [Donkey Car API](https://docs.donkeycar.com/) (inspired this project)
- [Donkey Car CNN architecture: fastai](https://github.com/autorope/donkeycar/blob/main/donkeycar/parts/fastai.py)


## Contributors 
During our final year at the University of Central Arkansas, we built on the work previously done by Team [WHAM](https://github.com/willward20/WHAM) and, with guidance from Dr. Zhang, made our own adjustments to the bot. We will continue working on this senior design project until May 2024, when we are slated to graduate with B.S. in [Engineering Physics](https://uca.edu/physics/engineering-physics/). 
- [Josiah Goode](https://github.com/jmg04006)
- [Masai Olowokere](https://github.com/Masai618)
- [Simon Podsiadlik](https://github.com/spodsiadlik)

## Advisor
- [Dr. Lin Zhang](https://github.com/linzhangUCA) (Thank you for your constant support, guidance, and enthusiasm!)


# Appendix
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
| Battery | 1000 mAh, 7.4  V Lithium Polymer Battery (Powers Motors) | 1 |
| Anker Power Bank | Serves as a Power Source for the Pi | 1 |
| 3-D Printed Frame | Used as a Base to Hold Attached Components | 1 |
| RC Car Frame | Used as a Base for the Overall Robot | 1 |
| Stand-off Screws | Used to Attach Parts to the Bot | 21 |
| Screws | Various Sized Screws Used to Attach Parts | 18 |
