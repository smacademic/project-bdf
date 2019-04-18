import authentication
import tweepy


auth = tweepy.OAuthHandler(authentication.consumer_key, authentication.consumer_secret)
auth.set_access_token(authentication.access_token, authentication.access_token_secret)
api = tweepy.API(auth)

user = api.me()
print (user.name)
