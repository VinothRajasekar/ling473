import glob
from collections import defaultdict
from typing import List, AnyStr, Any

V1 = u"\u0E40\u0E41\u0E42\u0E43\u0E44"
C1 = u"\u0E01\u0E02\u0E03\u0E04\u0E05\u0E06\u0E07\u0E08\u0E09\u0E0A\u0E0B\u0E0C\u0E0D\u0E0E\u0E0F" \
     + u"\u0E10\u0E11\u0E12\u0E13\u0E14\u0E15\u0E16\u0E17\u0E18\u0E19\u0E1A\u0E1B\u0E1C\u0E1D\u0E1E\u0E1F" \
     + u"\u0E20\u0E21\u0E22\u0E23\u0E24\u0E25\u0E26\u0E27\u0E28\u0E29\u0E2A\u0E2B\u0E2C\u0E2D\u0E2E"
C2 = u"\u0E23\u0E25\u0E27\u0E19\u0E21"
V2 = u"\u0E34\u0E35\u0E36\u0E37\u0E38\u0E39\u0E31\u0E47"
T = u"\u0E48\u0E49\u0E4A\u0E4B"
V3 = u"\u0E32\u0E2D\u0E22\u0E27"
C3 = u"\u0E07\u0E19\u0E21\u0E14\u0E1A\u0E01\u0E22\u0E27"


def add_text(state, char, processed_data):
    if state == 7 or state == 8:
        processed_data += u" " + char
        state = 1
    elif state == 8:
        processed_data += u" " + char
        state = 2
    elif state == 9:
        processed_data += char + u" "
        state = 0
    else:
        processed_data += char

    return processed_data, state


def process_data(data: AnyStr, fsm: dict) -> List[AnyStr]:
    """
    Process the syntactic constituents from the LDC file.
    Newline and tabs are stripped and joined and tokenized
    to form a Parented Tree.
    :param data: syntactic constituents from the LDC files
    :return: List of Parented Tree
    """
    state = 0
    processed_data = u""

    for char in data:
        if state in fsm:
            val = fsm.get(state)
            if char in C2 and state == 2:
                state = val.get("C2")
                processed_data, state = add_text(state, char, processed_data)
            elif char in V2 and (state == 2 or state == 3):
                state = val.get("V2")
                processed_data, state = add_text(state, char, processed_data)
            elif char in T and (state == 2 or state == 3 or state == 4):
                state = val.get("T")
                processed_data, state = add_text(state, char, processed_data)
            elif char in V3 and (state == 2 or state == 3 or state == 4 or state == 5):
                state = val.get("V3")
                processed_data, state = add_text(state, char, processed_data)
            elif char in C3 and (state == 2 or state == 3 or state == 4 or state == 5 or state == 6):
                state = val.get("C3")
                processed_data, state = add_text(state, char, processed_data)
            elif char in V1 and (state == 0 or state == 2 or state == 4 or state == 5 or state == 6):
                state = val.get("V1")
                processed_data, state = add_text(state, char, processed_data)
            elif char in C1 and (state == 0 or state == 1 or state == 4 or state == 5 or state == 6):
                state = val.get("C1")
                processed_data, state = add_text(state, char, processed_data)

    return processed_data


def main() -> None:
    """
    Read LDC files and compute the constituent counts and produce final output.
    :return: prints out final constituent count for (S..), (NP..), (VP..), VP verb (NP ...) (NP ...) ) (VP verb )
    """
    state_machine = {0: {"V1": 1, "C1": 2},
                     1: {"C1": 2},
                     2: {"C2": 3, "V2": 4, "T": 5, "V3": 6, "C3": 9, "V1": 7, "C1": 8},
                     3: {"V2": 4, "T": 5, "V3": 6, "C3": 9},
                     4: {"T": 5, "V3": 6, "C3": 9, "V1": 7, "C1": 8},
                     5: {"V3": 6, "C3": 9, "V1": 7, "C1": 8},
                     6: {"C3": 9, "V1": 7, "C1": 8},
                     7: {7: 7},
                     8: {8: 8},
                     9: {9: 9}
                     }

    results = u""
    filepath = "./fsm-input.utf8.txt"
    # filepath = "./test.txt"
    filenames = glob.glob(filepath)

    writefile = open("vinoth.html", "w+", encoding="utf-8")
    writefile.write("<html>\n<meta http-equiv='Content-Type' content='text/html; charset=UTF-8' />\n<body>\n")

    for file in filenames:
        with open(file, encoding="utf-8") as r:
            data = r.readlines()
            for line in data:
                results = process_data(line[:-1], state_machine)
                writefile.write(results + "<br/>\n")
            writefile.write("</body>\n</html>")


if __name__ == "__main__":
    main()
