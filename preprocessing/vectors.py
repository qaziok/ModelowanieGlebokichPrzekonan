from collections import defaultdict
from sklearn.feature_extraction.text import TfidfTransformer


def find_close_words(data: list[list[str]], key_words: list[str], r=2):
    """
    Znajdowanie bliskich słów dla słów kluczowych.

    :param data: lista danych z podziałem na słowa
    :param key_words: słowa kluczowe
    :param r: wielkość sąsiedztwa
    :return: lista wszystkich sąsiadów słów kluczowych
    """
    output = set()
    for a in data:
        for i, w in enumerate(a):
            if w in key_words:
                for n in range(max(i - r, 0), min(i + r, len(a))):
                    if a[n] not in key_words:
                        output.add(a[n])
    return list(output)


def prepare_dictionary(data: list[list[str]], key_words: list[str], r=2):
    """
    Zliczenie ilości wystąpień bliskich słów dla każdego słowa kluczowego.

    :param data: lista danych z podziałem na słowa
    :param key_words: słowa kluczowe
    :param r: wielkość sąsiedztwa
    :return: słownik zawierający ilość wystąpień bliskich słów dla każdego słowa kluczowego
    """
    dictionary = {s: defaultdict(int) for s in key_words}
    for a in data:
        for i, w in enumerate(a):
            if w in dictionary.keys():
                for n in range(max(i - r, 0), min(i + r, len(a))):
                    if a[n] not in dictionary.keys():
                        dictionary[w][a[n]] += 1
    return dictionary


def generate_vectors(dictionary: dict[defaultdict[int]], close_words: list[str]):
    """
    Generowanie wektorów wg. słownika.

    :param dictionary: słownik zawierający ilość wystąpień bliskich słów dla każdego słowa kluczowego
    :param close_words: lista wszystkich sąsiadów słów kluczowych
    :return: wektory słów kluczowych z ilością wystąpień bliskich słów
    """
    data = {}
    for i, (k, d) in enumerate(dictionary.items()):  # słowa kluczowe
        for w_i, w in enumerate(close_words):  # bliskie słowa
            if k not in data.keys():
                data[k] = [0 for _ in close_words]
            data[k][w_i] = d[w]

    return data


def tfidf_vectors(data, key_words, close_words, r=2):
    """
    Normalizacja wektorów wg. TF-IDF.

    :param data: wektory słów kluczowych z ilością wystąpień bliskich słów
    :param key_words: słowa kluczowe
    :param close_words: bliskie słowa
    :param r: wielkość sąsiedztwa
    :return: lista znormalizowanych wektorów
    """
    vectors = generate_vectors(prepare_dictionary(data,key_words,r=r),close_words)
    return TfidfTransformer().fit_transform(list(vectors.values())).toarray()
