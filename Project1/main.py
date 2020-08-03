import glob
from typing import List
from collections import defaultdict
from nltk.tree import ParentedTree
from nltk.tokenize import SExprTokenizer
from nltk.tgrep import tgrep_nodes


class Constituents(object):

    def __int__(self):
        pass

    def process_data(self, data) -> List:
        cleaned_data = ''.join(map(str.strip, data))
        tokenizer = SExprTokenizer()
        tokens = tokenizer.tokenize(cleaned_data)
        processed_data = [ParentedTree.fromstring(value) for value in tokens]
        return processed_data

    def calculate_count(self, tree_filtered) -> int:
        total_length = sum(len(row) for row in tree_filtered)
        return total_length

    def count_sentence(self, data) -> int:
        tree_filtered = list(tgrep_nodes('S', data))
        return self.calculate_count(tree_filtered)

    def count_np(self, data) -> int:
        tree_filtered = list(tgrep_nodes('NP', data))
        return self.calculate_count(tree_filtered)

    def count_vp(self, data) -> int:
        tree_filtered = list(tgrep_nodes('VP', data))
        return self.calculate_count(tree_filtered)

    def ditransitive_count(self, data) -> int:
        count = 0
        for tree in data:
            for subtree in tree.subtrees(lambda t: len(t) == 3):
                tree_filtered = list(tgrep_nodes("VP < (NP $ NP)", subtree))
                count += self.calculate_count(tree_filtered)
        return count

    def intransitive_count(self, data) -> int:

        count = 0
        for tree in data:
            for _ in tree.subtrees(lambda t: t.label() == "VP" and len(t) == 1):
                count += 1
        return count

    def main(self) -> None:
        print("Starting to Process data")
        results = defaultdict(list)
        filepath = "/Users/vinoth/PycharmProjects/ling473/test.prd"
        #filepath = "/corpora/LDC/LDC99T42/RAW/parsed/prd/wsj/14/*.prd"
        filenames = glob.glob(filepath)

        for file in filenames:
            with open(file) as f:
                parse_trees = f.readlines()
                parsed_data = self.process_data(parse_trees)
                results['S'].append(self.count_sentence(parsed_data))
                results['NP'].append(self.count_np(parsed_data))
                results['VP'].append(self.count_vp(parsed_data))
                results['DVP'].append(self.ditransitive_count(parsed_data))
                results['IVP'].append(self.intransitive_count(parsed_data))

        results_count = {}

        for key, value in results.items():
            results_count[key] = sum(value)
            print(f"The constituent count for {key} is {results_count[key]}")
        print("Completed Processing data successfully")


if __name__ == "__main__":
    process = Constituents()
    process.main()
