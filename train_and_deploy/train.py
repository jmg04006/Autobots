"""
Training script.
Model Input: image
Model Output: steering, throttle
"""
import sys
import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset, random_split
from torchvision.transforms.v2 import ToTensor
import matplotlib.pyplot as plt
import cnn_network
import cv2 as cv

# Designate processing unit for CNN training
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {DEVICE} device")

class CustomImageDataset(Dataset): 
    """
    Create a pytorch dataset from collected images and joystick input values.
    """
    def __init__(self, annotations_file, img_dir):
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir
        self.transform = ToTensor()

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        image = cv.imread(img_path, cv.IMREAD_COLOR)
        steering = self.img_labels.iloc[idx, 1].astype(np.float32)
        throttle = self.img_labels.iloc[idx, 2].astype(np.float32)
       
        if self.transform:
            image = self.transform(image)
        return image.float(), steering, throttle

def train(dataloader, model, loss_fn, optimizer):
    """
    Update model's parameters
    """
    size = len(dataloader.dataset)
    model.train()
    epoch_loss = 0.0
    sample_count = 0
    for batch, (image, steering, throttle) in enumerate(dataloader):
        # Combine steering and throttle into one tensor (2 columns, X rows)
        target = torch.stack((steering, throttle), -1) 
        X, y = image.to(DEVICE), target.to(DEVICE)
        # Compute prediction error
        pred = model(X)  # forward propagation
        batch_loss = loss_fn(pred, y)  # compute loss
        batch_loss.backward()  # back propagatin
        optimizer.step()  # update parameters
        optimizer.zero_grad()
        # Statistics
        sample_count += target.shape[0]
        epoch_loss = (epoch_loss*batch + batch_loss) / (batch + 1)
        print(f"loss: {batch_loss.item()} [{sample_count}/{size}]")        
    return epoch_loss.item()  

def test(dataloader, model, loss_fn):
    """
    Validate model performance
    """
    num_batches = len(dataloader)
    model.eval()
    test_loss = 0.0
    with torch.no_grad():
        for image, steering, throttle in dataloader:
            #Combine steering and throttle into one tensor (2 columns, X rows)
            target = torch.stack((steering, throttle), -1) 
            X, y = image.to(DEVICE), target.to(DEVICE)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
    test_loss /= num_batches
    return test_loss


# MAIN
data_dir = os.path.join(sys.path[0], 'data/2024_04_10_15_40')
annotations_file = os.path.join(data_dir, 'labels.csv')  # the name of the csv file
img_dir = os.path.join(data_dir, 'images')
collected_data = CustomImageDataset(annotations_file, img_dir)
print(f"Datapoints #: {len(collected_data)}")
# Define the size for train and test data
train_data_len = len(collected_data)
train_data_size = round(train_data_len*0.9)
test_data_size = train_data_len - train_data_size 
print(f"train size: {train_data_size}; test size: {test_data_size}")
# Create dataloaders (split into train and test)
train_data, test_data = random_split(collected_data, [train_data_size, test_data_size])
train_dataloader = DataLoader(train_data, batch_size=125)
test_dataloader = DataLoader(test_data, batch_size=125)
# Initialize the model
#    Models that train well:
#     lr = 0.001, epochs = 10
#     lr = 0.0001, epochs = 15 (epochs = 20 might also work)
model = cnn_network.DonkeyNet().to(DEVICE) # choose the architecture class from cnn_network.py
loss_fn = nn.MSELoss()
lr = 0.001
epochs = 15
optimizer = torch.optim.Adam(model.parameters(), lr=lr)
# Optimize the model
train_loss = []
test_loss = []
for t in range(epochs):
    print(f"Epoch {t+1}\n-------------------------------")
    training_loss = train(train_dataloader, model, loss_fn, optimizer)
    testing_loss = test(test_dataloader, model, loss_fn)
    print("average training loss: ", training_loss)
    print("average testing loss: ", testing_loss)
    # save values
    train_loss.append(training_loss)
    test_loss.append(testing_loss)   
print(f"Optimize Done!")
# Graph
fig = plt.figure()
axs = fig.add_subplot(1,1,1)
plt.plot(list(range(epochs)), train_loss, color='b', label="Training Loss")
plt.plot(list(range(epochs)), test_loss, '--', color='orange', label='Testing Loss')
axs.set_ylabel('Loss')
axs.set_xlabel('Epoch #')
title_name = f'{model._get_name()}-{epochs}Epochs-{lr}lr'
axs.set_title(title_name)
axs.legend()
fig.savefig(os.path.join(data_dir, title_name+'.png'))
# Save the model
torch.save(model.state_dict(), os.path.join(data_dir, title_name+'.pth'))
