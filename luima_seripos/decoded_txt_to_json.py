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
        self.pre_format_content()
        self.text_clusters = []
        self.extract_clusters()
        self.text_clusters = [cluster for cluster in self.text_clusters if self.relevant_cluster(cluster)]
        self.text_clusters = [self.format_cluster(cluster) for cluster in self.text_clusters]
        self.defective_clusters = []
        self.text_clusters = [self.clear_cluster(cluster, j) for j, cluster in enumerate(self.text_clusters)]

    def pre_format_content(self):
        self.caps_to_titles()

    def clear_cluster(self, cluster, cluster_num):
        sentences = re.split(r'(?<=[^А-ЯЁ])\s*\.\s*', cluster)
        if sentences[-1] != "":
            self.defective_clusters.append([cluster_num, sentences[-1]])
            sentences[-1] = None

        for j, sentence in enumerate(sentences):
            sentence = sentence.strip(" ")
            punct = list(string.punctuation + '«»')
            i = 0
            while sentence[i] in punct and i < len(sentence):
                i += 1

            if not sentence[i].istitle():
                self.defective_clusters.append([cluster_num, sentence])
                sentences[j] = None

        sent_groups = [list(g) for k, g in groupby(sentences, lambda x: x is None) if not k]
        self.defective_clusters += [[cluster, sg] for sg in sent_groups[:-1]]

        return '. '.join(sent_groups[-1])







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

        if re.search(r'лс[\s\n\t]*№[\s\n\t]*\d+', cluster, re.IGNORECASE):
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


ft = FormatTxt('luima_seripos_1_1043_11.txt')
print(ft.text_clusters)
ft.print_clusters()