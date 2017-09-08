#!/usr/bin/python3
import re
import requests
from string import punctuation
import time
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
    def __init__(self):
        pass

    class Twirpx:
        def __init__(self, query):
            self.pi = 0
            self.query = query
            self.sart = ''
            self.session = requests.Session()
            self.start = self.session.get('http://www.twirpx.com').text
            self.request_pi()
            self.pi_max = int(re.findall(r'(?<=data-page-index=")(\d+)', self.start)[-1])
            self.metadata = self.parse_list()
            self.get_next()

        def update_sart(self):
            self.sart = re.search(r'__SART[^>]+value\s*=\s*"([^"]+)', self.start).group(1)

        def request_pi(self):
            self.update_sart()
            self.start = self.session.post('http://www.twirpx.com/search/',
                data={
                    'SearchQuery': self.query,
                    'SearchScope': 'site',
                    'SearchUID': 0,
                    'SearchCID': 0,
                    'SearchECID': 0,
                    'pi': self.pi,
                    '__SART': self.sart
                },
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/59.0.3071.115 Safari/537.36'
                }
            ).text
            print(self.start)

        def analyze_file(self, url):
            res = self.session.get(url).text
            description = re.search(r'itemprop="description">\n*.+', res).group(0)
            description = re.sub(r'itemprop="description">|<[^>]*>', '', description)
            proc = Text(description)
            title = re.search(r'<meta\sproperty="og:title"\scontent="([^"]+)"\s+\/>', res).group(0)
            if proc.is_good():
                return [title] + proc.get_metadata()
            else:
                return False

        def parse_list(self):
            metadata = []
            for file in re.finditer(r'<a\sclass=\"file-link\"\shref="([^"]+)"', self.start):
                metadata.append(self.analyze_file(file.group(1)))
            return metadata

        def make_report(self, message):
            print('Twirpx parser report: {}'.format(message))

        def get_next(self):
            if self.pi < self.pi_max:
                self.request_pi()
                self.metadata += self.parse_list()
                self.pi += 1
                time.sleep(0.3)
                self.make_report(self.pi)
                self.get_next()
            else:
                return False

        def final_metadata(self):
            return self.metadata


for theme in ['манси']:
    md = Src.Twirpx(theme)
    from_ = json.loads(open('result.json').read())
    from_ += md.final_metadata()
    with open('result.json', 'a') as result:
        result.write(from_)
        result.close()

