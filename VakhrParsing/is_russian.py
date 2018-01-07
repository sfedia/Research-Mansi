#!/usr/bin/python3

import re
import pymorphy2


class Checker:
    def __init__(self, import_op=True):
        self.morph = pymorphy2.MorphAnalyzer()
        self.dict_file = open('dict.opcorpora.txt', encoding='utf-8')
        self.op_dict = {}
        for i, line in enumerate(self.dict_file):
            if not import_op:
                break
            print(i)
            title = False
            try:
                title = re.search(r'^[А-ЯЁ]+', line).group(0)
            except AttributeError:
                pass
            if title:
                self.op_dict[title] = 1

    mistakes = {
        'ӓ': ['а'],
        'ӱ': ['у'],
        'й': ['и', 'й'],
        'ӧ': ['о'],
        'ё': ['е', 'ё'],
        'б': ['б', 'о'],
        'к': ['к', 'а'],
        '1': ['и', '1'],
        '6': ['о', 'б', '6']
    }

    def get_alternatives(self, s):
        stack = [s]
        length = len(s)
        i = 0
        while i < length:
            new_stack = []
            for st in stack:
                if st[i] in self.mistakes:
                    for replacement in self.mistakes[st[i]]:
                        new_stack.append(''.join([x if j != i else replacement for j, x in enumerate(list(st))]))
            if new_stack:
                stack = new_stack
            i += 1
        return stack

    def check(self, token):
        token = re.sub(r'\/.*', '', token).strip('«»')
        for x in self.get_alternatives(token):
            for xx in (x, x.lower(), x.strip('-'), x.lower().strip('-')):
                str_parse = str(self.morph.parse(xx))
                if 'DictionaryAnalyzer' in str_parse and not 'Unknown' in str_parse:
                    return True
                elif xx in self.op_dict:
                    return True
        return False
