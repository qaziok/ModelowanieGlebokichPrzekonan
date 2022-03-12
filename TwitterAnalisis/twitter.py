import tweepy
from TwitterAnalisis import *


def connect():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def get_tweets(api, query, limit, max_id=None):
    tweets = tweepy.Cursor(api.search_tweets,
                           q=f'{query} -filter:retweets -filter:links exclude:replies',
                           tweet_mode='extended', lang='en', max_id=max_id).items(limit)
    return list(tweets)


if __name__ == '__main__':
    api = connect()

    query = 'covid vaccine'

    tweets = get_tweets(api, query, 10)

    save = {
        'pro': set(),
        'anty': set()
    }

    with open('pro.txt', 'r', encoding='utf-8') as pro:
        for line in pro:
            if line == '\n':
                continue
            save['pro'].add(line.rstrip())
    with open('anty.txt', 'r', encoding='utf-8') as anty:
        for line in anty:
            if line == '\n':
                continue
            save['anty'].add(line.rstrip())

    choice = 0
    while choice != 9:
        tweet = tweets.pop(0)
        last_id = tweet.id
        if not tweets:
            tweets = get_tweets(api, query, 10, last_id)
            tweets.pop(0)
        content: str
        content = tweet.full_text
        content = content.replace('\n', ' ')
        content = content.encode('utf-8', 'ignore').decode()
        print(repr(content))
        try:
            choice = int('0' + input())
        except ValueError:
            choice = 0
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

    with open('pro.txt', 'w', encoding='utf-8') as pro:
        for x in save['pro']:
            print(x, file=pro)
    with open('anty.txt', 'w', encoding='utf-8') as anty:
        for x in save['anty']:
            print(x, file=anty)
