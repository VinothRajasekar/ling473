import glob
from typing import List, AnyStr
import re
from collections import Counter


def process_data(data: AnyStr) -> List[AnyStr]:
    """
    Process the AQUAINT corpus of English newswire
    to remove SGML tags, trim any occurrence(s) of the straight
    apostrophe from the beginning and end of the word
    and convert every word to lower-case
    and finally retain only words and straight apostrophe
    :param data: Ennglish text from docyment.
    :return: cleaned text from corpus
    """
    data = ''.join(data)
    # Remove SGML Tags
    filter_tags = re.sub('<.*?>', '', data)
    # Filter only words and apostrophe
    filter_words = re.sub('[^A-Za-z\']', ' ', filter_tags)
    # Remove begining apostrophe
    filter_front_apostrophe = re.sub(' \'*', ' ', filter_words)
    # apostrophe end apostrophe
    filter_back_apostrophe = re.sub('\'* ', ' ', filter_front_apostrophe)
    # convert word to lowercase
    cleaned_data = filter_back_apostrophe.lower()
    return cleaned_data


def main() -> None:
    """
    Read AQUAINT corpus of English newswire, process them  and produce final output.
    :return: sorted unigram language model to the console by counts in descending order.
    """
    filepath = "/corpora/LDC/LDC02T31/nyt/2000/*"
    filenames = glob.glob(filepath)
    total_count = Counter()

    for file in filenames:
        with open(file) as f:
            data = f.readlines()
            parsed_data = process_data(data)
            word_list = parsed_data.split()
            current_count = Counter(word_list)
            total_count += current_count
    sorted_val = sorted(total_count.items(), key=lambda x: -x[1])
    results = dict(sorted_val)

    for key, value in results.items():
        print(f"{key}\t{value}")


if __name__ == "__main__":
    main()
