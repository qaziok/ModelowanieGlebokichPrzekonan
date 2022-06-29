import pickle
import json
from sklearn.metrics import classification_report


if __name__ == "__main__":
    with open("models_storage/data_csv_ms/vectorizer.pkl", "rb") as file:
        tfidf_vectorizer = pickle.load(file)

    with open("models_storage/data_csv_ms/classifier.pkl", "rb") as file:
        sgdc_classifier = pickle.load(file)

    # load others.json
    with open("resources/others.json","r",encoding="utf-8") as file:
        others = json.load(file)

    bow = tfidf_vectorizer.transform([o["text"] for o in others]).toarray()

    # print([int(not o["isAntiVaccine"]) for o in others])
    # print(sgdc_classifier.predict(bow))
    report = classification_report([int(not o["isAntiVaccine"]) for o in others], sgdc_classifier.predict(bow))
    print(report)


