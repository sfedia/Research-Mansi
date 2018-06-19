#!/usr/bin/python3

import json
import os
import re


txt_files = [fn for fn in os.listdir('./decoded_pdf') if fn.endswith('.txt')]


class FormatTxt:
    def __init__(self, file_name):
        self.content = open('./decoded_pdf/' + file_name, encoding='utf-8').read()
        self.pre_format_content()
        self.text_clusters = []
        self.extract_clusters()
        self.text_clusters = [cluster for cluster in self.text_clusters if self.relevant_cluster(cluster)]

    def pre_format_content(self):
        self.caps_to_titles()

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


ft = FormatTxt('luima_seripos_1_1043_7.txt')
print(ft.text_clusters)
ft.print_clusters()