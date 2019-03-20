# Temporary solution to test the extractURL function in TextifyBot.py

import re

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

# Test Data
testData1 = 'Hello my name is Brian, I am taking Devops this Spring 2019'
testData2 = 'Https://imgur.com/jfkdlsja.jpg'
testData3 = '[This is a link](https://facebook.com/image.png) <- check out this link'
testData4 = 'https://google.com/fjdlksaf.tif https://google.com/789fdsfh.png https://imgur.com/jfldk.jpg'
testData5 = 'I think that you will find this image useful [https://google.com/fjkd.png](https://google.com/fjkd.png) Let me know what you think'

print(extractURL(testData1))
print(extractURL(testData2))
print(extractURL(testData3))
print(extractURL(testData4))
print(extractURL(testData5))