#!/usr/bin/python3
import re
import requests
from string import punctuation
import json


class Text:
    def __init__(self, data):
        self.text = data
    langPrefix = [r'манси.*', r'.*лозьв.*', r'vogul*', r'mansi*']
    isGoodKeywords = [
        langPrefix + [r'речь', r'миф|(рас)?сказ([ыовами]{,3}|ан|к)|предани.+|песн.+', r'яз(ык)?'],
        langPrefix + [r'перев[ое]д'],
        langPrefix + [r'памятник'],
        [langPrefix[0]],
        [langPrefix[1]]
    ]

    def is_good(self):
        sequence = []
        for line in self.text.splitlines():
            sequence += [x.strip(punctuation) for x in line.lower()]

        gk_len = len(self.isGoodKeywords)
        tests = [0 for _ in range(gk_len)]
        for token in sequence:
            for i in range(gk_len):
                for x in self.isGoodKeywords[i]:
                    if not re.search(x, token) is None:
                        tests[i] += 1
                    if tests[i] == 2:
                        break

        for i in range(gk_len):
            if len(self.isGoodKeywords[i]) == 1 and tests[i] > 0:
                return True
            elif len(self.isGoodKeywords[i]) > 1 and tests[i] == 2:
                return True

        return False

    def get_metadata(self):
        year_any = r'(19|20)\d{2}'
        published_by = r'[А-ЯЁа-яё]\.?:\s*[А-Яёа-яё«»"\s]+|[A-zА-ЯЁа-яё\s]+,\s*' + year_any
        pg_count_any = r'[\.\s—-]*(\d+)\s*c(тр)\.?'
        pub_and_year = published_by + r'[,\.]\s*' + "(" + year_any + ")?" + "(" + pg_count_any + ")?"

        pub_and_year_s = re.search(pub_and_year, self.text)
        if pub_and_year_s:
            return pub_and_year_s.group(0)
        else:
            stack = []
            published_by_s = re.search(published_by, self.text)
            if published_by_s:
                stack.append(published_by_s.group(0))
            year_any_s = re.search(year_any, self.text)
            if year_any_s:
                stack.append(year_any_s.group(0))
            pg_count_any_s = re.search(pg_count_any, self.text)
            if pg_count_any_s:
                stack.append(pg_count_any_s.group(0))

            return stack


class Src:
    class Twirpx:
        def __init__(self, query):
            self.start = requests.post('http://twirpx.com/search', data = {'SearchQuery' : query}).text

        def analyze_file(url):
            res = requests.get(url).text
            description = re.search(r'itemprop="description">\n*.+', res).group(0)
            description = re.sub(r'itemprop="description">|<[^>]*>', '', description)
            proc = Text(description)
            if proc.is_good():
                return proc.get_metadata()
            else:
                return False

        def