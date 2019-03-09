# TextifyBot.py - Team BDF - CS 298-01 S19 WCSU

# This python script identified comments that should eventually be processed by our bot
# within a specific set of subreddits

import praw
from praw.models import Comment

KEYWORD = '!TextifyReddit' # what to look for to know when the bot is called
SUBREDDIT = 'BDFTest' # subreddit to search for comments in (multiple subreddits
                      # can be specified by placing a '+' between them)

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


print('Number of comments parsed: ', numComments)
print('Number of TextifyCalls identified: ', numRequests)
