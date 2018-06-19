#!/usr/bin/python3

from itertools import groupby
import json
import os
import re
import string


txt_files = [fn for fn in os.listdir('./decoded_pdf') if fn.endswith('.txt')]


class FormatTxt:
    def __init__(self, file_name):
        self.content = open('./decoded_pdf/' + file_name, encoding='utf-8').read()
        self.url_digits = tuple(re.findall(r'\d+', file_name))
        self.pre_format_content()
        self.text_clusters = []
        self.extract_clusters()
        self.text_clusters = [cluster for cluster in self.text_clusters if self.relevant_cluster(cluster)]
        self.text_clusters = [self.format_cluster(cluster) for cluster in self.text_clusters]
        self.defective_clusters = []
        self.added_clusters = []
        self.text_clusters = [self.clear_cluster(cluster, j) for j, cluster in enumerate(self.text_clusters)]
        self.text_clusters += self.added_clusters
        self.json_object = self.create_json_object()

    def pre_format_content(self):
        self.caps_to_titles()

    def clear_cluster(self, cluster, cluster_num):
        split_sym = r'(?<=[^А-ЯЁ])\s*[\.\?!]\s*'
        sentences = re.split(split_sym, cluster)
        split_symbols = re.findall(split_sym, cluster)

        if len(sentences) == 1:
            return cluster

        if sentences[-1] != "":
            self.defective_clusters.append([cluster_num, sentences[-1]])
            sentences[-1] = None
        else:
            sentences = sentences[:-1]

        for j, sentence in enumerate(sentences):
            if sentence is None:
                continue
            sentence = sentence.strip(" ")
            punct = list(string.punctuation + '«»')
            i = 0
            while i + 1 < len(sentence) and sentence[i] in punct:
                i += 1

            if not sentence[i].istitle():
                self.defective_clusters.append([cluster_num, sentence])
                sentences[j] = None

        sentences = [[split_symbols[q], s] for q, s in enumerate(sentences) if q < len(split_symbols)]
        sent_groups = [list(g) for k, g in groupby(sentences, lambda x: x[1] is None) if not k]
        for sg in sent_groups[:-1]:
            for sent in sg:
                self.added_clusters.append((sent[1] + sent[0]).strip(" "))

        string_cluster = ''
        for sent in sent_groups[-1]:
            string_cluster += (sent[1] + sent[0])

        return string_cluster.strip(" ")

    def format_cluster(self, cluster):
        cluster = re.sub(r'\n\d+$', '', cluster)
        cluster = re.sub(r'\n\d+(?=\n)', '', cluster)

        cluster = re.sub(r'(.+)\n([A-ZА-Я]̄?)\n', '\g<2>\g<1>\n', cluster)

        """ла̄тӈыл Л. Тасманова хансыстэ
        хансыстэ.."""
        cluster = re.sub(r'\n[^\s]+\.\.$', '', cluster)

        cluster = self.create_sentences(cluster)

        return cluster

    @staticmethod
    def create_sentences(cluster):
        cluster = " ".join(cluster.splitlines())
        cluster = re.sub(r'\s{2,}', ' ', cluster)
        cluster = re.sub(r'[^\s\t\n-]-\s', '', cluster)

        return cluster

    @staticmethod
    def relevant_cluster(cluster):
        if re.search(r'л?\s*уима|сэ.?рипос|общественно-политическая', cluster, re.IGNORECASE):
            return False

        kwb_search = re.findall(r'основан[ао]|11[\s\n\t]*февраля|1989[\s\n\t]*года', cluster, re.IGNORECASE)
        if len(kwb_search) >= 2:
            return False

        if re.search(r'e-?mail|@', cluster, re.IGNORECASE):
            return False

        if re.search(r'№(.|[\s\n\t])*\(\d{4}\)', cluster):
            return False

        if re.search(r'^[\s\n\t]*\d+[\s\n\t]*$', cluster):
            return False

        if re.search(r'\d{2}\.\d{2}.\d{2}', cluster):
            return False

        if re.search(r'лс[\s\n\t]*№[\s\n\t]*\d+|№[\s\n\t]*\d+[\s\n\t]*лс', cluster, re.IGNORECASE):
            return False

        return True

    def caps_to_titles(self):
        first_upper = False
        for j, char in enumerate(self.content):
            if first_upper:
                if char.istitle():
                    self.content = self.content[:j] + char.lower() + self.content[j+1:]
                else:
                    if char == '̄':
                        pass
                    else:
                        first_upper = False
            elif char.istitle():
                first_upper = True

    def extract_clusters(self):
        self.content = re.sub(r'\n{3,}', '\n\n', self.content)
        self.text_clusters = re.split(r'\n\n', self.content)

    def print_clusters(self):
        for num, cluster in enumerate(self.text_clusters):
            print('---')
            print('Cluster %d:' % num)
            print(cluster)

    def print_defective_clusters(self):
        for num, cluster in enumerate(self.defective_clusters):
            print('***')
            print('Defective cluster %d:' % num)
            print(cluster)

    def create_json_object(self):
        return json.dumps({
            "url": "http://www.khanty-yasang.ru/luima-seripos/no-%s-%s/%s" % self.url_digits,
            "title": None,
            "content": {
                "good": self.text_clusters,
                "uncertain": self.defective_clusters
            }
        })

    def save_json(self):
        with open("luima_seripos_%s_%s_%s.json" % self.url_digits, 'w') as sj:
            sj.write(self.json_object)
            sj.close()


ft = FormatTxt('luima_seripos_1_1043_5.txt')
ft.print_clusters()
ft.print_defective_clusters()