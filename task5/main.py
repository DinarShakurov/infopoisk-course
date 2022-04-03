import re
import os
import sys

from nltk import TreebankWordTokenizer, WordNetLemmatizer, pos_tag
from nltk.corpus import stopwords, wordnet
from os.path import join

sys.path.append('..')
from task3.bool_search import bool_search


def get_wordnet_pos(word):
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


def read_docs_tf_idf() -> dict:
    tf_idf_path = join('..', 'task4', 'lemmas_tf_idf')
    tmp = []
    for it in os.walk(tf_idf_path):
        tmp.append(it)
    tf_idf_files = tmp[0][2]
    result = dict()
    for tf_idf_file in tf_idf_files:
        with open(join('..', 'task4', 'lemmas_tf_idf', tf_idf_file), 'r') as file:
            all_lines = file.readlines()
        all_lines = [line for line in all_lines if not line == '']
        curr = result.setdefault(tf_idf_file.split('.')[0].split('_')[-1], dict())
        for line in all_lines:
            line_splitted = line.split(' ')
            lemma = line_splitted[0]
            lemma_idf = float(line_splitted[1])
            lemma_tf_idf = float(line_splitted[2])
            curr.setdefault(lemma, (lemma_idf, lemma_tf_idf))
    return result


def lemmatize_query(query: str) -> list:
    tokens = TreebankWordTokenizer().tokenize(query)
    eng_stopwords = stopwords.words('english')
    tokens = list(map(str.lower, tokens))
    eng_letters = re.compile("^[a-z]+$")
    tokens = [word for word in tokens if eng_letters.match(word)]

    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(tkn, get_wordnet_pos(tkn)) for tkn in tokens]
    lemmas = [lemma for lemma in lemmas if lemma not in eng_stopwords]
    return lemmas


def cos_sim(a: list, b: list):
    numerator = 0
    a_den = 0
    b_den = 0
    if not len(a) == len(b):
        raise Exception
    for i in range(0, len(a)):
        numerator += a[i] * b[i]
        a_den += a[i] * a[i]
        b_den += b[i] * b[i]
    return numerator / (a_den * b_den)


def vector_search(query: str) -> list:
    query_lemmas = lemmatize_query(query)
    td_idf = read_docs_tf_idf()

    unique_lemmas = set(query_lemmas)
    founded_docs = bool_search(" | ".join(query_lemmas))
    lemmas_idf: dict = dict()
    if not founded_docs:
        return []
    for doc in founded_docs:
        unique_lemmas.update(set(td_idf.get(doc).keys()))

    docs_vector = []
    for doc in founded_docs:
        html_lemma_info: dict = td_idf.get(doc)
        html_lemmas: set = set(html_lemma_info.keys())
        vector = []
        for lemma in unique_lemmas:
            if lemma in html_lemmas:
                lemma_idf, lemma_tf_idf = html_lemma_info.get(lemma)
                vector.append(lemma_tf_idf)
                lemmas_idf.setdefault(lemma, lemma_idf)
            else:
                vector.append(0.0)
        docs_vector.append([doc, vector])

    query_vector = []
    for lemma in unique_lemmas:
        if lemma in query_lemmas:
            lemma_idf = lemmas_idf.get(lemma)
            lemma_tf = query_lemmas.count(lemma) / len(query_lemmas)
            lemma_tf_idf = lemma_tf * lemma_idf
            query_vector.append(lemma_tf_idf)
        else:
            query_vector.append(0.0)

    for doc_vector in docs_vector:
        doc_vector.append(cos_sim(doc_vector[1], query_vector))

    docs_vector = sorted(docs_vector, key=lambda d: d[2], reverse=True)

    return [[d[0], d[2]] for d in docs_vector]  # ['document', Cosine similarity]


if __name__ == '__main__':
    print(vector_search('Online'))
