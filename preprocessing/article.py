from nltk import RegexpTokenizer, WordNetLemmatizer
from nltk.corpus import stopwords
import re


def word_preprocess(sentence: str) -> list:
    """
        Generuje listę kluczowych słów z podanego tekstu.
    """
    wordnet_lemmatizer = WordNetLemmatizer()
    sentence = str(sentence)
    sentence = sentence.lower()
    sentence = sentence.replace('{html}', "")
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', sentence)
    rem_url = re.sub(r'http\S+', '', cleantext)
    rem_num = re.sub('\d+', '', rem_url)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(rem_num)
    filtered_words = [w for w in tokens if len(w) > 2 if not w in stopwords.words('english')]
    lemma_words = [wordnet_lemmatizer.lemmatize(w) for w in filtered_words]
    return lemma_words


def pair_preprocess(sentence: str) -> list:
    """
        Generuje listę par słów sąsiadujących ze sobą z podanego tekstu.
    """
    words = word_preprocess(sentence)
    return [f'{words[i]} {words[i + 1]}' for i in range(len(words) - 1)]
