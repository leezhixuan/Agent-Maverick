import os
from dotenv import load_dotenv
import telebot
from telebot import types
import requests



load_dotenv()

APIKey = os.getenv('APIKey')
bot = telebot.TeleBot(APIKey)

@bot.message_handler(commands=['start'])
def start(message):
    """
    This gives the user a custom keyboard with two options
    """
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton("Encrypt")
    itembtn2 = types.KeyboardButton("Decrypt")
    markup.add(itembtn1,itembtn2)
    bot.send_message(message.chat.id, "Hi! Welcome to Steganography bot. Choose an option below.", reply_markup=markup)
   

@bot.message_handler(func=lambda m: True)
def userOption(message):
    """
    Depending on whether user selects Encrypt or Decrypt, this will 
    """
    if message.text == 'Encrypt':
        #bot.send_message(message.chat.id, "Select and send an image.")
        state = 'Encrypt'
        msg = bot.reply_to(message,"Select and send an image." )
        bot.register_next_step_handler(msg, recieveImage, state)
    elif message.text == "Decrypt":
        state = "Decrypt"
        msg = bot.reply_to(message,"Select and send an image." )
        bot.register_next_step_handler(msg, recieveImage, state)
    else:
        bot.send_message(message.chat.id, "Please use /start again.")

    

def recieveImage(message, state):
    """
    Recieved images for both encrypt and decrypt function
    """
    if message.content_type != "photo":
        bot.send_message(message.chat.id, "Wrong image file, please select and send an image Make sure you send it the quick way.")
        bot.register_next_step_handler(message,recieveImage)
    elif message.content_type == "photo":
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(APIKey, file_info.file_path))
        filename = "photosIn/" + file_id + '.jpg'
        with open(filename, 'wb') as f:
            f.write(file.content)

        if state == "Encrypt":
            msg = bot.reply_to(message, "Photo recieved. Please key in your message.")
            bot.register_next_step_handler(msg, encryptImage, filename)
        if state == "Decrypt":
            msg = bot.reply_to(message, "Photo recieved.")
            bot.register_next_step_handler(msg, decryptMessage)


def encryptImage(message, filename):
    """
    Gets both message to be encrypted and image, returns the image.
    """
    bot.send_message(message.chat.id, f"Your message to be encrypted is {message.text}, and the photo is the following.")
    bot.send_photo(message.chat.id, photo=open(filename, "rb"))
    #Write function for encryption
    
def decryptMessage(message,filename):
    """
    Need to write a function that decrypts the thing and sends it back.
    """
    output = "Test output"
    bot.send_message(message.chat.id, f"Decrypted Message: {output}")



# @bot.message_handler(commands=['privKey'])
# def getPrivKey(message):
#     privKey = message.text.split()[1]
#     bot.send_message(message.chat.id, f"Your private key is {privKey}")
    
# @bot.message_handler(content_types=['photo'])
# def handle_photo(message):
#     bot.send_message(message.chat.id, "Photo recieved")

# @bot.message_handler(func=lambda m: True)
# def handle_photo(message):
#     bot.send_message(message.chat.id, "Message recieved")


bot.polling()

