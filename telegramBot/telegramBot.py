import os
import telebot
import requests

from dotenv import load_dotenv
from telebot import types
from steganography import encodeText, decodeText 


load_dotenv()

API_TOKEN= os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

messageIdList = []

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
    messageIdList.append(message.message_id)

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
        messageIdList.append(message.message_id)
    elif message.text == "Decrypt":
        state = "Decrypt"
        msg = bot.reply_to(message,"Select and send an image." )
        bot.register_next_step_handler(msg, recieveImage, state)
        messageIdList.append(message.message_id)
    else:
        bot.send_message(message.chat.id, "Please use /start again.")
        messageIdList.append(message.message_id)

    

def recieveImage(message, state):
    """
    Recieved images for both encrypt and decrypt function.
    Need to check the output file TYPE
    """
    if message.content_type != "document":
        bot.send_message(message.chat.id, "Wrong image file, please select and send an image as a file.")
        bot.register_next_step_handler(message,recieveImage)
        messageIdList.append(message.message_id)
    elif message.content_type == "document":

        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))
        print(message.document.file_name)
        filename = "telegramBot/photosIn/" + message.document.file_name # change the file thingy 
        print(filename)
        with open(filename, 'wb') as f:
            f.write(file.content)
        print(state)
        if (state == "Encrypt"):
            msg = bot.reply_to(message, "Photo recieved. Please key in your message.")
            bot.register_next_step_handler(msg, encryptImage, filename)
            messageIdList.append(message.message_id)
        elif state == "Decrypt":
            msg = bot.reply_to(message, "Photo recieved.")
            bot.send_message(message.chat.id, f"Decrypted Message: {decryptMessage(message, filename)}") #Decrypted message
            messageIdList.append(message.message_id)


def encryptImage(message, filename):
    """
    Gets both message to be encrypted and image, returns the image.
    """
    imageFile = open(filename, 'rb')
    encodeText(message.text, filename)
    bot.send_message(message.chat.id, f"Your message to be encrypted is {message.text}, and the photo is the following.")
    bot.send_document(message.chat.id, imageFile) #Sents encrypted photo back
    messageIdList.append(message.message_id)
    #clearChat(message)
    
def decryptMessage(message, filename):
    """
    Need to write a function that decrypts the thing and sends it back.
    """
    decrypted = decodeText(filename)
    messageIdList.append(message.message_id)
    return decrypted


@bot.message_handler(commands=['delete'])
def clearChat(message):
    """
    Telegram API does not allow you to clear chat with a bot, hence this just a reminder to clear the chat for the user.
    """
    for id in messageIdList:
        bot.delete_message(message.chat.id,id)

bot.polling()

