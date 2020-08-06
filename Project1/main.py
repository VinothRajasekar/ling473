import glob
from collections import defaultdict
from nltk.tree import ParentedTree
from nltk.tokenize import SExprTokenizer
from nltk.tgrep import tgrep_nodes
from typing import List, AnyStr, Any


def process_data(data: AnyStr) -> List[AnyStr]:
    """
    Process the syntactic constituents from the LDC file.
    Newline and tabs are stripped and joined and tokenized
    to form a Parented Tree.
    :param data: syntactic constituents from the LDC files
    :return: List of Parented Tree
    """
    clean_data = ''.join(map(lambda x: x.strip(), data))
    tokenizer = SExprTokenizer()
    tokens = tokenizer.tokenize(clean_data)
    processed_data = [ParentedTree.fromstring(value) for value in tokens]
    return processed_data


def calculate_count(tree_filtered: List) -> int:
    """
    Helper method to calculate count
    :param tree_filtered: output of tgrep_nodes
    :return: total count
    """
    total_count = sum(len(row) for row in tree_filtered)
    return total_count


def count_sentence(data: Any) -> int:
    """
    compute count for sentence
    :param data: Parented Tree
    :return: total count for sentence constituent
    """
    tree_filtered = list(tgrep_nodes('S', data))
    return calculate_count(tree_filtered)


def count_np(data: Any) -> int:
    """
    compute constituent count for noun phrase
    :param data: Parented Tree
    :return: total count for noun phrase constituent
    """
    tree_filtered = list(tgrep_nodes('NP', data))
    return calculate_count(tree_filtered)


def count_vp(data: Any) -> int:
    """
    compute constituent count for verb phrase
    :param data: Parented Tree
    :return: total count for verb phrase constituent
    """
    tree_filtered = list(tgrep_nodes('VP', data))
    return calculate_count(tree_filtered)


def ditransitive_count(data: Any) -> int:
    """
    compute constituent count for ditransitive verb phrase
    :param data: Parented Tree
    :return: total count for ditransitive verb phrase constituent
    """
    count = 0
    for tree in data:
        for subtree in tree.subtrees(lambda t: len(t) == 3):
            tree_filtered = list(tgrep_nodes("VP < (NP $ NP)", subtree))
            count += calculate_count(tree_filtered)
    return count


def intransitive_count(data: Any) -> int:
    """
     compute constituent count for intransitive_count verb phrase
    :param data: Parented Tree
    :return: total count for intransitive_count verb phrase constituent
    """
    count = 0
    for tree in data:
        for _ in tree.subtrees(lambda t: t.label() == "VP" and len(t) == 1):
            count += 1
    return count


def main() -> None:
    """
    Read LDC files and compute the constituent counts and produce final output.
    :return: prints out final constituent count for (S..), (NP..), (VP..), VP verb (NP ...) (NP ...) ) (VP verb )
    """
    print("Starting to Process data")
    results = defaultdict(list)
    results_count = {}
    filepath = "/corpora/LDC/LDC99T42/RAW/parsed/prd/wsj/14/*.prd"
    filenames = glob.glob(filepath)

    for file in filenames:
        with open(file) as f:
            parse_trees = f.readlines()
            parsed_data = process_data(parse_trees)
            results['S'].append(count_sentence(parsed_data))
            results['NP'].append(count_np(parsed_data))
            results['VP'].append(count_vp(parsed_data))
            results['DVP'].append(ditransitive_count(parsed_data))
            results['IVP'].append(intransitive_count(parsed_data))

    for key, value in results.items():
        results_count[key] = sum(value)
        print(f"The constituent count for {key} is {results_count[key]}")


if __name__ == "__main__":
    main()
    print("Completed Processing data successfully")
