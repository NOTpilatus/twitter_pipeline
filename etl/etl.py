import time
import logging
from pymongo import MongoClient
from sqlalchemy import create_engine 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import psycopg2



client = MongoClient(host = 'mongodb', port = 27017)
mongo_db = client.twitter_pipeline
tweet_collection = mongo_db.tweets

HOST = 'mypg'
USERNAME = 'postgres'
PORT = '5432'
DB = 'postgres'
PASSWORD = '1234'

engine = create_engine(f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}')

#Create table in the Postgres Database

DROP_QUERY = ''' DROP TABLE IF EXISTS tweets;

            '''
CREATE_QUERY = ''' CREATE TABLE IF NOT EXISTS tweets
                   (
                    
                    username VARCHAR(50),
                   text VARCHAR(500),
                   sentiment_score NUMERIC
                   );'''

engine.execute(DROP_QUERY)
engine.execute(CREATE_QUERY)

s = SentimentIntensityAnalyzer()


def extract():
    '''Extracts tweets from the MongoDB database'''
    tweets = list(tweet_collection.find())
    return tweets


def transform(tweets):
    '''Performs sentiment analysis on extracted tweets'''

    for tweet in tweets:
        tweet['sentiment_score'] = s.polarity_scores(tweet['text'])['compound']

    return tweets


def load(tweets):

    '''Loads transformed tweets into postgres DB '''

    insert_query = 'INSERT INTO tweets VALUES (%s, %s, %s)'
    for tweet in tweets:
        engine.execute(insert_query, (tweet['username'], tweet['text'], tweet['sentiment_score']))



while True:
    time.sleep(10)
    extracted_tweets = extract()
    transformed_tweets = transform(extracted_tweets)
    load(transformed_tweets)
    logging.warning('----New list of tweets has been written into the Postgres database')


    




