#!/usr/bin/python3
from vakhr_split_lines import *
import re

test_results = [
    [6],  # 1
    [4, 8],  # 2
    [7],  # 3
    [],  # 4
    [4],  # 5
    [8],  # 6
    [5],  # 7
    [],  # 8
    [11, 15],  # 9
    [7],  # 10
    [],  # 11
    [5, 11],  # 12
    [6],  # 13
    [5],  # 14
    [],  # 15
    [4],  # 16
    [3],  # 17
    [5, 10, 14, 20, 24, 27],  # 18
    [3],  # 19
    [3, 11],  # 20
    [8, 13],  # 21
    [4, 8],  # 22
    [5],  # 23
    [3],  # 24
    [],  # 25
    [],  # 26
]
test_file = open('vakhr_split_lines_TESTS.txt', encoding='utf-8').read()
tests = []
i = -1
for line in test_file.splitlines():
    if not line or re.search(r'^\d+\)$', line):
        continue
    else:
        i += 1
    tests.append([line, test_results[i]])

correct = 0
wrong = []
for e, test in enumerate(tests):
    result = SplitString(test[0]).get_split_positions()
    print("{})".format(e + 1), test[1], '<==>', result, '(result)')
    if result == test[1]:
        correct += 1
    else:
        wrong.append(e)

print()
print('---')
print('{} out of {}'.format(correct, len(tests)))
print('wrong tests:', ', '.join(['N' + str(x + 1) for x in wrong]))
