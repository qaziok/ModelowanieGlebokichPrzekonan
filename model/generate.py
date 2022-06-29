import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from preprocessing.article import word_preprocess


if __name__ == "__main__":
    df = pd.read_csv("../resources/merged.csv", sep="\t", encoding="utf-8")

    train, test = train_test_split(df, test_size=0.2)

    words_per_article = df["data"].apply(word_preprocess)

    tfidf_vectorizer = TfidfVectorizer(tokenizer=word_preprocess)

    tfidf_wm = tfidf_vectorizer.fit_transform(train["data"])

    sgdc_classifier = SGDClassifier(verbose=True)

    sgdc_classifier.fit(tfidf_wm, train['label'])

    # cross validation
    predicted = sgdc_classifier.predict(tfidf_vectorizer.transform(test["data"]))

    print(classification_report(test['label'], predicted))

    # save model
    model = "merged_csv_ms"
    with open(f"../models_storage/{model}/words_pa.pkl", "wb") as file:
        pickle.dump(words_per_article, file)

    with open(f"../models_storage/{model}/vectorizer.pkl", "wb") as file:
        pickle.dump(tfidf_vectorizer, file)

    with open(f"../models_storage/{model}/bow.pkl", "wb") as file:
        pickle.dump(tfidf_wm, file)

    with open(f"../models_storage/{model}/classifier.pkl", "wb") as file:
        pickle.dump(sgdc_classifier, file)
