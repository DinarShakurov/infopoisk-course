import os
from os.path import join

if __name__ == '__main__':
    lemmas_dir_path = join('..', 'lemmas')
    lemmas = []
    for it in os.walk(lemmas_dir_path):
        lemmas.append(it)
    lemmas = lemmas[0][2]
    index = {}
    file_and_lemma = {}
    for lemma_file in lemmas:
        filenumber = int(lemma_file.split('.')[0].split('_')[1])

        with open(join(lemmas_dir_path, lemma_file)) as curr_lemma_file:
            text = curr_lemma_file.read().split(sep='\n')
            text.remove('')
            curr_lemmas = list(map(lambda words: words.split()[0], text))
            file_and_lemma.setdefault(filenumber, set()).update(curr_lemmas)
            text = list(map(lambda words: [words.split()[0], []], text))
            index.update(text)

    for lemma, lemma_list in index.items():
        for key, value in file_and_lemma.items():
            if lemma in value:
                lemma_list.append(key)
        lemma_list.sort()

    with open('index.txt', 'w') as index_file:
        result = ''
        for lemma, lemma_list in index.items():
            result = f'{result}{lemma} {" ".join([str(x) for x in lemma_list])}\n'
        index_file.write(result)
