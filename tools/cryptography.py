import rsa
from cryptography.fernet import Fernet


# important RSA key information 
publicKey, privateKey = None, None
symmKey = None 
fernet = None 

def generateSymmKey():
    global symmKey
    global fernet
    symmKey = Fernet.generate_key()
    fernet = Fernet(symmKey)

def encryptWithSymmetricKey(message): 
    encMessage = fernet.encrypt(message.encode())
    return encMessage

def decyrptWithSymmetricKey(encMessage): 
    decMessage = fernet.decrypt(encMessage).decode()
    return decMessage


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
generatePublicPrivateKey(256); 
encryptWithAssymmetricKey('Hello Mr Zhi Xuan') 
decryptWithAssymmetricKey(encryptWithAssymmetricKey("Hello Mr Zhi Xuan"))
print("##############")
generateSymmKey() 
encryptWithSymmetricKey("hello mr zhi xuan")
decyrptWithSymmetricKey(encryptWithSymmetricKey("hello mr zhi xuan"))