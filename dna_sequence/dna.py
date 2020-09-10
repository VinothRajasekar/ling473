import glob
from collections import defaultdict
from multiprocessing import Pool


class TrieNode:
    """
       Initialize and build a Trie Node
    """

    def __init__(self, text, is_word):
        self.text = text
        self.children = [None] * 4
        self.is_word = is_word

    def insert(self, word):
        if word.text == 'A':
            self.children[0] = word
        elif word.text == 'T':
            self.children[1] = word
        elif word.text == 'C':
            self.children[2] = word
        elif word.text == 'G':
            self.children[3] = word


class Trie:
    """
       Build a Prefix Tree from target sequences
    """

    def __init__(self):
        self.head = TrieNode("*", False)

    def add_char(self, word):
        current = self.head
        for char in word:
            if char == 'A':
                if current.children[0] is None:
                    current.insert(TrieNode(char, False))
                current = current.children[0]
            elif char == 'T':
                if current.children[1] is None:
                    current.insert(TrieNode(char, False))
                current = current.children[1]
            elif char == 'C':
                if current.children[2] is None:
                    current.insert(TrieNode(char, False))
                current = current.children[2]
            elif char == 'G':
                if current.children[3] is None:
                    current.insert(TrieNode(char, False))
                current = current.children[3]
        current.is_word = True

    def head_node(self):
        return self.head


def find_matches(arr):
    """
       Search and match DNA sequences.
    """

    trie = arr[0]
    file_name = arr[1]
    i = 0
    with open(file_name) as f:
        process_data = f.read().upper()
        process_data_len = len(process_data)
    output = {}
    while i < process_data_len:
        j = i
        current = trie.head_node()
        while j < process_data_len:
            node_char = process_data[j]
            if node_char == 'A' and current.children[0] is not None:
                current = current.children[0]
            elif node_char == 'T' and current.children[1] is not None:
                current = current.children[1]
            elif node_char == 'C' and current.children[2] is not None:
                current = current.children[2]
            elif node_char == 'G' and current.children[3] is not None:
                current = current.children[3]
            elif current.is_word:
                sequence = process_data[i:j]
                hex_offset = hex(i).lstrip('0x').upper().zfill(8)
                output[hex_offset] = sequence
                break
            else:
                break
            j += 1
        i += 1
    return file_name, output


def main() -> None:
    """
    Read DNA and targets sequences corpus, build a trie node with targets and find matches.
    :return: all matches found in the Human Genome Corpus, displaying output to console.
    """

    filepath = "/opt/dropbox/19-20/473/project4/targets"
    filepath_corpus = "/opt/dropbox/19-20/473/project4/hg19-GRCh37/*"
    filenames = glob.glob(filepath)
    corpus_filenames = glob.glob(filepath_corpus)
    extra_credit = defaultdict(list)
    trie = Trie()
    for file in filenames:
        with open(file) as f:
            for line in f:
                trie.add_char(line.strip().upper())

    arr = []

    for corpus_file in corpus_filenames:
        arr.append(tuple((trie, corpus_file)))

    with Pool(30) as p:
        results = p.map(find_matches, arr)

    for file_name, sequences in results:
        print(file_name)
        for k, v in sequences.items():
            print("\t" + k + "\t" + v)
            extra_credit[v].append(tuple((k, file_name)))

    with open('extra-credit', 'w') as w:
        for key, val in extra_credit.items():
            w.write(key + '\n')
            for offset_name, file_num in val:
                w.write("\t" + offset_name + "\t" + str(file_num).split("/")[-1] + "\n")


if __name__ == "__main__":
    main()
