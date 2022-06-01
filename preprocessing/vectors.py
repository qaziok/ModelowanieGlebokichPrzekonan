from collections import defaultdict


def find_close_words(data: list[list[str]], key_words: list[str], r=2):
    output = set()
    for a in data:
        for i, w in enumerate(a):
            if w in key_words:
                for n in range(max(i - r, 0), min(i + r, len(a))):
                    if a[n] not in key_words:
                        output.add(a[n])
    return list(output)


def prepare_dictionary(data: list[list[str]], key_words: list[str], r=2):
    dictionary = {s: defaultdict(int) for s in key_words}
    for a in data:
        for i, w in enumerate(a):
            if w in dictionary.keys():
                for n in range(max(i - r, 0), min(i + r, len(a))):
                    if a[n] not in dictionary.keys():
                        dictionary[w][a[n]] += 1
    return dictionary


def generate_vectors(dictionary: dict[defaultdict[int]], close_words: list[str]):
    data = {}
    for i, (k, d) in enumerate(dictionary.items()):  # słowa kluczowe
        for w_i, w in enumerate(close_words):  # bliskie słowa
            if k not in data.keys():
                data[k] = [0 for _ in close_words]
            data[k][w_i] = d[w]

    return data
