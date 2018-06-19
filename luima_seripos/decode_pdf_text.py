#!/usr/bin/python3

import json
import os
import re
import requests
import time


class FileDecode:
    def __init__(self, file_path, file_name, saving_folder, debug_mode=False):
        self.file_path = file_path
        self.file_name = file_name
        self.saving_folder = saving_folder
        self.capsules = []
        self.debug_mode = debug_mode
        self.text = open(self.file_path + '/' + self.file_name, encoding='utf-8').read()

    def format_text(self):
        self.remove_i()
        self.make_capsules()
        self.change_encoding()
        self.regular_correction()
        self.unpack_capsules()

    def remove_i(self):
        self.text = re.sub(r'\nI+\n', '\n', self.text)

    def key_gen(self, number=None):
        return "%~$" + str(len(self.capsules) if number is None else number) + "$~%"

    def make_capsules(self):
        regex_list = [
            r'«[IV]{2,}',
            r'WBI',
            r'[a-zа-яA-Z0-9_.+-]+@[a-zа-яA-Z0-9-]+\.[a-zа-яA-Z0-9-.]+',
            r'http:\/*([a-z\/]+.?\n?)+',
            r'[a-z]{4,}\n?\.([a-z]{2,}\.?\n?)+',
            r'[Ee]-?mail',
        ]
        for regex in regex_list:
            found = [x.group(0) for x in re.finditer(regex, self.text)]
            for occurrence in found:
                self.text = self.text.replace(occurrence, self.key_gen())
                self.capsules.append(occurrence)

    def unpack_capsules(self):
        for j, capsule in enumerate(self.capsules):
            self.text = self.text.replace(self.key_gen(j), self.capsules[j])

    def pack_capsule(self, regex):
        key = "%~$" + str(len(self.capsules)) + "$~%"
        found = [x.group(0) for x in re.finditer(regex, self.text)]
        for occurrence in found:
            self.text = self.text.replace(occurrence, key)

    def change_encoding(self):
        time.sleep(0.1)
        json_txt = requests.post('https://www.artlebedev.ru/tools/decoder/ajax.html', data={
            'msg': self.text
        }).text
        json_txt = json.loads(json_txt)
        self.text = json_txt['text']

    def regular_correction(self):
        corr = {
            "f": "а̄",
            "a": "а̄",
            "p": "э̄",
            "y": "ӯ",
            "j": "о̄",
            "h": "ӈ",
            "z": "я̄",
            "s": "ы̄",
            "t": "е̄",
            "b": "ӣ",
            "e": "ё̄",
            "c": "с",
            "u": "ю̄",
        }
        for symbol in corr:
            self.text = self.text.replace(symbol, corr[symbol])
            self.text = self.text.replace(symbol.upper(), corr[symbol].upper())

        latin_symbols = re.findall(r'[A-Za-z]', self.text)
        latin_symbols = list(set(latin_symbols))

        if latin_symbols:
            if self.debug_mode:
                print(self.text)
            raise ValueError(", ".join(latin_symbols) + ": " + self.file_name)

    def save_text(self):
        with open(self.saving_folder + '/' + self.file_name, 'w', encoding='utf-8') as saved_file:
            saved_file.write(self.text)
            saved_file.close()


pdf_texts = [fn for fn in os.listdir('./pdf_text') if fn.endswith('.txt')]
for pdf_file in pdf_texts:
    print('Converting file %s...' % pdf_file)
    fd = FileDecode('./pdf_text', pdf_file, './decoded_pdf')
    fd.format_text()
    fd.save_text()