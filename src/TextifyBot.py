# TextifyBot.py - Team BDF - CS 298-01 S19 WCSU

# This python script identified comments that should eventually be processed
# by our bot within a specific set of subreddits

import os
import urllib.request
import botSetup
import praw
import PIL
import pytesseract


KEYWORD = '!TextifyReddit' # what to look for to know when the bot is called
SUBREDDIT = 'BDFTest' # subreddit to search for comments in (multiple subreddits
                      # can be specified by placing a '+' between them)
IMAGE_DIR = 'images/' # directory to temporarily download images to
TESSERACT_PATH = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def findTextInSubreddit(connection, sub, keyword):

    checker = True

    for submission in connection.subreddit(sub).hot(limit=10):
        # this code is not well-optimized for deeply nested comments. See:
        # https://praw.readthedocs.io/en/latest/code_overview/models/comment.html
        for comment in submission.comments.list():
            if (comment.body.find(keyword)) >= 0:
                if isinstance(comment.parent(), praw.models.Comment):
                    urls = botSetup.extractURL(comment.parent().body)
                    print('Comment to textify:')
                    print(comment.parent().body)
                    if urls != None:
                        print('URL(s) found:')
                        print(urls)
                        print('Text transcribed:')
                        print(transcribeImages(urls))
                        if checker:
                            comment.reply(transcribeImages(urls))
                            checker = False
                else:
                    print('Submission to textify:')
                    print(comment.parent().url)
                        if checker:
                            comment.reply(transcribeImages(urls))
                            checker = False


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
findTextInSubreddit(bot, SUBREDDIT, KEYWORD)
