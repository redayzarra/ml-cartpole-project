"""
Traffic Signs Classification Project - LeNet Deep Network

This project utilizes the LeNet deep network architecture to classify 43 different 
types of traffic signs. LeNet refers to a convolutional neural network that can be 
used for computer vision and classification models. This project showcases a 
step-by-step implementation of the model as well as in-depth notes to customize the 
model further for higher accuracy.

We will first start by importing the necessary libraries we will need:
"""
# Classic libraries that will help us read and analyze data
import numpy as np
import pandas as pd

# Libraries used for plotting and data visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Using pickle package to open our data, not much use after that
import pickle


"""
Importing the data into three different sections: training, validation, and
testing. Training data is used to train the network, testing data is used to test
the trained network with data that it has never seen to see how it would perform in
the real world. The validation dataset ensures that we avoid overfitting by showing
the network validation data every epoch (or run) in a process called 
cross-validation to ensure that the network is not focusing on the details of the
training data. 
"""
with open("./traffic-signs-data/train.p", mode = 'rb') as training_data:
  train = pickle.load(training_data) # Use pickle's load method to load the defined data as the variable test

with open("./traffic-signs-data/valid.p", mode = 'rb') as validation_data:
  valid = pickle.load(validation_data)

with open("./traffic-signs-data/test.p", mode = 'rb') as testing_data:
  test = pickle.load(testing_data)


"""
Splitting the data into our individual training and testing set variables.
"""
# Assigning the features of the training set as X_train and the dependent variable (labels) as y_train
X_train, y_train = train['features'], train['labels']

# Assigning the features of the validation set as X_validation and the dependent variable (labels) as y_validation
X_validation, y_validation = valid['features'], valid['labels']

# Assigning the features of the testing set as X_test and the dependent variable (labels) as y_test
X_test, y_test = test['features'], test['labels']

# Checking the dimensions of the training set
X_train.shape # Gives us an output of a four element tuple. The first number is the quantity of images, the second is the width of image in pixels, the third is the height of the image, and the last number the depth - in this case the 3 tells us that the images are colored since they are being multiplied for both Red, Green, and Blue
y_train.shape # Gives us a tuple of one element, which is a label for each image in the training set

X_validation.shape
y_validation.shape

X_test.shape
y_test.shape


"""
Using matplotlib to display a randomly choosen image and see if it matches with its 
label, just to see what the images are and how the network will be classifying them. 
Each type of sign has its own class which will identify the type of sign to the 
model. 
"""
i = 23 # The index of the image we want to look at, arbitrarily chose 23

plt.imshow(X_train[i]) # Using matplotlib's .imshow method to show an image from the features training set at the index of 23
y_train[i] # Also show us the corresponding label from the same index in the label's training set - the label tells us that the sign is a "End of No Passing"

plt.imshow(X_validation[i]) # Verifying images for the validation dataset
y_validation[i]

plt.imshwo(X_test[i]) # Verifying images for the testing dataset
y_test[i]


"""
Preparing the data by shaving off things we don't need in the data. Such as 
transforming the images from RBG to grayscale (changes the depth from 3 to 1). I 
will also perform data normalization, where instead of using the pixel values 
ranging from 0 to 255, we can lower the range to use a more restricted range of
pixel values. The data needs to also be shuffled so the images do not get trained
in a certain order, we do not want the network to learn the order of these images.
We want to make it as hard as possible for the network to learn, which is why we
use low-quality images, more restricted pixel range, and grayscale images. 
"""
# Shuffling the dataset
from sklearn.utils import shuffle # Importing the shuffle function from the sci-kit learn library to shuffle the dataset first
X_train, y_train = shuffle(X_train, y_train) # Used the shuffle function to reassign the variables of X_train and y_train into a different order, however the labels still correspond to the correct images because the shuffle function reorders them the same way

# Converting images to Grayscale
X_train_gray = np.sum(X_train / 3, axis = 3, keepdims = True) # Use numpy to average the pixels to get the grayscale version of the image. We will simply add the pixel values from the three color channels (Red, Green, and Blue) and then divide them by 3. 
X_train_gray.shape # The depth of the features training set is no longer 3, its now 1. This means the images are now grayscale
plt.imshow(X_train_gray[i].squeeze(), cmap = 'gray') # The network will now learn from this "grayscale" image which uses much less processing power because the image depth is reduced to 1

X_validation_gray = np.sum(X_validation/3, axis = 3, keepdims = True)
X_validation_gray.shape # Averaging the RGB values to reduce the depth from 3 to 1 for the feature's validation set
plt.imshow(X_validation_gray[i].squeeze(), cmap = 'gray') # Grayscale sample image from the feature's validation set

X_test_gray = np.sum(X_test/3, axis = 3, keepdims = True)
X_test_gray.shape 
plt.imshow(X_test_gray[i].squeeze(), cmap = 'gray')

# Restrict the pixel value scale for each dataset, aka normalization. Normalization is important because we want all our pixels in a similar range so the weight at one part of the image is not a lot more than the weight at another part of an image.
X_train_gray_norm = (X_train_gray - 128) / 128 # There are many kinds of normalization methods. This one works by subtracting the image pixels by 128 because we want to center the data from its range of 0 to 255 (256 total, so half is 128). We then divide by 128 to put all the data between -1 and 1.
# X_train_gray_norm ~ confirms that all the pixel values are between -1 and 1
plt.imshow(X_train_gray_norm[i].squeeze(), cmap = 'gray') # The .squeeze() method gets rid of the 1 (last number) at the end of our tuple when we call the .shape method. This is because the 1 represented the depth of each image, but because our images are now grayscale we no longer need to include that. We are also specifying that we want our colormap, or cmap, to be in grayscale so we give it the 'gray' value.

X_validation_gray_norm = (X_validation_gray - 128) / 128
plt.imshow(X_validation_gray_norm[i].squeeze(), cmap = 'gray')

X_test_gray_norm = (X_test_gray - 128) / 128
plt.imshow(X_test_gray_norm[i].squeeze(), cmap = 'gray')


"""
To train the model we will implement six fundamental steps that will ensure we have
correctly implemented the LeNet-5 architecture. The original LeNet-5 architecture
was proposed by Yann LeCun and he developed it to recognize handwritten numbers. 
The dataset with the handwritten numbers is called the MNIST dataset and we will
be working with that in some different project. 

For our use, we will need to cutomize the LeNet architecture a bit because we have
more classes (or types of things) to differentiate from. Yann LeCun had 10 classes 
which were numbers ranging from 0 to 1, while we have over 43 different traffic 
signs. 

For our first step, we will take our input image (which is 32 x 32 x 1) and apply
6 filters that are 5 x 5 with input depth of 3. The output of these filters will be 
28 x 28 x 6 after the image has been processed through it. This is because there is 
an equation the ouptut has to follow that applies when we run images to filters: 

                        Output = ((Input - Filter) + 1) / Stride
the equation returns: 
                        Output = ((32 - 5) + 1) / 1 = 28

The stride is simply how much the kernel is shifted by each time when it passes over 
the image. The kernel is essentially a feature map that scans the image by 
essentially gliding over it. The stride is how much the kernel shifts, so a stride 
of 1 means that the kernel is moving 1px at a time which is slow. While a stride of 
2 means its moving 2px each time. 

The output depth is determined by the number of filters we apply, since we applied
six filters the output of the image after the filters have been applied becomes
28 x 28 x 6.

The second step is to apply a ReLU function on the output. The rectified linear 
unit, or ReLU, an activation function simply takes in input and converts all 
negative numbers into 0's while maintaining all the positive numbers.

Finally, a pooling layer (or subsampling layer) will be applied to simply shrink 
the feature map by 2. This means the output depth will remain the same (the output
from the filters is still maintained), however the size of the output will be 
divided from 28 to 14. The result of the pooling layer is 14 x 14 x 6.
"""



"""
A second convolutional layer is applied which works with the output of the last
layer. For our second step, we will simply repeat the process above but implementing 
some slight changes. We will take the output from the previous convolutional layer, 
which was 14 x 14 x 6 and then apply 16 filters. The filters will follow the same 
equation from above:

                        Output = ((14-5) + 1) / 1 = 10

The stride is 1px (kernel is shifting by 1px each time) and because we have applied 
16 filters, the output of the filters will be 10 x 10 x 16.

Similar to the previous layer, we apply a ReLU funciton which will simply convert 
all the negative values into 0's.

A subsampling layer aka pooling layer is applied to reduce the size of the images 
by 2. Meaning the images are shrunk down from 10 x 10 to 5 x 5, however the output 
depth from the filters has not changed. This means that the output after the second 
convolutional layer is 5 x 5 x 16.
"""



"""
The flatten layer is simply used to convert our matrix of data, which in our case 
is 5 x 5 x 16 into a single array so 400 x 1. This array basically stores the 
individual pixels of an image in a single line. It is important to flatten our data 
because the fully connected (dense) layers expects a one-dimensional vector data 
as input.
"""

"""
A fully connected layer or a dense layer is simply a layer that connects all of the
nodes from it's layer to all of the nodes in the next layer. Dense layers are often
used at the end of neural networks because they allow the network to learn the 
complex mapping from the input to the output data. They function by receiving 
input from all of the nodes and then multiplying weights and adding biases to each
input value. These values are then passed down to the next dense layer which adds 
its own weights and biases. The network learns to control these weights and biases
so that it can eventually make highly accurate predictions.

In our case, the first dense layer will have 400 nodes which will each be assigned 
a pixel from our 400 x 1 flattened vector. The nodes will then connect to a second 
layer which only has 120 nodes (or neurons). The dense layer will then apply a ReLU 
activation function to the output before sending it off to the next layer.
"""


"""
The second dense layer is similar to the first. It will take the input from the 
120 nodes from the previous layer, manipulate the input with its own weights & 
biases, and then pass on the output to the next layer.

The second dense layer will have 120 nodes to recieve the input from the previous 
layer and then it's output will be passed on to another dense layer with 80 nodes. 
The dense layer will then apply a ReLU activation function to the output before 
sending it off to the next layer.
"""


"""
The third and final dense layer will recieve input from the previous layer with its 
80 nodes. This layer will be responsible for manipulating the input recieved and 
sending it to the final output layer. The dense layer will then apply a ReLU 
activation function to the output before sending it off to the output layer.

Our output layer needs to have nodes equal to the number of classes. In the MNIST 
experiment, Yann LeCun only had 10 classes because he was trying to recognize the 
handwritten digits 0 to 9. However, we are trying to classify 43 different kinds of 
signs so our output layer needs to have 43 nodes. One node for each class.
"""