#!/usr/bin/python3

import re
import is_russian
import string

bal_vakhr = open('balandin_vakhr_4.txt', encoding='utf-8').read().splitlines()
checker = is_russian.Checker(import_op=False)
len_bv = len(bal_vakhr)
new_bv = []


class SplitString:
    def __init__(self, str2split, simplify=True):
        self.str2split = str2split
        self.str2split = re.sub(r',(?!\s)', ', ', self.str2split)
        self.symbols = [x for x in 'аӓбвгдеёжзийклмнӈоӧөпрстуӱфхцчшщъыьэәӛюя']
        self.simplify = {
            'ӓ': 'а',
            'ӧ': 'о',
            'ӱ': 'у',
            'ӛ': 'ә'
        }
        self.sorted = self.sort_mansi(self.str2split, simplify)
        self.str_splitted = self.str2split.split()

    @staticmethod
    def regex_ranges(regex, search_string):
        new_token_inds = []
        new_token = True
        for i, sym in enumerate(search_string):
            if new_token:
                new_token_inds.append(i)
                new_token = False
            elif sym == ' ':
                new_token = True
        sym_ranges = [[x.start(), x.end()] for x in re.finditer(regex, search_string)]
        token_ranges = []
        for sr_start, sr_end in sym_ranges:
            start_token = min(new_token_inds, key=lambda x: abs(x - sr_start) * (8192 if x > sr_start else 1))
            end_token = min(new_token_inds, key=lambda x: abs(x - sr_start) * (8192 if x < sr_start else 1))
            token_ranges.append([start_token, end_token])
        return token_ranges

    @staticmethod
    def in_regex_ranges(position, ranges):
        for start, end in ranges:
            if end >= position >= start:
                return True
        return False

    def check_in_af_range(self, position):
        str_splitted_ed = self.str2split
        str_splitted_ed = re.sub(r'\d+\.\s*', '', str_splitted_ed)
        str_splitted_ed = str_splitted_ed.split()
        if re.search(r'[’°]', str_splitted_ed[position]):
            return True
        if re.search(r'^\s*/', str_splitted_ed[position]):
            return True
        i = position
        slash_pos = 0
        while i > 0:
            if re.search(r'^\s*/', str_splitted_ed[i]):
                slash_pos = i
                break
            i -= 1
        if not slash_pos:
            return False
        group_numbers = [0]
        commas_number = 0
        wrong_const = 3
        for i in range(position - 1, slash_pos - 1, -1):
            if i == wrong_const:
                return False
            if not re.search(r',\s*$', str_splitted_ed[position]):
                group_numbers[-1] += 1
            else:
                commas_number += 1
                group_numbers.append(0)

        return len(group_numbers) != len(set(group_numbers)) and len(group_numbers) == (commas_number - 1)

    def sort_mansi(self, s, simplify=True):
        unsorted_unstripped = s.split()
        unsorted_stripped = [x.strip(string.punctuation) for x in s.split()]
        sorted_stripped = []
        corresp = {}
        corresp_indices = {}
        corresp_use = {}
        for us_token in unsorted_stripped:
            key_token = us_token
            if simplify:
                for simpl in self.simplify:
                    key_token = key_token.replace(simpl, self.simplify[simpl])
                key_token = key_token.lower()
            if key_token not in corresp:
                corresp[key_token] = []
            if key_token not in corresp_indices:
                corresp_indices[key_token] = []
            corresp[key_token].append(us_token)
            corresp_indices[key_token].append(
                [x for x, v in enumerate(unsorted_stripped) if v == us_token and x not in corresp_indices[key_token]][0]
            )
            corresp_use[key_token] = 0
            sorted_stripped.append(key_token)
        sorted_stripped.sort()
        sorted_indexed = []
        for token in sorted_stripped:
            sorted_indexed.append(
                (corresp_indices[token][corresp_use[token]], corresp[token][corresp_use[token]])
            )
            corresp_use[token] += 1
        return sorted_indexed


sm = SplitString("вор ургалан хотпа леснйк /суй урәйл’ӓ°л’нәха°р, суй урәй-л’ӓнха°р; суй урәйл’ӓпха°р, суй урил’ӓлха°р ворсик I трясогӱзка /вӓрщәх Ворсик II Ворсик (клйчка со-бякн) /Ворсих")
print(sm.sort_mansi(sm.str2split))
while True:
    print(sm.check_in_af_range(int(input())))