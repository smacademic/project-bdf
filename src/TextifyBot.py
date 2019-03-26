# TextifyBot.py - Team BDF - CS 298-01 S19 WCSU

# This python script transcribes text from images in comments and submissions
# that have been requested by a Reddit comment

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
POST_LEDGER = 'processedPosts.txt' # file that contains a list of IDs of
                                   # comments and submissions that have been
                                   # processed (delim: \n)


def findTextInSubreddit(connection, sub, keyword):
    for submission in connection.subreddit(sub).hot(limit=10):
        # this code is not well-optimized for deeply nested comments. See:
        # https://praw.readthedocs.io/en/latest/code_overview/models/comment.html
        for comment in submission.comments.list():
            if comment.body.find(keyword) >= 0 and not \
                isPostIDProcessed(comment.parent().id):
                if isinstance(comment.parent(), praw.models.Comment):
                    urls = botSetup.extractURL(comment.parent().body)
                    print('Comment to textify:')
                    print(comment.parent().body)
                    if urls != None:
                        print('URL(s) found:')
                        print(urls)
                        print('Text transcribed:')
                        print(transcribeImages(urls))
                    markPostIDAsProcessed(comment.parent().id)
                elif isinstance(comment.parent(), praw.models.Submission):
                    print('Submission to textify:')
                    print(comment.parent().url)
                    markPostIDAsProcessed(comment.parent().id)


# Checks if a comment or submission ID has already been parsed for image URLS
def isPostIDProcessed(id):
    with open(POST_LEDGER, 'a+') as ledger:
        ledger.seek(0,0)
        for line in ledger:
            if id in line:
                return True
        return False


# Adds an ID to the list of processed IDs. A comment or post should only be
# added if it has been scanned for URLs and transcribed
def markPostIDAsProcessed(id):
    with open(POST_LEDGER, 'a') as ledger:
        ledger.write(id + '\n')


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
