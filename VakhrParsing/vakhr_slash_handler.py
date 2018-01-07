#!/usr/bin/python3

import re
import is_russian

bal_vakhr = open('balandin_vakhr.txt', encoding='utf-8').read().splitlines()
checker = is_russian.Checker(import_op=False)

with open('balandin_vakhr_new.txt', 'a', encoding='utf-8') as new_bv:
    for e, line in enumerate(bal_vakhr):
        line = re.sub(r'([^\s])/\s*([^\s])', '\g<1> /\g<2>', line)
        for found in re.finditer(r'([^\s]+)(\s+)/(\s+)([^\s]+)', line):
            a_token = found.group(1)
            f_ws_sequence = found.group(2)
            s_ws_sequence = found.group(3)
            b_token = found.group(4)

            if checker.check(a_token) and not checker.check(b_token):
                line = line.replace(
                    a_token + f_ws_sequence + "/" + s_ws_sequence + b_token,
                    a_token + " /" + b_token
                )
        new_bv.write(line + "\n")

new_bv.close()
