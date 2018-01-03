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


def multiple_split(string, *keys):
    keymap = {}
    charmap = {}
    before = 1
    after = 2
    main_insertion = False
    repeated = 'before'  # or 'before' or 'after'
    main_index = 0
    for e, char in enumerate(string):
        if char in keys:
            if (not main_insertion and repeated != 'main') or repeated == 'before':  # that means 'before'
                position = [main_index, before, 0]
                while tuple(position) in keymap and char not in keymap[tuple(position)]:
                    print(keymap[tuple(position)])
                    position[-1] += 1
                position = tuple(position)
                if position not in keymap:
                    keymap[position] = ''
                keymap[position] += char
                repeated = 'before'
            elif main_insertion or repeated == 'after':
                main_insertion = False
                position = (main_index - 1, after, 0)
                while position in keymap and char not in keymap[position]:
                    position[-1] += 1
                if position not in keymap:
                    keymap[position] = ''
                keymap[position] += char
                repeated = 'after'
        else:
            charmap[main_index] = char
            main_index += 1
            main_insertion = True
            repeated = 'main'

    def char_in_keymap(index):
        keys = []
        for key in keymap:
            if key[0] == index:
                keys.append(key)
        return keys

    print(charmap)
    print(keymap)
    for char_index in charmap:
        if char_in_keymap(char_index):
            print('!!! {} !!!'.format(char_index))


multiple_split("foobarXXYlorYYYYYemQipsLLLLum", "X", "Y", "Q", "L")
#for page in pages:
    #space = multiple_split(page, "\n", " ")
    #print(page)
    #print(debug_split_object_list(space))
    #print()
