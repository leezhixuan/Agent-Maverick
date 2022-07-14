import os
import telebot
import requests

from dotenv import load_dotenv
from telebot import types
from collections import defaultdict
from steganography import encodeText, decodeText 

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

messageIdDictionary = defaultdict(list)
photoIdDictionary = defaultdict(list)


@bot.message_handler(commands=['start'])
def start(message):
    """
    This gives the user a custom keyboard with two options
    """
    if message.content_type != "text":
        # markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        # itembtn1 = types.KeyboardButton("Encrypt")
        # itembtn2 = types.KeyboardButton("Decrypt")
        # markup.add(itembtn1,itembtn2)
        messageOutId = bot.send_message(message.chat.id, "Please select an option.", reply_markup=markup).message_id
        #Append messageOutID
        messageIdDictionary[message.chat.id].append(messageOutId)

    elif message.content_type == "text":
        #Updating googlesheet with sessionID
        # newUser = User(message.chat.id, message.from_user.first_name, message.from_user.last_name)
        # gc.updateUser(newUser)
        #Append messageInID
        messageIdDictionary[message.chat.id].append(message.message_id)
        #Send custom keyboard
        markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        itembtn1 = types.KeyboardButton("Encrypt")
        itembtn2 = types.KeyboardButton("Decrypt")
        markup.add(itembtn1,itembtn2)
        messageOutId = bot.send_message(message.chat.id, "🤖Welcome to Steganography bot.🤖 Please choose an option below.☺️ Use /start at anytime to restart the process.🔁 Only PNG Files are ALLOWED!", reply_markup=markup).message_id
        #Append messageOutID
        messageIdDictionary[message.chat.id].append(messageOutId)


@bot.message_handler(func=lambda m: True)
def userOption(message):
    """
    Depending on whether user selects Encrypt or Decrypt, this will 
    """
    #Append messageInID
    messageIdDictionary[message.chat.id].append(message.message_id)
    #Handle Encrypt or Decrypt
    if message.text == 'Encrypt':
        #bot.send_message(message.chat.id, "Select and send an image.")
        state = 'Encrypt'
        msg = bot.reply_to(message,"🤖 Please select and send an [uncompressed] image 🤖" )
        messageOutId = msg.message_id
        bot.register_next_step_handler(msg, recieveImage, state)
        #Append messageOutID
        messageIdDictionary[message.chat.id].append(messageOutId)

    elif message.text == "Decrypt":
        state = "Decrypt"
        msg = bot.reply_to(message,"🤖 Please select and send an secret [uncompressed] image 🤖")
        messageOutId = msg.message_id
        bot.register_next_step_handler(msg, recieveImage, state)
        #Append messageOutID
        messageIdDictionary[message.chat.id].append(messageOutId)

    elif message.text == "Delete":
        clearChat(message)
    elif message.text =="Start":
        start(message)
    else:
        messageOutId = bot.send_message(message.chat.id, "🤖 Please use /start again 🤖").message_id
        #Append messageOutID
        messageIdDictionary[message.chat.id].append(messageOutId)


def promptDelete(chat_id):
    """
    Gives user the prompt to delete the chat. This is only triggered via custom keyboard.
    """
    #Send custom keyboard.
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton("Start")
    itembtn2 = types.KeyboardButton("Delete")
    markup.add(itembtn1,itembtn2)
    messageOutId = bot.send_message(chat_id, "After you are done, please clear the chat WITHIN 48 hours 🤖 \nPs: We wanna keep your secrets safe!🤫 ", reply_markup=markup).message_id
    messageIdDictionary[chat_id].append(messageOutId)

def recieveImage(message, state):
    """
    Recieved images for both encrypt and decrypt function.
    Need to check the output file TYPE
    """
    #Write code to handle if user fucking sends decrypt or encrypt
    #Append messageInID
    messageIdDictionary[message.chat.id].append(message.message_id)
    if message.content_type == "text":
        if message.text == "Encrypt":
            state = 'Encrypt'
            msg = bot.reply_to(message, "Please select and send an secret [uncompressed] image 🤖")
            messageOutId = msg.message_id
            bot.register_next_step_handler(msg, recieveImage, state)
            #Append messageOutID
            messageIdDictionary[message.chat.id].append(messageOutId)
        elif message.text == "Decrypt":
            state = "Decrypt"
            msg = bot.reply_to(message, "Please select and send an secret [uncompressed] image 🤖")
            messageOutId = msg.message_id
            bot.register_next_step_handler(msg, recieveImage, state)
            #Append messageOutID
            messageIdDictionary[message.chat.id].append(messageOutId)
        else:
            msg = bot.reply_to(message, "❌ Invalid input ❌ Please use /start again 🔁")
            messageOutId = msg.message_id
            messageIdDictionary[message.chat.id].append(messageOutId)

    elif message.content_type != "document":
        messageOutId =bot.send_message(message.chat.id, "❌❌ Wrong image file ❌❌ \nPlease select and send an image as a file.").message_id
        messageIdDictionary[message.chat.id].append(messageOutId)
        bot.register_next_step_handler(message,recieveImage, state)

    elif message.content_type == "document":
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))
        filename = "telegramBot/photosIn/"  + message.document.file_name  
        with open(filename, 'wb') as f:
            f.write(file.content)
        #Add filename to list to remove later
        photoIdDictionary[message.chat.id].append(filename)

        if state == "Encrypt":
            msg = bot.reply_to(message, "✅ Photo file received ✅ \nPlease key in your secret message now 👀 \nOr use /start to restart the process 🔁 ")
            messageOutId = msg.message_id
            bot.register_next_step_handler(msg, handleEncryption, filename)
            #Append messageOutID
            messageIdDictionary[message.chat.id].append(messageOutId)
        if state == "Decrypt":
            decrypted = decodeText(filename)
            if decrypted == "not done":
                msg = bot.reply_to(message, f"❌❌ Image is not encoded yet ❌❌ \nPlease encrypt the image first.")
            else:
                msg = bot.reply_to(message, f"✅ Decoded Message is: \n {decrypted} ") 
            messageOutId = msg.message_id
            # bot.register_next_step_handler(msg, decryptMessage, filename)
            #Append messageOutID
            messageIdDictionary[message.chat.id].append(messageOutId)
            #Prompts delete
            promptDelete(message.chat.id)


def handleEncryption(message,filename):
    """
    Gets both message to be encrypted and image, returns the image.
    """
    if message.content_type != 'text':
        msg = bot.reply_to(message, "❌❌ Invalid input ❌❌ \nPlease use /start again.🔁")
        messageOutId = msg.message_id
        messageIdDictionary[message.chat.id].append(messageOutId)
    if message.content_type == "text":
        if message.text == "/start":
            start(message)
        else:
            #Append messageInID
            messageIdDictionary[message.chat.id].append(message.message_id)
            #Encrypt
            imageFile = open(filename, 'rb')
            messageOutId = bot.send_message(message.chat.id, f"Your message is encrypted safely🎉, and the photo is the following... 🤫").message_id
            messageIdDictionary[message.chat.id].append(messageOutId)

            encodeText(message.text, filename)

            #Sends it back
            messageOutId = bot.send_document(message.chat.id, imageFile).message_id #Sents encrypted photo back
            messageIdDictionary[message.chat.id].append(messageOutId)
            #Prompts delete
            promptDelete(message.chat.id)


def clearChat(message):
    """
    Telegram API does not allow you to clear chat with a bot, hence this just a reminder to clear the chat for the user.
    """ 
    chat_id = message.chat.id
    for id in messageIdDictionary[chat_id][2:]:
        try:
            bot.delete_message(chat_id,id)
        except:
            continue 
    messageIdDictionary[chat_id] = []
    clearLocalImages(chat_id)


def clearLocalImages(chat_id):
    """
    Given chat_id, remove all instances of local image.
    """
    if len(photoIdDictionary[chat_id]) == 0:
        pass
    else:
        for photoFile in photoIdDictionary[chat_id]:
            os.remove(photoFile)
    photoIdDictionary[chat_id] = []


bot.polling()




