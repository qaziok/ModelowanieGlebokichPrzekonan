import json
import pandas

if __name__ == "__main__":
    # open data.csv
    df = pandas.read_csv("resources/data.csv", sep="\t", encoding="utf-8")
    print(df.head())
    last = len(df)

    # open others.json
    with open("resources/others.json", "r", encoding="utf-8") as file:
        others = json.load(file)
        texts = [o["text"] for o in others]
        labels = [int(not o["isAntiVaccine"]) for o in others]
        ids = map(lambda x: x+1+last, range(len(others)))
        new = pandas.DataFrame({"id": ids, "label": labels, "data": texts})

    # merge data.csv and others.json
    df = pandas.concat([df, new], ignore_index=True, axis=0)

    # save merged.csv
    df.to_csv("resources/merged.csv", sep="\t", encoding="utf-8", index=False)
