import config
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json
import logging
from pymongo import MongoClient



client = MongoClient(host = 'mongodb', port = 27017) # hostname: MongoDB Container
mongo_db = client.twitter_pipeline
tweet_collection = mongo_db.tweets


def authenticate():
    """Function for handling Twitter Authentication.
    """
    auth = OAuthHandler(config.CONSUMER_API_KEY, config.CONSUMER_API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    return auth

class TwitterListener(StreamListener):

    def on_data(self, data):

        """Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""

        t = json.loads(data) 
        tweet = {
        'text': t['text'],
        'username': t['user']['screen_name'],
        'followers_count': t['user']['followers_count']
        }

        logging.critical(f'\n\n\nTWEET INCOMING: {tweet["text"]}\n\n\n')
        tweet_collection.insert({'username' : tweet['username'],'followers_count' : tweet['followers_count'], 'text' : tweet['text']})


    def on_error(self, status):

        if status == 420:
            print(status)
            return False






if __name__ == '__main__':
    
    auth = authenticate()
    listener = TwitterListener()
    stream = Stream(auth, listener)
    stream.filter(track=['berlin'], languages=['de'])

    
