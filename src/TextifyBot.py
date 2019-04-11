# TextifyBot.py - Team BDF - CS 298-01 S19 WCSU

# This python script transcribes text from images in comments and submissions
# that have been requested by a Reddit comment

import os
import urllib.request
import botSetup
import praw
import PIL
import pytesseract
from PIL import Image
import time
# The following are exceptions that are thrown when there are network issues
from socket import gaierror
from urllib3.exceptions import NewConnectionError
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectionError
from prawcore.exceptions import RequestException


# Note: both WHITELIST and BLACKLIST are case insensitive; WHITELIST overrides
# BLACKLIST if a subreddit exists in both lists
WHITELIST = ['BDFTest'] # list of subreddits where bot is allowed to transcribe
                        # posts. If the first item in the list is '*' the bot
                        # is allowed to post in any subreddit not in BLACKLIST.
BLACKLIST = [] # list of subreddits where bot is not allowed to transcribe posts
IMAGE_DIR = 'images/' # directory to temporarily download images to
TESSERACT_PATH = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
CHECKER = True # enables posting to Reddit


def processUsernameMentions(connection):
    for newMsg in connection.inbox.unread():
        if isinstance(newMsg, praw.models.Comment) and isMention(newMsg):
            processMention(newMsg)
            if CHECKER:
                newMsg.mark_read()


def isMention(message):
    if isinstance(message, praw.models.Comment):
        return message.subject == 'username mention'
    else:
        return False


def processMention(mention):
    if isinstance(mention.parent(), praw.models.Comment) and \
    allowedToParse(mention.parent()):
        urls = botSetup.extractURL(mention.parent().body)
        print('Comment to textify:')
        print(mention.parent().body)
        if urls != None:
            print('URL(s) found:')
            print(urls)
            print('Text transcribed:')
            result = transcribeImages(urls)
            print(result)
            if CHECKER:
                if arrayToString(result) == '' or arrayToString(result) == ' ':
                    mention.reply("Transcription was unable to identify any text within the image")
                else:
                    mention.reply(arrayToString(result))
        else:
            if CHECKER:
                mention.reply("No URL(s) found")
    elif isinstance(mention.parent(), praw.models.Submission):
        urls = botSetup.extractURL(mention.parent().url)
        if urls != None:
            print('URL(s) found:')
            print(urls)
            print('Text transcribed:')
            result = transcribeImages(urls)
            print(result)
            if CHECKER:
                if arrayToString(result) == '' or arrayToString(result) == ' ':
                    mention.reply("Transcription was unable to identify any text within the image")
                else:
                    mention.reply(arrayToString(result))
        else:
            if CHECKER:
                mention.reply("No URL(s) found")
# - Post's subreddit must not be in blacklist
# - Post's subreddit must be in whitelist if whitelist is not disabled by '*'
def allowedToParse(postID):
    if postID.subreddit.over18:
        return False

    if WHITELIST[0] == '*':
        return postID.subreddit.display_name.lower() not in \
            (name.lower() for name in BLACKLIST)
    else:
        return postID.subreddit.display_name.lower() in \
            (name.lower() for name in WHITELIST)


def tesseractTranscribe(imagePath):
    image = PIL.Image.open(improveImage(imagePath))
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

    return pytesseract.image_to_string(image)


# Makes the given image larger to improve success of transcription
def improveImage(imagePath):
    image = Image.open(imagePath)
    width = image.width
    height = image.height
    image = image.resize((width*2, height*2))
    image.save(imagePath)
    return imagePath


def transcribeImages(imagesToDL): # download and transcribe a list of image URLs
    transcribedText = []
    transcriptionSpacing = "\n---\n"

    for imageURL in imagesToDL:
        imageURL = imageURL.rstrip('/')

        # rpartition returns a 3-tuple: (pre-last-separator, separator,
        #                                post-last-separator)
        imageName = imageURL.rpartition('/')[2]

        if imageName != '':
            imagePath = IMAGE_DIR + imageName

            try:
                urllib.request.urlretrieve(imageURL, imagePath)
                imageText = tesseractTranscribe(imagePath)
                transcribedText.append(transcriptionSpacing)
                transcribedText.append(imageText)
                os.remove(imagePath)
            except urllib.error.HTTPError as e:
                print("WARNING: HTTPError when downloading " + imageURL + ":\n")
                print(str(e) + '\n')
                transcribedText = "HTTPError when downloading"
            except ValueError as e:
                print("Unknown URL type: " + imageURL + ":\n")
                print(str(e) + '\n')
                transcribedText = "Unknown URL type"
    return transcribedText

#Extract characters from array into a string variable
def arrayToString(textArray):
    str1 = ""
    for x in textArray:
        str1 = str1 + x
    return escapeMarkdown(str1)

#Function to properly format new lines
def escapeMarkdown(str1):
    markdownSyntax = ['#','*','_','+','\n']
    newString = ""
    for char in markdownSyntax:
        if char == '\n':
            x = 0
            while x < len(str1):
                index1 = str1.find(char, x)
                index2 = str1.find(char, index1 + 1)
                if index1 == -1:
                    break
                elif index1 - index2 == -1:
                    x = index1 + 2
                else:
                    newString = str1[:index1] + char + str1[index1:]
                    str1 = newString
                    x = index1 + 2
        else:
            x = 0
            while x < len(str1):
                index1 = str1.find(char, x)
                if index1 == -1:
                    break
                else:
                    newString = str1[:index1] + '\\' + str1[index1:]
                    str1 = newString
                    x = index1 + 2
    return newString

# Main driver code
if __name__ == '__main__': # This if statement guards this code from being executed when this file is imported
    bot = botSetup.textify_login()
    while True:
        try:
            processUsernameMentions(bot)
            time.sleep(5)
        except(gaierror, NewConnectionError, MaxRetryError, ConnectionError, RequestException):
            print("It looks like there is a network issue. Retrying in 30 seconds...")
            time.sleep(30)
