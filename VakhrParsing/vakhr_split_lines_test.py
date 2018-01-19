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
    [7],  # 27
    [],  # 28
    [],  # 29
    [],  # 30
    [5, 9],  # 31
    [6],  # 32
    [4],  # 33
    [],  # 34
    [8],  # 35
    [6],  # 36
    [5],  # 37
    [6],  # 38
]
test_file = open('vakhr_split_lines_TESTS.txt', encoding='utf-8').read()
tests = []
i = -1
test_lines = []
digit_n_paren = False
for line in test_file.splitlines():
    if re.search(r'^\d+\)$', line):
        i += 1
        continue
    elif line:
        test_lines.append(line)
    elif not line:
        tests.append([test_lines, test_results[i]])
        test_lines = []
tests.append([test_lines, test_results[i]])

correct = 0
wrong = []
for e, test in enumerate(tests):
    result = SplitString(test[0][0], next_lines=[x for x in test[0][1:] if x != '']).get_split_positions()
    print("{})".format(e + 1), test[1], '<==>', result, '(result)')
    if result == test[1]:
        correct += 1
    else:
        wrong.append(e)

print()
print('---')
print('{} out of {}'.format(correct, len(tests)))
print('wrong tests:', ', '.join(['N' + str(x + 1) for x in wrong]))
