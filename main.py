import json
import operator
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

nltk.download('stopwords')
nltk.download('punkt')
stemmer = SnowballStemmer('spanish')

index_generated = nltk.defaultdict(list)


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


def L(word):
    root = stemmer.stem(word)
    if root in index_generated:
        return index_generated[root]


def OR(*listas):
    or_result = []
    for books in listas:
        for book in books:
            if book not in or_result:
                or_result.append(book)
    return or_result


def AND(*listas):
    and_result = []
    counters = nltk.defaultdict(int)
    for books in listas:
        for book in books:
            counters[book] += 1
    for key, value in counters.items():
        if len(listas) == value:  # Esta en todas las listas
            and_result.append(key)
    return and_result


def ANDNOT(conjunto1, conjunto2):  # Resta de conjuntos
    and_not_result = []
    for book in conjunto1:
        if book not in conjunto2:
            and_not_result.append(book)
    return and_not_result


def main():
    global index_generated
    index_generated = build_inverted_index()
    print(ANDNOT(AND(L("Frodo"), L("Mordor")), L("anillo")))
    print(AND(L("anillo"), L("enano"), L("elfo")))
    print(OR(AND(L("hobbit"), L("Gandalf"), L("Gollum")), L("Saruman")))


if __name__ == '__main__':
    main()
