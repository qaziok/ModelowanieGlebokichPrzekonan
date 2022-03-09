import tweepy as tw
import pandas as pd
from TwitterAnalisis import *


def connect():
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tw.API(auth)


if __name__ == '__main__':
    api = connect()


