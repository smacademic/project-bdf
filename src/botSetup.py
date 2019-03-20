# botSetup.py

import praw
from praw.models import Comment
import authentication # contains credentials for TextifyReddit account
import re # regex library

# build Reddit instance using TextifyReddit's credentials
def textify_login():
    bot = praw.Reddit(username = authentication.username,
                password = authentication.password,
                client_id = authentication.client_id,
                client_secret = authentication.client_secret,
                user_agent = authentication.user_agent)
    print("Logged in!")
    return bot


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
        png = re.search('(.*\.png$)', word)
        tif = re.search('(.*\.tif$)', word)
        
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


