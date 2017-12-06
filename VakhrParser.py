#!/usr/bin/python3
import re
import pymorphy2

bal_vakhr = open('balandin_vakhr.txt', encoding='utf-8')

alphabet_sequence = [x for x in 'аӓбвгдеёжзийклмнӈоӧөпрстуӱфхцчшщъыьэәӛюя']
l_as = len(alphabet_sequence)


class isRussian:
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

    def check(self, x):
        str_parse = str(self.morph.parse(x))
        return 'DictionaryAnalyzer' in str_parse and not 'Unknown' in str_parse


is_russian = isRussian()

for i, line in enumerate(bal_vakhr):
    if len(line) == 1:
        try:
            void = int(line)
        except ValueError:
            if line.istitle():
                continue

    line_sp = line.split()
    title = line_sp[0]
    line_sp_det = []
    for lsp in line_sp:
        line_sp_det.append([lsp, 'russian' if is_russian.check(lsp) else 'mansi'])

    len_line_sp_det = len(line_sp_det)
    margins = []
    for j, token in enumerate(line_sp_det):
        if j == len_line_sp_det:
            break
        if not is_russian.check(token) and is_russian.check(line_sp_det[j + 1]):
            margins.append([j, j + 1])
    margins_confirmed = []
    for marg in margins:
        start_i = marg[0]
        back_i = start_i - 1
        rus_i = marg[1]
        if start_i == 2:
            continue
        while back_i > 0 and line_sp_det[back_i][0] == 'mansi':
            triple_list = [line_sp[back_i + 1], line_sp[back_i], line_sp[0]]
            triple_list.sort()
            st_i_new = triple_list.index(line_sp[back_i + 1])
            if triple_list.index(title) > 0:
                break
            al_i = alphabet_sequence.index(title[0])
            next_sym = alphabet_sequence[al_i + 1] if al_i < l_as - 1 else None
            if st_i_new == 1 and (line_sp[back_i + 1][0] == title[0] or (next_sym is not None and line_sp[back_i + 1][0] == next_sym)):
                margins_confirmed.append([back_i + 1, marg[1]])
                break
            back_i -= 1

