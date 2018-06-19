#!/usr/bin/python3

import json
import re
import requests


class FileDecode:
    def __init__(self, file_path, saving_folder):
        self.file_path = file_path
        self.saving_folder = saving_folder
        self.text = open(self.file_path).read()

    def change_encoding(self):
        json_txt = requests.post('https://www.artlebedev.ru/tools/decoder/ajax.html', data={
            'msg': self.text
        }).text
        json_txt = json.loads(json_txt)
        self.text = json_txt['text']

    def regular_correction(self):
        corr = {
            "f": "а̄",
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
            "u": "ю̄"
        }
        for symbol in corr:
            self.text = self.text.replace(symbol, corr[symbol])

        latin_symbols = re.findall(r'[a-z]', self.text)
        latin_symbols = list(set(latin_symbols))

        if latin_symbols:
            raise ValueError(", ".join(latin_symbols) + ": " + self.file_path)

    def save_text(self):
        with open(self.saving_folder + '/' + self.file_path, 'w') as saved_file:
            saved_file.write(self.text)
            saved_file.close()