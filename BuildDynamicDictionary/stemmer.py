#!/usr/bin/python3

from collections import Counter
import datrie
import json


class WordEntry:
    def __init__(self, lemma):
        self.lemma = lemma
        self.full_lemma = lemma
        self.reduce_lemma()
        self.pos_options = []
        self.rus_meanings = []
        self.common_pos = None

    def reduce_lemma(self):
        self.lemma = re.sub(r'[ёуеыаоэяию]ӈкве$', '', self.lemma)

    def dynamic_lemma(self, wf):
        if wf.endswith("ь"):
            return self.full_lemma
        return self.lemma

    def get_pos(self, update=False):
        if self.common_pos is not None and not update:
            return self.common_pos
        else:
            self.common_pos = Counter(self.pos_options).most_common(1)[0][0]
            return self.common_pos


stem_base = datrie.Trie.load('dict_entries.trie')

print(base.longest_prefix(u'маньщи'))
