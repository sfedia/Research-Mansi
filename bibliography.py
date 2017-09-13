#!/usr/bin/python3
import re
import requests
from string import punctuation
import time


class Text:
    def __init__(self, data):
        self.text = data
    langPrefix = [r'(?<!-)манси.*', r'.*лозьв.*', r'vogul*', r'mansi*']
    fiction = [r'повест[ьяеи]', 'роман', 'бестселлер']
    industry = [r'нефт', 'газ', 'металл', 'промышл', 'производств', '(эко|био)лог', 'строит']
    isGoodKeywords = [
        [
            langPrefix + [r'речь', r'миф|(рас)?сказ([ыовами]{,3}|ан|к)|предани.+|песн.+', r'^яз(ык)?'],
            [fiction, industry]
        ],
        [
            langPrefix + [r'фолькл*', 'культур'],
            [fiction, industry]
        ],
        [
            langPrefix + [r'перев[ое]д', 'учебн'],
            [fiction, industry]
        ],
        [
            langPrefix + [r'памятник'],
            [fiction, industry]
        ]
    ]

    def is_good(self):
        sequence = []
        for line in self.text.splitlines():
            sequence.append(' '.join([x.strip(punctuation) for x in line.lower().split()]))

        gk_len = len(self.isGoodKeywords)
        tests = [0 for _ in range(gk_len)]
        f_used = {}

        for sub_sequence in sequence:
            for token in sub_sequence.split():
                for i in range(gk_len):
                    if not i in f_used:
                        f_used[i] = []
                    for x in self.isGoodKeywords[i][0]:
                        if x in f_used[i]:
                            continue
                        if not re.search(x, token) is None:
                            tests[i] += 1
                            f_used[i].append(x)
                            print("+", x)
                        if tests[i] == 2:
                            break
                    for l in self.isGoodKeywords[i][1]:
                        for x in l:
                            if not re.search(x, token) is None:
                                tests[i] = 0
                                print("!", x)

        print("...", tests)

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
            return [pub_and_year_s.group(0)]
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
        def __init__(self, query, soft_start = False):
            self.session = requests.Session()
            if not soft_start:
                self.pi = 0
                self.query = query
                self.sart = ''
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

        def analyze_file(self, url):
            res = self.session.get(url).text
            description = re.findall(r'itemprop="description">[^\$]+', res, re.MULTILINE)[0]
            description = re.split(r'<\/div>[\s\n\t]*<\/div>[\s\n\t]*<\/div>', description)[0]
            description = re.sub(r'itemprop="description">', '', description).strip()
            dspl = description.split('<div class="bb-sep"></div>')
            if len(dspl) > 1:
                metadata = re.split(r'<\/*br[^>]*>', dspl[0].strip())[0]
            else:
                metadata = ''
            description = re.sub(r'<[^>]*>', '', description).strip()
            title = re.search(r'<meta\sproperty="og:title"\scontent="([^"]+)"\s+\/>', res).group(1).strip()
            proc = Text(title + ' ' + description)
            if proc.is_good():
                #return [title] + proc.get_metadata()
                print(metadata)
                metadata = description.splitlines()[0]
                return [title] + [metadata]
            else:
                return False

        def parse_list(self):
            metadata = []
            for file in re.finditer(r'<a\sclass=\"file-link\"\shref="([^"]+)"', self.start):
                metadata.append(self.analyze_file('http://twirpx.com' + file.group(1)))
                time.sleep(0.3)
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

