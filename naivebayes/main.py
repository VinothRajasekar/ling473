import glob
from collections import defaultdict
import string
import math
import sys

lang_list = ['dan', 'deu', 'dut', 'eng', 'fin', 'fra', 'gla', 'ita', 'nob', 'pol', 'por', 'spa', 'swe', 'swh',
             'tgl']
word_lang = defaultdict(dict)
lang_word = defaultdict(dict)


def process_data(data, lang):
    word_count = data.strip("\n").split("\t")
    if word_count[0] not in word_lang:
        word_lang[word_count[0]] = {'dan': 0, 'deu': 0, 'dut': 0, 'eng': 0, 'fin': 0, 'fra': 0, 'gla': 0, 'ita': 0,
                                    'nob': 0, 'pol': 0, 'por': 0, 'spa': 0, 'swe': 0, 'swh': 0, 'tgl': 0}
    word_lang[word_count[0]][lang] = int(word_count[1])


def build_probability(data):
    prob = {}
    for lang in lang_list:
        calc = float(0)
        for word in data:
            if word in word_lang and word_lang[word][lang] > 0:
                calc += math.log10(word_lang[word][lang] / word_lang[word]['total'])
            else:
                calc += math.log10(1 / lang_word[lang]['total'])
        prob[lang] = calc
    return prob


def word_laplace_smoothing():
    for word in word_lang:
        for lang in word_lang[word]:
            word_lang[word][lang] += 1


def lang_laplace_smoothing():
    for lang in lang_word:
        for word in lang_word[lang]:
            lang_word[lang][word] += 1


def predict(res, extra_credit):
    max_value = -1 * float('inf')
    max_lang = "unk"
    total_val = 0
    for k, v in res.items():
        if res[k] > max_value:
            max_value = res[k]
            max_lang = k
        print(f'{k} \t {res[k]}')
        total_val += res[k]

    if extra_credit == "1" and max_value < -100:
        print(f'result \t unk {max_value}')
    else:
        print(f'result \t {max_lang} {max_value}')


def main(file_path, dataset_path, extra_credit) -> None:
    """
    Read language model files and build a naive bayes classifier.
    :return: return predictions for each language in the test dataset
    """

    filepath = file_path + "/*"
    filenames = glob.glob(filepath)

    for file in filenames:
        with open(file, encoding="latin-1") as r:
            data = r.readlines()
            for line in data:
                lang = file.split('/')[-1][:3]
                process_data(line, lang)

    for k, v in word_lang.items():
        for k1, v1 in v.items():
            lang_word[k1][k] = v1

    lang_laplace_smoothing()

    for word, val in lang_word.items():
        total = sum(val.values())
        lang_word[word]['total'] = total

    word_laplace_smoothing()

    for word, val in word_lang.items():
        total = sum(val.values())
        word_lang[word]['total'] = total

    with open(dataset_path, encoding="latin-1") as r:
        for data in r:
            print(data.strip("\n"))
            data = data.strip("\n").split("\t")
            translator = str.maketrans('', '', string.punctuation)
            data = data[1].translate(translator).split(' ')
            res = build_probability(data)
            predict(res, extra_credit)


if __name__ == "__main__":
    file_path = sys.argv[1]
    dataset_path = sys.argv[2]
    extra_credit = sys.argv[3]
    main(file_path, dataset_path, extra_credit)
