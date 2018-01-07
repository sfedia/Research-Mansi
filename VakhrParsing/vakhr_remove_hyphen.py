#!/usr/bin/python3

import re
import is_russian

bal_vakhr = open('balandin_vakhr_2.txt', encoding='utf-8').read().splitlines()
checker = is_russian.Checker(import_op=False)

with open('balandin_vakhr_3.txt', 'a', encoding='utf-8') as new_bv:
    for e, line in enumerate(bal_vakhr):
        tokens = line.split()
        new_line = []
        for token in tokens:
            check = checker.check(token)
            if '-' in token and check and check[0] in [3, 4]:
                new_line.append(token.replace('-', ''))
            else:
                new_line.append(token)
        print(e)

        new_bv.write(' '.join(new_line) + "\n")

new_bv.close()