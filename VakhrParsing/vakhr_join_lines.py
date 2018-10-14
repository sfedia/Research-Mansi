#!/usr/bin/python3

import re
import is_russian

bal_vakhr = open('balandin_vakhr_6.txt', encoding='utf-8').read().splitlines()
checker = is_russian.Checker(import_op=False)
len_bv = len(bal_vakhr)
new_bv = []

for e, line in enumerate(bal_vakhr):
    join = False
    if 0 < e < len_bv - 1:
        check_stack = [bal_vakhr[e - 1].split()[0], line.split()[0], bal_vakhr[e + 1].split()[0]]
        sorted_stack = check_stack[:]
        sorted_stack.sort()
        if check_stack != sorted_stack:
            join = True
    if e > 0:
        if re.search(r'\s*-\s*$', bal_vakhr[e - 1]):
            join = True
        elif re.search(r'^\s*\d+[\.,]', line):
            join = True
        elif re.search(r'\s*,\s*$', bal_vakhr[e - 1]):
            join = True
        elif re.search(r'\s*/\s*$', bal_vakhr[e - 1]):
            join = True

    if join:
        new_bv[-1] += ' ' + line
        new_bv[-1] = re.sub(r'\s{2,}', ' ', new_bv[-1])
    else:
        new_bv.append(line)

with open('balandin_vakhr_6x.txt', 'w', encoding='utf-8') as new_bv_file:
    new_bv_file.write("\n".join(new_bv))
    new_bv_file.close()