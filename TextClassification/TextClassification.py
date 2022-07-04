import re
import pandas as pd
from nltk import WordNetLemmatizer
from textblob import TextBlob
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.decomposition import PCA
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
        normalized_text = lem.lemmatize(normalized_text)
        normalized_tweet.append(normalized_text)
    return normalized_tweet
#mds
#pca
#tsl

def text_processing(tweet):
    return normalization(no_user_alpha(form_sentence(tweet)))


if __name__ == "__main__":
    art = pd.read_csv('../resources/data.csv', sep='\t')

    art = art[["label", "data"]]

    X = art["data"]
    Y = art["label"]

    msg_train, msg_test, label_train, label_test = train_test_split(art["data"],
                                                                    art["label"],
                                                                    test_size=0.2)

    vect = CountVectorizer(analyzer=text_processing)
    tfidf = TfidfTransformer()
    clas = SGDClassifier()

    pipeline = Pipeline([
        ('bow', vect),
        ('tfidf', tfidf),
        ("classifier", clas),
    ])
    pipeline.fit(msg_train, label_train)
    predictions = pipeline.predict(msg_test)
    print(classification_report(predictions, label_test))
    print("\n")
    print(confusion_matrix(predictions, label_test))
    print(accuracy_score(predictions, label_test))

    #wybranie słów najbardzej kluczowych 

    HOW_MANY = 10

    def f_importances(coef, names):
        imp = coef[0]
        x = sorted(zip(imp,names))
        imp,names = zip(*(x[:HOW_MANY] + x[-HOW_MANY:]))
        plt.barh(range(len(names)), imp, align='center')
        plt.yticks(range(len(names)), names)
        plt.show()
        return x[:HOW_MANY],x[-HOW_MANY:]

    slowa_anty, slowa_pro = f_importances(clas.coef_, vect.get_feature_names_out())

    print("pro")

    for coef, feat in slowa_pro[::-1]:
        print(coef, feat)

    print("-----------------------------------------")
    print("anty")

    for coef, feat in slowa_anty:
        print(coef, feat)

    #generowanie wykresu rozmieszczenia artykułów w przestrzeni 2D

    pp = Pipeline([('v',vect),('t',tfidf)])
    A = tfidf.transform(vect.transform(msg_train)).todense()

    data2D = PCA(n_components=2).fit_transform(A)

    for i,e in enumerate(data2D):
        plt.scatter(e[0], e[1], color='red' if label_train.array[i] == 0 else 'green')
    plt.show()

    #generowanie wykresu rozmieszczenia słów w przestrzeni 2D

    h = vect.transform(msg_train)

    indexes = list(map(lambda t: vect.get_feature_names_out().tolist().index(t[1]),slowa_pro+slowa_anty))
    ha = h.toarray()[:,indexes]

    pca = PCA(2)
    pca.fit(h.toarray())

    plt.scatter(pca.components_[0][indexes[:HOW_MANY]], pca.components_[1][indexes[:HOW_MANY]] ,color='green')
    plt.scatter(pca.components_[0][indexes[-HOW_MANY:]], pca.components_[1][indexes[-HOW_MANY:]],color='red')
    plt.show()
