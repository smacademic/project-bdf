# TextifyBot.py - Team BDF - CS 298-01 S19 WCSU

# This python script identified comments that should eventually be processed by our bot
# within a specific set of subreddits

import praw
from praw.models import Comment
import re

KEYWORD = '!TextifyReddit' # what to look for to know when the bot is called
SUBREDDIT = 'BDFTest' # subreddit to search for comments in (multiple subreddits
                      # can be specified by placing a '+' between them)

# build Reddit instance using TextifyReddit's credentials
reddit = praw.Reddit(client_id='', # 14 characters
                     client_secret='', # 27 characters
                     user_agent='script:smacademic.project-bdf.textifyreddit:v0.0.20190308 (by /u/TextifyReddit)')


numComments = 0 # total number of comments parsed
numRequests = 0 # number of comments with KEYWORD

# splits comment sentence into individual words then parses words 
# to find if they end in popular image format
def extractURL(comment):
    commentSplit = re.split('\s', comment)
    
    imageList = []

    for word in commentSplit:
        #these variables store the image URL if it is enclosed within parentheses
        jpgWithParens = re.search('\((.*\.jpg)\)$', word)
        pngWithParens = re.search('\((.*\.png)\)$', word)
        tifWithParens = re.search('\((.*\.tif)\)$', word)
        
        #these variables store the image URL if it is not enclosed with any special characters
        jpg = re.search('(.*\.jpg$)', word)
        png = re.search('.*\.png$', word)
        tif = re.search('.*\.tif$', word)
        
        if jpgWithParens != None:
            imageList.append(jpgWithParens.group(1))
        elif pngWithParens != None:
            imageList.append(pngWithParens.group(1))
        elif tifWithParens != None:
            imageList.append(tifWithParens.group(1))
        elif jpg != None:
            imageList.append(jpg.group(1))
        elif png != None:
            imageList.append(png.group(1))
        elif tif != None:
            imageList.append(tif.group(1))
    
    if imageList:
        return imageList

for submission in reddit.subreddit(SUBREDDIT).hot(limit=10):
    # this code is not well-optimized for deeply nested comments
    # see https://praw.readthedocs.io/en/latest/code_overview/models/comment.html#praw.models.Comment.parent
    for comment in submission.comments.list():
        numComments += 1
        if (comment.body.find(KEYWORD)) >= 0:
            numRequests += 1
            if isinstance(comment.parent(), Comment):
                url = extractURL(comment.parent().body)
                print('Comment to textify:')
                print(comment.parent().body)
                if url != None:
                    print('URL found:')
                    print(url)
            else:
                print('Submission to textify:')
                print(comment.parent().url)


print('Number of comments parsed: ', numComments)
print('Number of TextifyCalls identified: ', numRequests)
