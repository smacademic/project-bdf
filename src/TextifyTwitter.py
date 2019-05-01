from googlesearch import search

def googleSearch(response):
    for link in search(response, tld="com", num=10, stop=1, pause=2):
        if link.find('twitter') >= 0:
            print('found twitter link: ' + link)
            return 'Twitter link found: ' + link
        else:
            return getTwitterUsernames(response)

    #have to chek here as well in case the search returns no results
    #if the search for the entire tweet returns no results, which it will occassionally with jumbled transcriptions,
    #the above for loop will immediately exit
    if getTwitterUsernames(response) == None:
        return None
    else:
        return getTwitterUsernames(response)

#if google search is unable to find specific tweet, will attempt to find the twitter user page
def getTwitterUsernames(response):
    twitterUsernames = extractUsername(response)
    usernameList = ''
    for username in twitterUsernames:
        if username != None:
            for link in search(username, tld="com", num=10, stop=1, pause=2):
                if link.find('twitter') >= 0:
                    usernameList = usernameList + '\n\n' + link
                    print('found twitter user page: ' + link)

    if usernameList == None:
        return None
    else:
        return 'Twitter user(s) found: ' + usernameList


# If tweet is not able to be found, extract username from tweet and return it to search for it
def extractUsername(response):
    responseSplit = response.split()
    usernames = []

    for word in responseSplit:
        if word.find('@') >= 0:
            usernames.append(word)

    return usernames
