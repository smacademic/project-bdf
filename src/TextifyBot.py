# TextifyBot.py - Team BDF - CS 298-01 S19 WCSU

# This python script identified comments that should eventually be processed
# by our bot within a specific set of subreddits

import os
import urllib.request
import botSetup
import praw
import PIL
import pytesseract


SUBREDDIT = 'BDFTest' # subreddit to search for comments in (multiple subreddits
                      # can be specified by placing a '+' between them)
IMAGE_DIR = 'images/' # directory to temporarily download images to
TESSERACT_PATH = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def findTextInSubreddit(connection):
    for mention in connection.inbox.mentions(limit=None):
        if isinstance(mention.parent(), praw.models.Comment):
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
