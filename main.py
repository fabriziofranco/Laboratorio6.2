import json
import operator

import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

nltk.download('stopwords')
nltk.download('punkt')
stemmer = SnowballStemmer('spanish')


def preprocessFile(file_name):
    file = open(file_name, 'r')
    file = file.read()
    dirty_tokens = nltk.word_tokenize(file)
    stop_list = stopwords.words("spanish")
    stop_list += ["(", ")", ";", ".", ",", ":"]
    tokens = []
    for token in dirty_tokens:
        if token not in stop_list:
            tokens.append(token)
    stemmed_tokens = []
    for token in tokens:
        stemmed_tokens.append(stemmer.stem(token))
    stemmed_tokens.sort()
    return stemmed_tokens


def preprocess_all_files():
    matrix_of_tokens = []
    counter = 1
    while counter <= 6:
        file_name = "docs/libro" + str(counter) + ".txt"
        matrix_of_tokens.append(preprocessFile(file_name))
        counter += 1
    return matrix_of_tokens


def build_inverted_index():
    library_tokens = preprocess_all_files()
    counters = nltk.defaultdict(int)
    for book_tokens in library_tokens:
        for token in book_tokens:
            counters[token] += 1

    counters = sorted(counters.items(), key=operator.itemgetter(1), reverse=True)
    counters = dict(counters[:500])

    index = nltk.defaultdict(list)
    i = 1

    for book_tokens in library_tokens:
        for token in book_tokens:
            if token in counters.keys() and i not in index[token]:
                index[token].append(i)
        i += 1

    index = dict(sorted(index.items(), key=operator.itemgetter(0)))
    index_file = open("index.json", "w")
    index_file.write(json.dumps(index))
    return index


build_inverted_index()
