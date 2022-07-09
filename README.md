# lifehack22-PrBros
LifeHack 2022 


# Set up Python Virtual Environment 
- `python3 -m pip install --user virtualenv`
- `python3 -m venv env`
- `source env/bin/activate`
To leave: `deactivate` 

## Inspiration
Ever had the need to encrypt a message, but not wanting it to look painfully obvious that it has been encrypted? We do! From personal details to bank account numbers, there are plenty of instances where encryption comes in handy. It doesn't just end here in our project. In our project, we take it a notch higher.

## What it does
{Project Name} is a Telegram bot that takes in an image alongside the secret message that the user intends to hide. We encrypt the secret message using {technique} then embed the ciphertext into the image provided via image steganography. The resultant image is then sent back to the user. 

There are 2 key functionalities in our project:

### Cryptography ({type of cryptography})

### Image Steganography (Least Significant Bit (LSB) Approach)
Digital images may be described as a finite set of pixels. Pixels, are in turn defined to be the smallest individual element of an image. They hold values to represent the brightness of a given colour at any specific point. As such, we can think of images as a matrix of pixels.

In the LSB approach, we replace the last bit of each pixel with each bit of our ciphertext. Each pixel contains 3 values: Red, Green and Blue. These values range from 0 to 255. By encryting and converting the secret message into binary, we interate over the pixel values 1 by 1, replacing each LSB with the ciphertext bits sequentially. Since we are only modifying pixel values by +1 or -1, any changes in the resultant image will be indistinguishable to the human eye.

## How we built it

### Telegram Bot

### Cryptography

### Image Steganography
Image steganographic functionalities are built with NumPy and opencv-python. We settled for NumPy because we are able to enjoy the flexibility of Python as well as the speed of compiled C code at its core. What is more is that NumPy indexing is the de facto standard of array computing today. OpenCV was another obvious choice for us as it is one of the famously used open-source Python libraries meant exclusively for Computer Vision. Modules and methods available in OpenCV allow us to perform image processing with a few lines of codes. We wanted to make use of this hackathon to learn a little more about Computer Vision techniques.

## Challenges we ran into
We experimented with discrete cosine transform as our implementation for image steganography. Unfortunately, the resultant image has a tinge of a strange blue hue to it. As a result, we scrapped the our work and started from square 1 again. This time, we looked to modify the least significant bit of each pixel in the image. We are glad that the resultant image turned out to be indistinguishable from the original, at least to the human eye.

## Accomplishments that we're proud of

## What we learned

## What's next for Untitled