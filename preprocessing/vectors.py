import pandas as pd
from collections import defaultdict


def prepare_dictionary(data, words, r=3):
    dictionary = {s: defaultdict(int) for _, s in words}
    for a in data:
        for i, w in enumerate(a):
                if w in dictionary.keys():
                    for n in range(max(i - r, 0), min(i + r, len(a))):
                        if a[n] not in dictionary.keys():
                            dictionary[w][a[n]] += 1
    return dictionary


def generate_vectors(dictionary, words) -> pd.DataFrame:
    data = {}
    for i, (k, d) in enumerate(dictionary.items()):
        for w in words:
            if d[w] > 1:
                if w not in data.keys():
                    data[w] = [0 for _ in words]
                data[w][i] = d[w]

    return pd.DataFrame(data, index=dictionary.keys())
