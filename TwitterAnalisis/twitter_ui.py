import PySimpleGUI as sg
import tweepy

from TwitterAnalisis import *


def connect():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


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
            if line == '/n':
                continue
            save['pro'].add(line.rstrip())
    with open('anty.txt', 'r') as anty:
        for line in anty:
            if line == '/n':
                continue
            save['anty'].add(line.rstrip())

    layout = [[sg.Text("click any button to start", key='-tweet-', size=(100, 7))],
              [sg.Button("pro", size=(10, 1)), sg.Button("anty", size=(10, 1)), sg.Button("skip", size=(10, 1))]]
    window = sg.Window("simple ui", layout)
    event, values = window.read()

    for tweet in tweets:
        content: str
        content = tweet.full_text
        content = content.replace('/n', ' ')
        content = content.encode('ascii', 'ignore').decode()

        window['-tweet-'].update(content)
        event, values = window.read()
        if event == "pro":
            save['pro'].add(content)
        elif event == "anty":
            save['anty'].add(content)
        elif event == "skip":
            continue
        elif event == sg.WIN_CLOSED:
            break

    window.close()
    print(save)

    with open('pro.txt', 'w') as pro:
        for x in save['pro']:
            print(x, file=pro)
    with open('anty.txt', 'w') as anty:
        for x in save['anty']:
            print(x, file=anty)
