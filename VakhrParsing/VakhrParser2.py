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


bal_vakhr = open('balandin_vakhr.txt', encoding='utf-8').read()

alphabet_sequence = [x for x in 'аӓбвгдеёжзийклмнӈоӧөпрстуӱфхцчшщъыьэәӛюя']
regex_class = '[аӓбвгдеёжзийклмнӈоӧөпрстуӱфхцчшщъыьэәӛюя]'
mansi_seq = 'аӓбвгдеёжзийклмнӈоӧөпрстуӱфхцчшщъыьэәӛюя'
l_as = len(alphabet_sequence)


class isRussian:
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

    def check(self, x):
        x = re.sub(r'\/.*', '', x).strip('«»')
        for xx in (x, x.lower(), x.strip('-'), x.lower().strip('-')):
            str_parse = str(self.morph.parse(xx))
            if 'DictionaryAnalyzer' in str_parse and not 'Unknown' in str_parse:
                return True
            elif xx in op_dict:
                return True
        return False


class SplitObject:
    def __init__(self, content, before=None, after=None):
        self.content = content
        self.before = before
        self.after = after

    def inner(self):
        return self.content

    def add_to_before(self, add):
        self.before += add

    def add_to_after(self, add):
        self.after += add

    def what_before(self):
        return self.before

    def what_after(self):
        return self.after

    def clear_before(self):
        self.before = None

    def clear_after(self):
        self.after = None


def debug_split_object_list(objs):
    for obj in objs:
        print('---')
        print('Before: {}'.format(obj.what_before() if obj.what_before is not None else "NONE"))
        print('Content: {}'.format(obj.inner()))
        print('After: {}'.format(obj.what_after() if obj.what_after is not None else "NONE"))
        print('---')


class LineSplit:
    def __init__(self, line):
        self.line = line


page_pattern = r'\n[{0}\-\s]+\n[{0}\-\s]+\n\d+\n|\n\d+\n[{0}\-\s]+\n[{0}\-\s]+\n|'
page_pattern += r'\n[{0}\-\s]+\s+\d+\s+[{0}\-\s]+\n|\n\d+\n|\n[A-ZА-ЯЁа-яё]\n'
page_pattern = page_pattern.format(mansi_seq)
print(page_pattern)
pages = [page.group(0) for page in re.finditer(page_pattern, bal_vakhr) if not re.search(r"[',\(\)\/]", page.group(0))]
for page in pages:
    bal_vakhr = bal_vakhr.replace(page, '')

pre_buffer = ''
post_buffer = ''
bal_vakhr_lines = bal_vakhr.splitlines()
len_vl = len(bal_vakhr_lines)

def skip

for e, line in enumerate(bal_vakhr_lines):


