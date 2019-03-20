# TextifyBot.py - Team BDF - CS 298-01 S19 WCSU

# This python script identified comments that should eventually be processed by our bot
# within a specific set of subreddits

import os
import time # temporary for testing image saving
import urllib.request
import botSetup
import praw


KEYWORD = '!TextifyReddit' # what to look for to know when the bot is called
SUBREDDIT = 'BDFTest' # subreddit to search for comments in (multiple subreddits
                      # can be specified by placing a '+' between them)
IMAGE_DIR = 'images/' # directory to temporarily download images to


numComments = 0 # total number of comments parsed
numRequests = 0 # number of comments with KEYWORD


bot = botSetup.textify_login()

def findTextInSubreddit(connection, sub): # pass subreddit name in to search for !TextifyReddit
    for submission in connection.subreddit(sub).hot(limit=10):
        # this code is not well-optimized for deeply nested comments
        # see https://praw.readthedocs.io/en/latest/code_overview/models/comment.html#praw.models.Comment.parent
        for comment in submission.comments.list():
            numComments += 1
            if (comment.body.find(KEYWORD)) >= 0:
                numRequests += 1
                if isinstance(comment.parent(), praw.models.Comment):
                    urls = botSetup.extractURL(comment.parent().body)
                    print('Comment to textify:')
                    print(comment.parent().body)
                    if urls != None:
                        print('URL(s) found:')
                        print(urls)
                        transcribeImages(urls)
                else:
                    print('Submission to textify:')
                    print(comment.parent().url)


# download image given a URL
imagesToDL = urls
def transcribeImages(imagesToDL): # list of image URLs to download
    transcribedText = []
    for imageURL in imagesToDL:
        imageURL = imageURL.rstrip('/')

        # rpartition returns a 3-tuple: (pre-last-separator, separator, post-last-separator)
        imageName = imageURL.rpartition('/')[2]
        
        if imageName != '':
            imagePath = IMAGE_DIR + imageName
            urllib.request.urlretrieve(imageURL, imagePath)
            time.sleep(5) # TEMP: Allows time for inspecting image
            # TODO: Process image
            os.remove(imagePath)

    return transcribedText


print('Number of comments parsed: ', numComments)
print('Number of TextifyCalls identified: ', numRequests)
