import os
import re
import string
from pathlib import Path
from bs4 import BeautifulSoup as BSHTML
from bs4.element import Comment
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet


nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')

def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


def cleanhtml(raw_html) -> str:
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', raw_html)
    return cleantext


def remove_reduction(text) -> str:
    return text.replace("'re", " are")\
        .replace("'m", " am")\
        .replace("'d", " would")\
        .replace("'ve", " have")\
        .replace("'ll", " will")\
        .replace("can't", "can not")\
        .replace("n't", " not")\
        .replace("'s", " is")


def tokenize(raw_text) -> set:
    soup = BSHTML(raw_text, features="html.parser")
    for s in soup(['figure', 'script', 'style', 'link', 'meta', 'noscript']):
        s.decompose()
    for comments in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comments.extract()
    only_text = " ".join(cleanhtml(str(soup.find())).split()).replace('&amp;', '&')
    only_text = remove_reduction(only_text)
    current_tokens = nltk.word_tokenize(only_text)

    eng_stopwords = stopwords.words('english')
    current_tokens = [a for a in current_tokens if a.lower() not in eng_stopwords]
    current_tokens = [a for a in current_tokens if a.lower() not in string.punctuation]
    current_tokens = [a for a in current_tokens if not a.isnumeric()]
    eng_letters = re.compile("^[a-zA-Z]+$")
    current_tokens = [a for a in current_tokens if eng_letters.match(a)]
    return set(map(lambda x: x.lower(), current_tokens))


def lemmatization(tokens) -> dict:
    lemm_dict = {}
    lemmaizer = WordNetLemmatizer()
    lemms = []
    for token in tokens:
        current_lemm = lemmaizer.lemmatize(token, get_wordnet_pos(token))
        lemms.append(current_lemm)
        lemm_dict.setdefault(current_lemm, []).append(token)
    return lemm_dict


if __name__ == '__main__':
    list = []
    for it in os.walk("../downloaded_html/"):
        list.extend(it)
    list = list[2]
    token_dir_path = os.path.join('.', 'tokens')
    lemmas_dir_path = os.path.join('.', 'lemmas')
    Path(token_dir_path).mkdir(exist_ok=True)
    Path(lemmas_dir_path).mkdir(exist_ok=True)
    for filepath in list:
        filename = filepath.split('.')[0]
        token_filename = os.path.join(token_dir_path, f'tokens_{filename}.txt')
        lemma_filename = os.path.join(lemmas_dir_path, f'lemmas_{filename}.txt')
        Path(token_filename).touch(exist_ok=True)
        Path(lemma_filename).touch(exist_ok=True)
        with open("../downloaded_html/" + filepath, 'r', encoding="utf-8") as file:
            tokens = tokenize(file.read())

        with open(token_filename, 'w') as token_file:
            token_file.write('\n'.join(tokens))

        lem_dict = lemmatization(tokens)
        with open(lemma_filename, 'w') as lemma_file:
            for key, value in lem_dict.items():
                lemma_file.write(f'{key} {" ".join(value)}\n')

    print('Finished')
