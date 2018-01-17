#!/usr/bin/python3

import re
import is_russian
import string

bal_vakhr = open('balandin_vakhr_4.txt', encoding='utf-8').read().splitlines()
checker = is_russian.Checker(import_op=False)
len_bv = len(bal_vakhr)
new_bv = []


class SplitString:
    def __init__(self, str2split, next_lines=[], simplify=True, debug=False):
        self.debug = debug
        self.str2split = str2split
        self.src_str2split = self.str2split
        self.str2split = re.sub(r',(?!\s)', ', ', self.str2split)
        self.str2split = re.sub(r'\d+\.\s*', '', self.str2split)
        self.symbols = [x for x in 'аӓбвгдеёжзийклмнӈоӧөпрстуӱфхцчшщъыьэәӛюя']
        self.next_lines = next_lines
        self.simplify = {
            'ӓ': 'а',
            'ӧ': 'о',
            'ӱ': 'у',
            'ӈ': 'н',
            'ӛ': 'ә'
        }
        self.sorted = self.sort_mansi(self.str2split, simplify)
        self.str_splitted = self.str2split.split()
        self.class_cmcc = r'[А-ЯӒЁӇӦӰӘӚ]'
        self.class_smcc = r'[а-яӓёӈӧөӱәӛ]'
        self.class_smcc_n_punct = r"[а-яӓёӈӧөӱәӛ\,\-\s']"
        self.class_smcc_n_punct_ext = r"[а-яӓёӈӧөӱәӛ\,\-\s\(\)']"
        self.regex_examples = r'{CMCC}{SMCC_PUNCT_EXT}+\s*[\.!\?](\s*{CMCC}({SMCC_PUNCT_EXT}+(\.\s*{SMCC}+)?)+\s*[\.!\?]*\s*)?'
        self.regex_examples += r'|;(\s+{SMCC_PUNCT}+)'
        self.token_number = 0
        self.regex_examples = self.regex_examples.format(
            CMCC=self.class_cmcc,
            SMCC=self.class_smcc,
            SMCC_PUNCT=self.class_smcc_n_punct,
            SMCC_PUNCT_EXT=self.class_smcc_n_punct_ext
        )
        self.regex_examples += r'{5,}'
        self.examp_ranges = self.regex_ranges(self.regex_examples, self.str2split)
        if debug:
            print('Examp_Ranges:', self.examp_ranges)

    def regex_ranges(self, regex, search_string):
        new_token_inds = []
        new_token = True
        for i, sym in enumerate(search_string):
            if new_token:
                new_token_inds.append(i)
                new_token = False
            elif sym == ' ':
                new_token = True
        sym_ranges = [[x.start(), x.end()] for x in re.finditer(regex, search_string)]
        if self.debug:
            print('Sym_Ranges:', sym_ranges)
        token_ranges = []
        for sr_start, sr_end in sym_ranges:
            start_token = min(new_token_inds, key=lambda x: abs(x - sr_start) * (65536 if x > sr_start else 1))
            end_token = min(new_token_inds, key=lambda x: abs(x - sr_end) * (65536 if x < sr_end else 1))
            token_ranges.append([new_token_inds.index(start_token), new_token_inds.index(end_token)])
        return token_ranges

    @staticmethod
    def in_regex_ranges(position, ranges):
        for start, end in ranges:
            if end >= position >= start:
                return True
        return False

    def append_tn(self, x):
        self.token_number += x
        return x

    def check_in_af_range(self, position):
        str_splitted_ed = self.str2split
        str_splitted_ed = str_splitted_ed.split()

        if re.search(r"[’°'ө]", str_splitted_ed[position]):
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

        wrong_const = 3

        root = str_splitted_ed[position]
        prefix = ' '.join(str_splitted_ed[:position + 1])
        postfix = ' '.join(str_splitted_ed[position:])

        prefix_groups = re.search(r'/([^/]+{})$'.format(root), prefix).group(1)
        prefix_forms = [x.strip() for x in re.findall(r'[^),;]+', prefix_groups)]

        self.token_number = 0
        pf_length_values = [self.append_tn(len(x.split())) for x in prefix_forms]
        pf_ne_length = pf_length_values[0]
        pf_max_length = max(pf_length_values)
        if pf_max_length > wrong_const:
            return False

        slash_pos = position - self.token_number + 1

        pf_ne_length_decr = pf_ne_length - 1
        postfix_forms_regex = r'^' + root
        postfix_forms_regex += r'(\s+{SMCC}+)'.format(SMCC=self.class_smcc)
        postfix_forms_regex += r'{' + str(pf_ne_length_decr) + r'}'

        try:
            postfix_forms = re.search(postfix_forms_regex, postfix).group(0).split()
        except AttributeError:
            return False

        postfix_forms = [x.strip() for x in postfix_forms]
        end_pos = position + len(postfix_forms) - 1
        if len(postfix_forms) > 1:
            del pf_length_values[-1]
            pf_length_values.append(len(postfix_forms) + len(prefix_forms[-1].split()) - 1)
        if len(pf_length_values) == len(set(pf_length_values)):
            return False
        if max(pf_length_values) != min(pf_length_values):
            return False
        """
        if len(pf_length_values) < 4 and max(pf_length_values) - min(pf_length_values) > 1:
            return False
        if len(pf_length_values) >= 4 and max(pf_length_values) != min(pf_length_values):
            return False
        """
        if max(pf_length_values) > wrong_const:
            return False

        return slash_pos <= position <= end_pos

    def sort_mansi(self, s, simplify=True):
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

    def get_split_positions(self):
        srted = self.sort_mansi(self.str2split)
        if self.debug:
            print('Sorted:', srted)
        split_positions = []
        null_index = [e for e, pair in enumerate(srted) if not pair[0]][0]
        title_sym = srted[null_index][1][0]
        this_index = self.symbols.index(title_sym)
        next_sym = None if this_index == len(self.symbols) - 1 else self.symbols[this_index + 1]
        last_index = None
        if null_index == len(srted) - 1:
            return []
        for index, token in srted[null_index + 1:]:
            if self.debug:
                print('Position', index, ', step', -1)
            if index <= 2 or re.search(r'\d+\.\s*' + token + r'\s+', self.src_str2split):
                continue
            if self.debug:
                print('Position', index, ', step', 0)
            alphabet_comparison = (next_sym is not None and token[0] in (title_sym, next_sym)) or title_sym == token[0]

            if alphabet_comparison and self.next_lines:
                if len(self.next_lines) == 1:
                    split_nl = self.next_lines[0].split()
                    if re.search(r'^\s*({}|{})'.format(self.class_smcc, self.class_cmcc), split_nl[0]):
                        alphabet_comparison = token < split_nl[0]
                elif len(self.next_lines) > 1:
                    split_nl_first = self.next_lines[0].split()
                    split_nl_second = self.next_lines[1].split()
                    is_good = True
                    for tkn in (split_nl_first[0], split_nl_second[0]):
                        is_good = re.search(r'^\s*({}|{})'.format(self.class_smcc, self.class_cmcc), tkn)
                    if is_good:
                        alphabet_comparison = token < split_nl_first[0] or token < split_nl_second[0]

            if alphabet_comparison:
                if self.debug:
                    print('Position', index, ', step', 1)
                if not self.in_regex_ranges(index, self.examp_ranges) and not self.check_in_af_range(index):
                    if self.debug:
                        print('Position', index, ', step', 2)
                    if last_index is None or (index - last_index) > 1:
                        if self.debug:
                            print('Position', index, ', step', 3)
                        split_positions.append(index)
                        last_index = index
        return split_positions


if __name__ == "__main__":
    while True:
        #print(SplitString(input(), debug=True).get_split_positions())
        a = SplitString(input(), debug=True)
        print(a.get_split_positions())