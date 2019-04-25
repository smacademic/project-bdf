# TextifyBot.py - Team BDF - CS 298-01 S19 WCSU

# This python script transcribes text from images in comments and submissions
# that have been requested by a Reddit comment

import os
import urllib.request
import botSetup
import authentication
import praw
import PIL
import pytesseract
import json
import requests
from PIL import Image
import time
import math
import TextifyTranslate
from googlesearch import search


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
TRANSLATE_FLAG = '!Translation'
CV_KEYWORD = "!describe" # keyword for providing a description of an image
TWITTER_FLAG = '!Twitter';



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
        if urls == None:
            if CHECKER:
                mention.reply("No URL(s) found")
        elif CV_KEYWORD in mention.body.lower():
            print('URL(s) found:')
            print(urls)
            result = describeImages(urls)
            print("Descriptions:")
            print(result)
            makeReply(mention, result)
        else:
            print('URL(s) found:')
            print(urls)
            print('Text transcribed:')
            result = transcribeImages(urls)
            print(result)
            if CHECKER:
                if arrayToString(result) == '' or arrayToString(result) == ' ':
                    mention.reply("Transcription was unable to identify any text within the image")
                else:
                    makeReply(mention, result)
    elif isinstance(mention.parent(), praw.models.Submission):
        urls = botSetup.extractURL(mention.parent().url)
        if urls == None:
            if CHECKER:
                mention.reply("No URL(s) found")
        elif CV_KEYWORD in mention.body.lower():
            print('URL(s) found:')
            print(urls)
            result = describeImages(urls)
            print("Descriptions:")
            print(result)
            makeReply(mention, result)
        else:
            print('URL(s) found:')
            print(urls)
            print('Text transcribed:')
            result = transcribeImages(urls)
            print(result)
            if CHECKER:
                if arrayToString(result) == '' or arrayToString(result) == ' ':
                    mention.reply("Transcription was unable to identify any text within the image")
                else:
                    makeReply(mention, result)
        else:
            if CHECKER:
                mention.reply("No URL(s) found")

# - Post's subreddit must not be in blacklist
# - Post's subreddit must not be NSFW (+18)
# - Post's subreddit must not be in blacklist OR

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


def makeReply(mention, transcriptions):
    response = arrayToString(transcriptions)

    #check for twitter flag
    if mention.body.find(TWITTER_FLAG) >=0:
        print("Twitter flag found, searching google for link...")
        twitterLink = googleSearch(response)
        if twitterLink != None:
            response = response + '\n\n' + twitterLink
        else:
            print("unable to find link")
            response = response + '\n\nUnable to find associated twitter link'
                
    #check for translation flag
    if mention.body.find(TRANSLATE_FLAG) >=0:
        for langCode in TextifyTranslate.LANGUAGE_CODE:
            if mention.body.find(langCode, 29) >=0:
                print("translating to : " + langCode )
                response = TextifyTranslate.translate(response, langCode)

    MAX_POST_LEN = 10000 # Reddit imposes a cap of 10000 characters for comments
    HEADER_LEN = 21 # Length of "### Reply x of x:\n\n"

    if len(response) < MAX_POST_LEN:
        mention.reply(response)
    else:
        numReplies = math.ceil(len(response) / (MAX_POST_LEN + HEADER_LEN))
        currReplyNum = 1
        while len(response) > MAX_POST_LEN - HEADER_LEN:
            currReply = "### Reply " + str(currReplyNum) + " of " + str(numReplies) + ":\n\n"
            currReply += response[0:MAX_POST_LEN - HEADER_LEN]
            mention.reply(currReply)

            response = response[MAX_POST_LEN - HEADER_LEN:]
            currReplyNum += 1
        currReply = "### Reply " + str(currReplyNum) + " of " + str(numReplies) + ":\n\n"
        currReply += response
        mention.reply(currReply)


def tesseractTranscribe(imagePath):
    image = PIL.Image.open(imagePath)
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

    return pytesseract.image_to_string(image)


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
                imageText = escapeMarkdown(imageText)
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


def describeImages(imagesToProcess):
    cvEndPoint = authentication.cvBaseURL + "/vision/v2.0/analyze"
    callHeader = {"Ocp-Apim-Subscription-Key": authentication.cvKey1}
    callParams = {'visualFeatures': "Categories,Description,Color"}

    imageDescriptions = []

    currentImageNumber = 1
    for imageURL in imagesToProcess:
        imageURL = imageURL.rstrip('/')
        callData = {"url": imageURL}

        response = requests.post(cvEndPoint, headers=callHeader, params=callParams, json=callData)
        response.raise_for_status()

        result = response.json()
        print("Computer Vision result: " + str(json.dumps(result)))

        if len(result["description"]["captions"]) > 0:
            imageCaption = result["description"]["captions"][0]["text"]
            captionConfidence = result["description"]["captions"][0]["confidence"]
            message = "I am " + str(captionConfidence * 100) \
              + "% sure that this is: **" + imageCaption + "**\n"
        else:
            message = "Sorry, I could not describe that image\n"

        if len(imagesToProcess) > 1:
            message = "- Image " + str(currentImageNumber) + ": " + message
            currentImageNumber += 1

        imageDescriptions.append(message)

    return imageDescriptions


#Extract characters from array into a string variable
def arrayToString(textArray):
    str1 = ""
    for x in textArray:
        str1 = str1 + x
    return str1


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


# If twitter keyword is used, search google to see if link to tweet can be found
def googleSearch(response):
    for link in search(response, tld="com", num=10, stop=1, pause=2):
        if link.find('twitter') >= 0:
            print('found twitter link: ' + link)
            return 'Twitter link found: ' + link
        else:
            return getTwitterUsernames(response)

    #have to chek here as well in case the search returns no results
    #if the search for the entire tweet returns no results, which it will occassionally with jumbled transcriptions,
    #the above for loop will immediately exit
    if getTwitterUsernames(response) == None:
        return None
    else:
        return getTwitterUsernames(response)


#if google search is unable to find specific tweet, will attempt to find the twitter user page
def getTwitterUsernames(response):
    twitterUsernames = extractUsername(response)
    usernameList = ''
    for username in twitterUsernames:
        if username != None:
            for link in search(username, tld="com", num=10, stop=1, pause=2):
                if link.find('twitter') >= 0:
                    usernameList = usernameList + '\n\n' + link
                    print('found twitter user page: ' + link)

    if usernameList == None:
        return None
    else:
        return 'Twitter user(s) found: ' + usernameList


# If tweet is not able to be found, extract username from tweet and return it to search for it
def extractUsername(response):
    responseSplit = response.split()
    usernames = []

    for word in responseSplit:
        if word.find('@') >= 0:
            usernames.append(word)

    return usernames


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
