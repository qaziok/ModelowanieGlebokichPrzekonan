import tweepy
import pandas as pd
from TwitterAnalisis import *
import twint


def connect():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

from pprint import pprint

if __name__ == '__main__':
    api = connect()

    query = 'covid vaccine'

    tweets = tweepy.Cursor(api.search_tweets, q=f'{query} -filter:retweets -filter:links',
                           tweet_mode='extended', lang='en').items(10)
    for tweet in tweets:
        content: str
        content = tweet.full_text
        print(repr(content))
