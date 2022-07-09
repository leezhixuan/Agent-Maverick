def ascii_caesar_shift(message, distance):
    encrypted = ""
    for char in message:
        value = ord(char) + distance
        encrypted += chr(value % 128) #128 for ASCII
    return encrypted

def ascii_caesar_shift_back(message, distance):
    encrypted = ""
    for char in message:
        value = ord(char) - distance
        encrypted += chr(value % 128) #128 for ASCII
    return encrypted






# ################################################################
# ### ROOM FOR IMPROVEMENT USING ADVANCE CRYTOPGRAPHIC METHODS ###
# ################################################################
# # important RSA key information
# publicKey, privateKey = None, None

# data = {}


# ####################################
# ### SYMMETRIC KEY IMPLEMENTATION ###
# ####################################

# def generate_secret_key_for_AES_cipher():
#     AES_key_length = 16  # use larger value in production
#     secret_key = os.urandom(AES_key_length)
#     encoded_secret_key = base64.b64encode(secret_key)
#     return encoded_secret_key

# def encrypt_message(private_msg):
#     secret_key = generate_secret_key_for_AES_cipher()
#     cipher = AES.new(secret_key, AES.MODE_EAX)

#     nonce = cipher.nonce
#     print(nonce)
#     global data
#     data[secret_key] = nonce
#     encoded_message = str.encode(private_msg)
#     ciphertext, tag = cipher.encrypt_and_digest(encoded_message)

#     keyCiphertext = secret_key + b'%*' + ciphertext

#     print("Recevied Secret Message: " + private_msg)
#     print(b'Private Key generated: ' + secret_key)
#     print(b'Key + ciphertext: ' + keyCiphertext)
#     return keyCiphertext, tag

# def decrypt_message(ciphertext):
#     global data
#     print(data)
#     cipherKey = ciphertext[:24].encode()
#     encrypt = ciphertext[26:]
#     _nonce = data[cipherKey]
#     cipher = AES.new(cipherKey.decode("utf-8"), AES.MODE_EAX, nonce=_nonce)
#     plaintext = cipher.decrypt(encrypt)
#     return plaintext

#     # try:
#     #     cipher.verify(tag)
#     #     print("The message is authentic:", plaintext)
#     # except ValueError:
#     #     print("Key incorrect or message corrupted")
#     # return plaintext


# # #Example Run
# # key = generate_secret_key_for_AES_cipher()
# # print("key: ")
# # print(key)
# # print("encrpyted message and tag:")
# # ciphertext, tag = encrypt_message("Hello Erwin", key)
# # print(ciphertext)
# # print("decrypt:")
# # print(decrypt_message(ciphertext, key, tag))

# ##########################
# ### RSA IMPLEMENTATION ###
# ##########################

# # generate public and private keys
# # possible key sizes (bits): 128,256,384,512,1024,2048,3072,4096
# def generatePublicPrivateKey(keySize):
#     global publicKey
#     global privateKey
#     publicKey, privateKey = rsa.newkeys(keySize)
#     print(publicKey)
#     print(privateKey)

# # rsa.encrypt method is used to encrypt string with public key string
# # should be encode to byte string before encryption with encode method
# def encryptWithAssymmetricKey(message):
#     encMessage = rsa.encrypt(message.encode(), publicKey)
#     print("original string: ", message)
#     print("encrypted string: ", encMessage)
#     return encMessage

# # the encrypted message can be decryptes with ras.decrypt method and private key
# # decrypt method returns encoded byte string,
# def decryptWithAssymmetricKey(ciphertext):
#     decMessage = rsa.decrypt(ciphertext, privateKey).decode()
#     print("decrypted string: ", decMessage)


# # Example Run
# # generatePublicPrivateKey(256);
# # encryptWithAssymmetricKey('Hello Mr Zhi Xuan')
# # decryptWithAssymmetricKey(encryptWithAssymmetricKey("Hello Mr Zhi Xuan"))