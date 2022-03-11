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

    tweets = tweepy.Cursor(api.search_tweets, q=f'{query} -filter:retweets -filter:links exclude:replies',
                           tweet_mode='extended', lang='en', ).items(10)

    save = {
        'pro': set(),
        'anty': set()
    }

    with open('pro.txt', 'r') as pro:
        for line in pro:
            if line == '\n':
                continue
            save['pro'].add(line.rstrip())
    with open('anty.txt', 'r') as anty:
        for line in anty:
            if line == '\n':
                continue
            save['anty'].add(line.rstrip())

    for tweet in tweets:
        content: str
        content = tweet.full_text
        content = content.replace('\n', ' ')
        content = content.encode('ascii','ignore').decode()
        print(repr(content))
        choice = int('0' + input())
        # 1 - pro
        # 2 - anty
        # 3 - skip
        if choice == 1:
            save['pro'].add(content)
            print('Dodano do pro')
        elif choice == 2:
            save['anty'].add(content)
            print('Dodano do anty')

    print(save)

    with open('pro.txt', 'w') as pro:
        for x in save['pro']:
            print(x, file=pro)
    with open('anty.txt', 'w') as anty:
        for x in save['anty']:
            print(x, file=anty)
