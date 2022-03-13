import re


import pandas as pd
from nltk import WordNetLemmatizer
from textblob import TextBlob
from nltk.corpus import stopwords

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score


def form_sentence(tweet):
    tweet_blob = TextBlob(tweet)
    return " ".join(tweet_blob.words)


def no_user_alpha(tweet):
    tweet_list = [ele for ele in tweet.split() if ele != "user"]
    clean_tokens = [t for t in tweet_list if re.match(r"[^\W\d]*$", t)]
    clean_s = " ".join(clean_tokens)
    clean_mess = [word for word in clean_s.split() if word.lower() not in stopwords.words("english")]
    return clean_mess


def normalization(tweet_list):
    lem = WordNetLemmatizer()
    normalized_tweet = []
    for word in tweet_list:
        normalized_text = lem.lemmatize(word, "v")
        normalized_tweet.append(normalized_text)
    return normalized_tweet


def text_processing(tweet):
    return normalization(no_user_alpha(form_sentence(tweet)))


if __name__ == "__main__":
    tweets_df = pd.read_csv("../out/train.csv")
    tweets_df = tweets_df.apply(text_processing)

    pipeline = Pipeline([
        ('bow', CountVectorizer(analyzer=text_processing)),
        ('tfidf', TfidfTransformer()),
        ("classifier", MultinomialNB()),
    ])
