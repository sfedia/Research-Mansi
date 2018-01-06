#!/usr/bin/python3

import re

bal_vakhr = open('balandin_vakhr.txt', encoding='utf-8').read().splitlines()

pre_buffer = ''
post_buffer = ''

class_cmcc = r'[А-ЯӒЁӇӦӰӘӚ]'
class_smcc = r'[а-яӓёӈӧӱәӛ]'
class_smcc_n_punct = r'[а-яӓёӈӧӱәӛ\,\-\s]'

len_bv = len(bal_vakhr)


def regex_for_lines(line_number, regexp):
    skip_regex = r'\\n(.*?)\\n'
    skip_count = len(re.findall(skip_regex, regexp))
    regexp = re.sub(skip_regex, r'\n^\g<1>$\n', regexp)
    lines_regex = regexp.split(r'\n')
    for incr, content in bal_vakhr[line_number:]:
        if incr == len(lines_regex):
            break
        if (line_number + incr) == (len_bv - 1) and incr < (len(lines_regex) - 1):
            return False
        if not re.search(lines_regex[incr], content):
            return False
    return skip_count


skip = 0
for number, line in enumerate(bal_vakhr):
    if skip:
        skip -= 1
        if skip > 0:
            continue
    ignore_cases = [
        r'\n[{0}\-\s]+\n[{0}\-\s]+\n\d+\n',
        r'\n\d+\n[{0}\-\s]+\n[{0}\-\s]+\n',
        r'\n[{0}\-\s]+\s+\d+\s+[{0}\-\s]+\n',
        r'\n\d+\n',
        r'\n[A-Z{CMCC}{SMCC}\-\s]\n'.format(CMCC=class_cmcc[1:-1], SMCC=class_smcc[1:-1])
    ]
    for case in ignore_cases:
        skip = regex_for_lines(number, case)
        if skip:
            break
    if skip:
        continue
