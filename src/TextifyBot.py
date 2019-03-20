# TextifyBot.py - Team BDF - CS 298-01 S19 WCSU

# This python script identified comments that should eventually be processed by our bot
# within a specific set of subreddits

import praw
import os
import time # temporary for testing image saving
import urllib.request

from praw.models import Comment

KEYWORD = '!TextifyReddit' # what to look for to know when the bot is called
SUBREDDIT = 'BDFTest' # subreddit to search for comments in (multiple subreddits
                      # can be specified by placing a '+' between them)
IMAGE_DIR = 'images/' # directory to temporarily download images to

# build Reddit instance using TextifyReddit's credentials
reddit = praw.Reddit(client_id='', # 14 characters
                     client_secret='', # 27 characters
                     user_agent='script:smacademic.project-bdf.textifyreddit:v0.0.20190308 (by /u/TextifyReddit)')


numComments = 0 # total number of comments parsed
numRequests = 0 # number of comments with KEYWORD

for submission in reddit.subreddit(SUBREDDIT).hot(limit=10):
    # this code is not well-optimized for deeply nested comments
    # see https://praw.readthedocs.io/en/latest/code_overview/models/comment.html#praw.models.Comment.parent
    for comment in submission.comments.list():
        numComments += 1
        if (comment.body.find(KEYWORD)) >= 0:
            numRequests += 1
            if isinstance(comment.parent(), Comment):
                print('Comment to textify:')
                print(comment.parent().body)
            else:
                print('Submission to textify:')
                print(comment.parent().url)


# download image given a URL
imagesToDL = ['https://i.redd.it/hovk55p9xty01.jpg', 'https://i.redd.it/slo0elpdf9n21.jpg/',
              'https://i.redd.it/3p7qj2zbr9n21.png', 'https://i.imgur.com/VDpcFrz.jpg']

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


print('Number of comments parsed: ', numComments)
print('Number of TextifyCalls identified: ', numRequests)
