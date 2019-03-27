# TextifyBot.py - Team BDF - CS 298-01 S19 WCSU

# This python script identified comments that should eventually be processed
# by our bot within a specific set of subreddits

import os
import urllib.request
import botSetup
import praw
import PIL
import pytesseract

# Note: both WHITELIST and BLACKLIST are case insensitive; WHITELIST overrides
# BLACKLIST if a subreddit exists in both lists
WHITELIST = ['BDFTest'] # list of subreddits where bot is allowed to transcribe
                        # posts. If the first item in the list is '*' the bot
                        # is allowed to post in any subreddit not in BLACKLIST.
BLACKLIST = [] # list of subreddits where bot is not allowed to transcribe posts
IMAGE_DIR = 'images/' # directory to temporarily download images to
TESSERACT_PATH = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def findTextInSubreddit(connection):
    for mention in connection.inbox.mentions(limit=None):
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
        elif isinstance(mention.parent(), praw.models.Submission):
            print('Submission to textify:')
            print(mention.parent().url)

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
bot = botSetup.textify_login()
findTextInSubreddit(bot)
