import numpy as np
import glob
from typing import List
from collections import defaultdict
import logging


def flatten_tree(parse_tree) -> List:
    cleaned_data = parse_tree.split()
    return cleaned_data


def count_sentence(data) -> int:
    print(data)
    sentence = '(S'
    sentence_count = data.count(sentence)
    print(sentence_count)
    return sentence_count


def count_np(data) -> int:
    noun_phrase = '(NP'
    np_count = data.count(noun_phrase)
    print(np_count)
    return np_count


def count_vp(data) -> int:
    verb_phrase = '(VP'
    vp_count = data.count(verb_phrase)
    print(vp_count)
    return vp_count


def ditransitive_count(data) -> int:
    count = 0
    for i, word in enumerate(data):
        try:
            if word == '(VP' and data[i + 2] == '(NP' and data[i + 3] == '(NP' and data[i + 4] != '(':
                count += 1
        except IndexError as e:
            logging.exception("Index Error", e)

    return count


def intransitive_count(data) -> int:
    data_len = len(data) - 1
    count = 0
    for i, word in enumerate(data):
        if i + 2 < data_len and i + 3 < data_len:
            try:
                if word == '(VP' and (data[i + 2] == '(S' or data[i + 2] == '(.'):
                    count += 1
            except IndexError as e:
                logging.exception("Index Error", e)

    return count


def main() -> None:
    print("project 1 work")
    results = defaultdict(list)
    print(results)
    filepath = "/Users/vinoth/PycharmProjects/ling473/*.prd"
    filenames = glob.glob(filepath)

    for file in filenames:
        with open(file) as f:
            parse_tree = f.read()
            data = flatten_tree(parse_tree)
            results['S'].append(count_sentence(data))
            results['NP'].append(count_np(data))
            results['VP'].append(count_vp(data))
            results['DVP'].append(ditransitive_count(data))
            results['IVP'].append(intransitive_count(data))

    print(results)
    results_count = {}
    for key, value in results.items():
        results_count[key] = sum(value)
    print(results_count)


if __name__ == main():
    main()
