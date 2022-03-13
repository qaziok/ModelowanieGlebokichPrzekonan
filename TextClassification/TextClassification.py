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
    train_tweets = pd.read_csv("../out/train.csv")
    test_tweets = pd.read_csv("../out/test.csv")

    train_tweets = train_tweets[["label", "tweet"]]
    test_tweets = test_tweets[["tweet"]]

    train_tweets["tweet_list"] = train_tweets["tweet"].apply(text_processing)
    test_tweets["tweet_list"] = test_tweets["tweet"].apply(text_processing)

    X = train_tweets["tweet"]
    Y = train_tweets["label"]
    test = test_tweets["tweet"]

    msg_train, msg_test, label_train, label_test = train_test_split(train_tweets["tweet"],
                                                                    train_tweets["label"],
                                                                    test_size=0.2)

    pipeline = Pipeline([
        ('bow', CountVectorizer(analyzer=text_processing)),
        ('tfidf', TfidfTransformer()),
        ("classifier", MultinomialNB()),
    ])
    pipeline.fit(msg_train, label_train)
    predictions = pipeline.predict(msg_test)
    print(classification_report(predictions, label_test))
    print("\n")
    print(confusion_matrix(predictions, label_test))
    print(accuracy_score(predictions, label_test))
