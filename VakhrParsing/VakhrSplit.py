#!/usr/bin/python3

import re
import pymorphy2

dict_file = open('dict.opcorpora.txt', encoding='utf-8')
IMPORT_OP_DICT = False

op_dict = {}
for i, line in enumerate(dict_file):
    if not IMPORT_OP_DICT:
        break
    print(i)
    title = False
    try:
        title = re.search(r'^[А-ЯЁ]+', line).group(0)
    except AttributeError:
        pass
    if title:
        op_dict[title] = 1

mistakes = {
    'ӓ': ['а'],
    'ӱ': ['у'],
    'й': ['и', 'й'],
    'ӧ': ['о'],
    'ё': ['е', 'ё'],
    'б': ['б', 'о'],
    'к': ['к', 'а']
}


def get_alternatives(s):
    stack = [s]
    length = len(s)
    i = 0

    while i < length:
        new_stack = []
        for st in stack:
            if st[i] in mistakes:
                for replacement in mistakes[st[i]]:
                    new_stack.append(''.join([x if j != i else replacement for j, x in enumerate(list(st))]))
        if new_stack:
            stack = new_stack
        i += 1
    return stack


alphabet_sequence = [x for x in 'аӓбвгдеёжзийклмнӈоӧөпрстуӱфхцчшщъыьэәӛюя']
regex_class = '[аӓбвгдеёжзийклмнӈоӧөпрстуӱфхцчшщъыьэәӛюя]'
mansi_seq = 'аӓбвгдеёжзийклмнӈоӧөпрстуӱфхцчшщъыьэәӛюя'
l_as = len(alphabet_sequence)


class isRussian:
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

    def check(self, x):
        x = re.sub(r'\/.*', '', x).strip('«»')
        print('# START')
        print(x)
        print('# END')
        for xx in (x, x.lower(), x.strip('-'), x.lower().strip('-')):
            str_parse = str(self.morph.parse(xx))
            if 'DictionaryAnalyzer' in str_parse and not 'Unknown' in str_parse:
                return True
            elif xx in op_dict:
                return True
        return False


bal_vakhr = open('balandin_vakhr.txt', encoding='utf-8').read().splitlines()

pre_buffer = ''
post_buffer = ''

class_cmcc = r'[А-ЯӒЁӇӦӰӘӚ]'
class_smcc = r'[а-яӓёӈӧӱәӛ]'
class_smcc_n_punct = r'[а-яӓёӈӧӱәӛ\,\-\s]'

len_bv = len(bal_vakhr)

skip = 0
is_russian = isRussian()
for number, line in enumerate(bal_vakhr):
    ws_split = re.split(r'\s+', line)
    if not len(ws_split):
        continue
    title = ws_split[0]
    
