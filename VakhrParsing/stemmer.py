#!/usr/bin/python3

import re
import string
import itertools
import is_russian


class Stem:
    def __init__(self):
        self.bal_file = open('balandin_vakhr_5.txt', encoding='utf-8-sig').read().splitlines()
        self.token_index = {}
        self.r_checker = is_russian.Checker(import_op=False)
        for e, line in enumerate(self.bal_file):
            for token in line.split():
                token = token.strip(string.punctuation)
                if token not in self.token_index:
                    self.token_index[token] = []
                self.token_index[token].append(e)

    def find(self, token, start_del=[], end_del=[]):
        del_substrings = [('start', x) for x in start_del]
        del_substrings += [('end', x) for x in end_del]
        del_perms = []
        for e in range(len(del_substrings)):
            perms = list(itertools.permutations(del_substrings, e + 1))
            for perm in perms:
                del_perms.append(perm)
        del_perms = sorted(del_perms, key=lambda p: len(''.join([x[1] for x in p])))
        line_arr = {}
        for perm in del_perms:
            token_snapshot = token
            for position, chars in perm:
                if position == 'start' and token_snapshot.startswith(chars):
                    token_snapshot = token_snapshot[len(chars):]
                elif position == 'end' and token_snapshot.endswith(chars):
                    token_snapshot = token_snapshot[:-len(chars)]
                ###
                if token_snapshot in self.token_index:
                    line_arr[token_snapshot] = tuple(self.bal_file[x] for x in self.token_index[token_snapshot])
        prop_set = []
        for ts in line_arr:
            arr = line_arr[ts]
            for line in arr:
                ls = line.split()
                occs = [i for i, tkn in enumerate(ls) if tkn.strip() == ts]  # comparison function
                for occ in occs:
                    # *[EG()] P R
                    if occ < len(ls) - 1:
                        check_next = self.r_checker.check(ls[occ + 1])
                        if check_next:
                            # prop_set.append
                            props = {
                                'lemma': ls[occ],
                                'pos_tags': check_next[2],
                                'translation': ['']
                            }
                            i = occ + 1
                            while i < len(ls):
                                r_check = self.r_checker.check(ls[i].strip(string.punctuation))
                                print(ls[i], r_check)
                                if not r_check:
                                    break
                                if not re.search(r'\s*[,;]\s*$', ls[i]):
                                    if not props['translation'][-1]:
                                        props['translation'][-1] = r_check[1].strip(string.punctuation)
                                    else:
                                        props['translation'][-1] += ' ' + r_check[1].strip(string.punctuation)
                                else:
                                    props['translation'].append(r_check[1].strip(string.punctuation))
                                i += 1
                            prop_set.append(props)

        returned_set = []
        for obj in prop_set:
            if obj not in returned_set:
                returned_set.append(obj)
        return returned_set


stemmer = Stem()
print(stemmer.find('нэпакыт', start_del=[], end_del=['ыт', 'т']))