#!/usr/bin/python3

import re

bal_vakhr = open('balandin_vakhr.txt', encoding='utf-8').read().splitlines()

pre_buffer = ''
post_buffer = ''

class_cmcc = r'[А-ЯӒЁӇӦӰӘӚ]'
class_smcc = r'[а-яӓёӈӧӱәӛ]'
class_smcc_n_punct = r'[а-яӓёӈӧӱәӛ\,-\s]'

len_bv = len(bal_vakhr)


def regex_for_lines(line_number, regexp):
    regexp = re.sub(r'\\n(.*?)\\n', r'\n^\g<1>$\n', regexp)
    lines_regex = regexp.split(r'\n')
    for incr, content in bal_vakhr[line_number:]:
        if incr == len(regexp):
            break
        if (line_number + incr) == (len_bv - 1) and incr < (len(regexp) - 1):
            return False
        if not re.search(lines_regex[incr], content):
            return False


for line in bal_vakhr:
    print(line)