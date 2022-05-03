import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from preprocessing.article import word_preprocess

if __name__ == "__main__":
    df_train = pd.read_csv("../resources/data.csv", sep="\t")

    words_per_article = df_train["data"].apply(word_preprocess)

    tfidf_vectorizer = TfidfVectorizer(tokenizer=word_preprocess)

    tfidf_wm = tfidf_vectorizer.fit_transform(df_train["data"])

    sgdc_classifier = SGDClassifier()

    sgdc_classifier.fit(tfidf_wm, df_train['label'])

    with open("../model_storage/words_pa.pkl", "wb") as file:
        pickle.dump(words_per_article, file)

    with open("../model_storage/vectorizer.pkl", "wb") as file:
        pickle.dump(tfidf_vectorizer, file)

    with open("../model_storage/bow.pkl", "wb") as file:
        pickle.dump(tfidf_wm, file)

    with open("../model_storage/classifier.pkl", "wb") as file:
        pickle.dump(sgdc_classifier, file)
