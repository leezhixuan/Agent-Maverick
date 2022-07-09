import cv2
import random

from cryptography import ascii_caesar_shift, ascii_caesar_shift_back
from utils import convertTextToBinary
from bitstring import BitArray

def encodeText(messageToHide, filePathName): 
    if (len(messageToHide) == 0): 
        raise ValueError('Data is empty')
    image = cv2.imread(filePathName) # Read the input image using OpenCV-Python.

    # Generate important variables to encrypt the message 
    key = random.randint(1, 127)
    cipher = ascii_caesar_shift(messageToHide, key) 
    messageToHide = str(key) + "@@@@@" + cipher
    encoded_image = hideData(filePathName, image, messageToHide) # call the hideData function to hide the secret message into the selected image

    #save the new canges 
    cv2.imwrite(filePathName, encoded_image) 
    return encoded_image


def decodeText(filePathName):
    # read the image that contains the hidden image 
    image = cv2.imread(filePathName) #read the image using cv2.imread() 
    text = showData(image)
    return text


def hideData(imageName, image, secret_message):
    # calculate the maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8

    #Check if the number of bytes to encode is less than the maximum bytes in the image
    if len(secret_message) > n_bytes:
        raise ValueError(f"Error: Please provide a shorter message. Maximum length is: {n_bytes}")

    secret_message += "#####" # dummy string as delimeter

    data_index = 0
    binaryCipherText = convertTextToBinary(secret_message)

    data_len = len(binaryCipherText) #Find the length of data that needs to be hidden
    for values in image:
        for pixel in values:
            # convert RGB values to binary format
            r, g, b = convertTextToBinary(pixel)

            # modify the LSB only if there is still data to store
            if data_index < data_len:
                # hide the data into LSB of the red pixel
                pixel[0] = int(r[:-1] + binaryCipherText[data_index], 2)
                data_index += 1

            if data_index < data_len:
                # hide the data into LSB of the green pixel
                pixel[1] = int(g[:-1] + binaryCipherText[data_index], 2)
                data_index += 1

            if data_index < data_len:
                # hide the data into LSB of the blue pixel
                pixel[2] = int(b[:-1] + binaryCipherText[data_index], 2)
                data_index += 1

            # break out of the loop if there is no more data to hide
            if data_index >= data_len:
                break

    cv2.imwrite(imageName,image)           
    return image


def showData(image):
    binary_data = ""
    for values in image:
        for pixel in values:
            r, g, b = convertTextToBinary(pixel) #convert the red,green and blue values into binary format
            binary_data += r[-1] #extracting data from the LSB of red pixel
            binary_data += g[-1] #extracting data from the LSB of red pixel
            binary_data += b[-1] #extracting data from the LSB of red pixel

    # split by 8-bits
    all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]

    # convert from bits to characters
    decoded_data = ""

    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "#####": #check if we have reached the delimeter which is "#####"
            break
    
    # result = decrypt_message(decoded_data[:-5])
    if "@@@@@" not in decoded_data[:-5]: 
        return "not done"

    result = ascii_caesar_shift_back(decoded_data[:-5].split("@@@@@")[1], int(decoded_data[:-5].split("@@@@@")[0]))

    return result #remove the delimeter to show the original hidden message