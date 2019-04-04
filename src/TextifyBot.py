# TextifyBot.py - Team BDF - CS 298-01 S19 WCSU

# This python script transcribes text from images in comments and submissions
# that have been requested by a Reddit comment

import os
import urllib.request
import botSetup
import praw
import PIL
import pytesseract
import time

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
            print(transcribeImages(urls))
            if CHECKER:
                mention.reply(str(transcribeImages(urls)))
    elif isinstance(mention.parent(), praw.models.Submission):
        print('Submission to textify:')
        print(mention.parent().url)
        if CHECKER:
            mention.reply(str(transcribeImages(urls)))


# Returns true if bot is allowed to parse the post. The following rules apply:
# - Post's subreddit must not be marked NSFW
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
    image = PIL.Image.open(imagePath)
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

    return pytesseract.image_to_string(image)


def transcribeImages(imagesToDL): # download and transcribe a list of image URLs
    transcribedText = []
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
                transcribedText.append(imageText)
                os.remove(imagePath)
            except urllib.error.HTTPError as e:
                print("WARNING: HTTPError when downloading " + imageURL + ":\n")
                print(str(e) + '\n')
    return transcribedText


# Main driver code
if __name__ == '__main__': # This if statement guards this code from being executed when this file is imported
    bot = botSetup.textify_login()
    while True:
        processUsernameMentions(bot)
        time.sleep(5)
