#!/usr/bin/python3

import re
import string
import itertools
import is_russian
import json
import sqlite3
import time


class Stem:
    def __init__(self, save_cache=None):
        self.bal_file = open('balandin_vakhr_5.txt', encoding='utf-8-sig').read().splitlines()
        self.token_index = {}
        self.r_checker = is_russian.Checker(import_op=False)
        self.save_cache = save_cache
        if self.save_cache:
            self.cache_db = sqlite3.connect(self.save_cache)
            self.cache_db_cursor = self.cache_db.cursor()
            try:
                self.cache_db_cursor.execute('CREATE TABLE stemmer_cache(title text, result text)')
            except sqlite3.OperationalError:
                pass
        else:
            self.cache_db_cursor = None
        self.lozv = sqlite3.connect('lozv.sqlite3')
        self.lozv_cursor = self.lozv.cursor()
        for e, line in enumerate(self.bal_file):
            for token in line.split():
                token = token.strip(string.punctuation)
                if token not in self.token_index:
                    self.token_index[token] = []
                self.token_index[token].append(e)

    def cache_result(self, title, result):
        if not self.cache_db_cursor:
            return
        result = json.dumps(result)
        wq = 'INSERT INTO stemmer_cache(title, result) SELECT ?, ? ' \
             'WHERE NOT EXISTS(SELECT 1 FROM stemmer_cache WHERE title=?)'
        self.cache_db_cursor.execute(wq, (title, result, title,))

    def write_cache(self):
        self.cache_db.commit()
        self.cache_db.close()
        self.lozv.close()

    def cache_request(self, title):
        if not self.cache_db_cursor:
            return None
        res = self.cache_db_cursor.execute('SELECT result FROM stemmer_cache WHERE title=?', (title,)).fetchall()
        if res:
            return [json.loads(x[0]) for x in res]
        return None

    def find(self, token, start_del=[], end_del=[], start_add=[], end_add=[]):
        del_substrings = [('start_del', x) for x in start_del]
        del_substrings += [('end_del', x) for x in end_del]
        del_perms = [[]]
        for e in range(len(del_substrings)):
            perms = list(itertools.permutations(del_substrings, e + 1))
            for perm in perms:
                del_perms.append(perm)
        del_perms = sorted(del_perms, key=lambda p: len(''.join([x[1] for x in p])))
        line_arr = {}
        stems = {}
        for perm in del_perms:
            token_snapshot = token
            is_valid = True
            if perm:
                for role, chars in perm:
                    if role == 'start_del' and token_snapshot.startswith(chars):
                        token_snapshot = token_snapshot[len(chars):]
                    elif role == 'start_del':
                        is_valid = False
                        break
                    elif role == 'end_del' and token_snapshot.endswith(chars):
                        token_snapshot = token_snapshot[:-len(chars)]
                    elif role == 'end_del':
                        is_valid = False
                        break
            if not is_valid:
                continue
            ###
            creq = self.cache_request(token_snapshot)
            if creq:
                return creq

            if token_snapshot in self.token_index:
                line_arr[token_snapshot] = tuple(self.bal_file[x] for x in self.token_index[token_snapshot])
                if token_snapshot not in stems:
                    stems[token_snapshot] = []
                stems[token_snapshot].append(token_snapshot)
            else:
                for sa in start_add:
                    if sa + token_snapshot in self.token_index:
                        line_arr[sa + token_snapshot] = tuple(
                            self.bal_file[x] for x in self.token_index[sa + token_snapshot]
                        )
                        if sa + token_snapshot not in stems:
                            stems[sa + token_snapshot] = []
                        stems[sa + token_snapshot].append(token_snapshot)
                        break
                for ea in end_add:
                    if token_snapshot + ea in self.token_index:
                        line_arr[token_snapshot + ea] = tuple(
                            self.bal_file[x] for x in self.token_index[token_snapshot + ea]
                        )
                        if token_snapshot + ea not in stems:
                            stems[token_snapshot + ea] = []
                        stems[token_snapshot + ea].append(token_snapshot)
                        break

        prop_set = []
        for ts in line_arr:
            arr = line_arr[ts]
            for line in arr:
                line = re.sub(r'\(.+?\)', '', line)
                line = re.sub(r'\s{2,}', ' ', line)
                ls = line.split()
                occs = [i for i, tkn in enumerate(ls) if tkn.strip() == ts]  # comparison function
                for occ in occs:
                    # *[EG()] (!) P R
                    if occ < len(ls) - 1 and not re.search(r'\d+\.?', ls[occ + 1]):
                        check_next = self.r_checker.check(ls[occ + 1])
                        if check_next:
                            # prop_set.append
                            props = {
                                'lemma': ls[occ],
                                'pos_tags': check_next[2],
                                'translation': '',
                                'stems': stems[ts]
                            }
                            i = occ + 1
                            while i < len(ls):
                                r_check = self.r_checker.check(ls[i].strip(string.punctuation))
                                if not r_check:
                                    break
                                props['translation'] += ' ' + r_check[1] + (',' if re.search(r'[;,]\s*$', ls[i]) else '')
                                i += 1
                            props['translation'] = [
                                x.strip(string.punctuation + ' ') for x in re.split(r'\s*[;,]\s*', props['translation'])
                            ]
                            prop_set.append(props)
                    elif occ < len(ls) - 1 and re.search(r'\d+\.?', ls[occ + 1]):
                        parsed_field = ' '.join(ls[occ + 1:])
                        numbered_group = re.search(r'(\d+\.\s*[^;/]+([;])?\s*)+', parsed_field).group(0)
                        translations = [
                            re.sub(r'^\d+\.?\s*', '', x).strip(string.punctuation + ' ')
                            for x in re.split(r'\s*[;,]\s*', numbered_group)
                        ]

                        # polymorphism sucks:
                        def convert_none(x): return (None,) * 3 if x is None else x

                        pw_pairs = [convert_none(self.r_checker.check(x))[1:] for x in translations]

                        pw_pairs = [x for x in pw_pairs if None not in x]
                        props = {
                            'lemma': ls[occ],
                            'pos_tags': [x[1] for x in pw_pairs],
                            'translation': [x[0] for x in pw_pairs],
                            'stems': stems[ts]
                        }
                        props['pos_tags'] = list(set(list(itertools.chain(*props['pos_tags']))))
                        prop_set.append(props)

        returned_set = []
        for obj in prop_set:
            if obj not in returned_set:
                returned_set.append(obj)
                for stem in obj['stems']:
                    self.cache_result(stem, obj)
        return returned_set


stemmer = Stem(save_cache='cache_table.sqlite3')
start = time.time()
print(stemmer.find('потыртас', start_del=[], end_del=['а', 'с'], end_add=['ӈкве', 'аӈкве', 'юӈкве', 'уӈкве']))
print(time.time() - start)
stemmer.write_cache()