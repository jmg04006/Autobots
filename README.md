# Team Autobots - Autonomous Navigation Using a Neural Network

![image0 (8)](https://github.com/jmg04006/Autobots/assets/112110593/9116daa2-f7d0-4688-be8b-25208634bf0b) 

## Project Overview 
Our team designed a small autonomous vehicle with the goal of autonomously navigating various mazes set up throughout Lewis Science Center (LSC) and the Conway Corporation Center for Sciences (CCCS). The setup of the tracks is loosely based on two robotics competitions that last year's teams competed in:  (1) the Autonomous Vehicle Challenge at the [National Robotics Challenge](https://www.thenrc.org/) (NRC) and (2) the Intelligent Vehicle Challenge at the annual [Arkansas Space Grant Consortium](https://arkansasspacegrant.org/) (ASGC) Symposium. However, on our version of the tracks, there are multiple different variables at play that will be described below. By the end of next semester, we plan to have the ability to autonomously navigate all five possible tracks.

We created our autonomous process using vision-based supervised machine learning, and we continued the work of Team WHAM from last semester (who took inspiration from the open-source [Donkey Car](https://docs.donkeycar.com/) project. To navigate the maze, we first collected data by driving the bot around the course with a camera, and then we used a neural network to train a model that the robot would use to find its way through the course. At the end of the semester, we were able to used this method to have our robot autnomously navigate around the _CCCS Clipper_ track (see _Autonomous Vehicle Performance_ section).


## Circuit Diagram
![image0 (10)](https://github.com/jmg04006/Autobots/assets/112110593/f5bf7ea1-deae-41f1-9be8-5103e386c89a)


## Project Instructions
To get things started, we go to the Autobots Wiki page and find [First Time Driving Instructions](https://github.com/jmg04006/Autobots/wiki/First-Time-Driving-Instructions). That page explains all the steps for pre-installation, collecting data, training a model, and running autopilot. It is a general template for performing those tasks. 

### Training a Model and Running Autopilot: 

1. From the host computer, type ssh -X user@192.168.0.111 into the terminal to connect to the RPi remotely. (Note: The IP address/username will depend on what you set up; this change will also translate to other steps below.)
2. Navigate to the _train_and_deploy_ folder. The contents of this folder are describen more in detail in the [Wiki](https://github.com/jmg04006/Autobots/wiki/Description-of-Content-in-train_and_deploy-Folder).
3. Run _collect_data_autobots.py_ and start collecting data by pressing the X key on the wireless controller.
4. Once data collection is complete, transfer the data to the host computer from the RPi by typing rsync -rv user@192.168.0.111:~/Autobots/train_and_deploy/data/FOLDERNAME ~/Autobots/train_and_deploy/data/ into the host terminal window. FOLDERNAME needs to be changed to the name of the folder where the data is stored. It can be found in Data folder inside the _train_and_deploy_ folder.
5. Go to the _train.py_ script on the host computer and change the Folder name in lines 101 and 102 in the script to the folder name where the data was saved. Then, run the script.
6. After _train.py_ is finished and the model is created, transfer it back to the RPi using and command rsync -rv /home/robotics-j/Autobots/train_and_deploy/data/FOLDERNAME/DonkeyNet_15_epochs_lr_1e_3.pth user@192.168.0.111:~/Autobots/train_and_deploy/models/. Run this command in the host terminal, and change the foldername to the name of the folder where the data was stored before running the command.
7. Lastly, run _autopilot_autobots.py_ .


## Approaches
> Make this section as **Approaches** section. Use your knowledge learned from deep learning class to explain how the autopilot model works under the hood. Assuming you are explaining everything to high school students. Diagrams and more illustrative methods are welcome here.

The procedure for our robot's autonomous navigation consists of three primary sub-processes: data collection, neural network training, and autopilot/navigation.

Initially, we collected data using a mounted camera as we drove it around the decided course multiple times (we tended to do about 20 laps on average). As we drove around the area, we collected both image data and the corresponding throttle/steering values. Then, we saved the image data (our _feature data_) to a directory, and the throttle/steering values (our _target data_) into a .csv file.

Next, we trained a neural network using our _train.py_ script. To accomplish this, we executed a __forward pass__ where we used our recorded images to compute predicted throttle and steering values. Second, we used _back propagation_

Training  - Involves forward pass (going to use to compute a prodicted throttle/steering value based on images)
- Back propagation
- Compare predicted values to label/target values from data collection
- Calculate the error between target and predicted values using MSE
- Calculate the gradient of the error(loss) with respect to trainable parameters to update them.

Navigation - Using new input images in conjuction with trained parameters to make a prediction by itself on how to navigate the course.


Our robot's navigational process starts with data collected when we drive it around the preset course multiple times (we aimed for about 20 times on average). While we steer the robot, it records images from a mounted camera on the front which we will then use to train the robot. Next, we compress the images and run them through a convolutional neural network. This neural network flattens and compresses the image until we retrieve two values: steering and throttle. A graphic showing this process is shown below. Once the training is completed, we then begin the autonomous navigation process. During this, our robot will take in images while driving and make a prediction about where and how fast it should go based on the trained paramters. In doing so, our robot can actively make slight adjustments based on new information in the course and effectively navigate the maze.

![cnn_architecture](https://github.com/jmg04006/Autobots/assets/112110593/21f1a2d3-da94-4caf-9365-79268b2af716)


### Track Possibilities & Conditions

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
This is the [final navigation](https://youtu.be/jehrM9FV0Xk) from December 12, 2023! Our robot functioned properly and was able to autonomously navigate the maze in about 27 seconds. In the process of obtaining data for the final test, we collected 24,834 images, and each image, in addition to its own pixel values, had a respective throttle and steering value. Below, we have included a picture of the training loss curve that our model used in the final race. The training and test loss are quite low in the end, meaning that our data was sufficient with slight room for error. Lastly, the only issue that we observed with our bot during the final race occurred after completing one full lap; our robot would go towards a specific spot in the chairs that was not on the programmed course. Therefore, we should consider fine-tuning the model to complete more than one lap.

![Loss versus Training Epoch](https://github.com/jmg04006/Autobots/blob/main/media/DonkeyNet_15_epochs_lr_1e_3.png) 


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
