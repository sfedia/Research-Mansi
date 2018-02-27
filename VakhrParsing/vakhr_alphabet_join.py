#!/usr/bin/python3
import re
import string


def extract_title(whole):
    for token in [x.strip(string.punctuation) for x in whole.split()]:
        if re.search(r'[а-яё]', token):
            return token


symbols = [x for x in 'аӓбвгдеёжзийклмнӈоӧөпрстуӱфхцчшщъьыэәӛюя']

bal_vakhr = open('balandin_vakhr_5.txt', encoding='utf-8').read().splitlines()
len_bv = len(bal_vakhr)
new_bv = []

for e, line in enumerate(bal_vakhr):
    test_set = []
    if e == 0:
        new_bv.append(line)
        continue
    elif e == len_bv - 1:
        test_set = [extract_title(bal_vakhr[e - 2]), extract_title(bal_vakhr[e - 1]), extract_title(line)]
    else:
        test_set = [extract_title(bal_vakhr[e - 1]), extract_title(line), extract_title(bal_vakhr[e + 1])]

    sorted_set = sorted(test_set, key=lambda word: [symbols.index(x) if x in symbols else -1 for x in word])
    print(test_set, sorted_set)
    if test_set != sorted_set:
        new_bv[-1] += ' ' + line
        new_bv[-1] = re.sub(r'\s{2,}', ' ', new_bv[-1])
    else:
        new_bv.append(line)

with open('balandin_vakhr_5x.txt', 'w', encoding='utf-8') as new_bv_file:
    new_bv_file.write("\n".join(new_bv))
    new_bv_file.close()
