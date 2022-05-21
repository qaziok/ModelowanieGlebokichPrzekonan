import pandas as pd


def generate_vectors(dictionary) -> dict:
    data = {}
    for i, (k, d) in enumerate(dictionary.items()):
        for w, v in d.items():
            if v > 1:
                if w not in data.keys():
                    data[w] = [0 for _ in dictionary.keys()]
                data[w][i] = v

    return pd.DataFrame(data, index=dictionary.keys())
