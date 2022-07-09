import rsa
from Crypto.Cipher import AES
import base64
import os

# important RSA key information
publicKey, privateKey = None, None
nonce = None

def generate_secret_key_for_AES_cipher():
    AES_key_length = 16  # use larger value in production
    secret_key = os.urandom(AES_key_length)
    encoded_secret_key = base64.b64encode(secret_key)
    return encoded_secret_key

def encrypt_message(private_msg):
    secret_key = generate_secret_key_for_AES_cipher()
    cipher = AES.new(secret_key, AES.MODE_EAX)
    global nonce 
    nonce = cipher.nonce
    encoded_message = str.encode(private_msg)
    ciphertext, tag = cipher.encrypt_and_digest(encoded_message)
    keyCiphertext = b'secret_key%*' + ciphertext

    print("Recevied Secret Message: " + private_msg)
    print(b'Private Key generated: ' + secret_key)
    print(b'Key + ciphertext: ' + keyCiphertext) 
    return keyCiphertext, tag

def decrypt_message(ciphertext, encoded_secret_key, tag):
    cipher = AES.new(encoded_secret_key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        print("The message is authentic:", plaintext)
    except ValueError:
        print("Key incorrect or message corrupted")  
    return plaintext


# #Example Run 
# key = generate_secret_key_for_AES_cipher()
# print("key: ")
# print(key)
# print("encrpyted message and tag:")
# ciphertext, tag = encrypt_message("Hello Erwin", key)
# print(ciphertext)
# print("decrypt:")
# print(decrypt_message(ciphertext, key, tag))

##########################
### RSA IMPLEMENTATION ###
##########################

# generate public and private keys
# possible key sizes (bits): 128,256,384,512,1024,2048,3072,4096
def generatePublicPrivateKey(keySize):
    global publicKey
    global privateKey
    publicKey, privateKey = rsa.newkeys(keySize)
    print(publicKey)
    print(privateKey)

# rsa.encrypt method is used to encrypt string with public key string
# should be encode to byte string before encryption with encode method
def encryptWithAssymmetricKey(message):
    encMessage = rsa.encrypt(message.encode(), publicKey)
    print("original string: ", message)
    print("encrypted string: ", encMessage)
    return encMessage

# the encrypted message can be decryptes with ras.decrypt method and private key
# decrypt method returns encoded byte string,
def decryptWithAssymmetricKey(ciphertext):
    decMessage = rsa.decrypt(ciphertext, privateKey).decode()
    print("decrypted string: ", decMessage)


# Example Run
# generatePublicPrivateKey(256);
# encryptWithAssymmetricKey('Hello Mr Zhi Xuan')
# decryptWithAssymmetricKey(encryptWithAssymmetricKey("Hello Mr Zhi Xuan"))
