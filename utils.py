import numpy as np
import types

def convertTextToBinary(text):
    if type(text) == str:
        return ''.join([format(ord(i), "08b") for i in text])
    elif type(text) == bytes or type(text) == np.ndarray:
        return [format(i, "08b") for i in text]
    elif type(text) == int or type(text) == np.uint8:
        return format(text, "08b")
    else:
        raise TypeError("Input type not supported")

        
        