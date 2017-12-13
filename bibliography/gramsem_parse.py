#!/usr/bin/python3
import re
import string
import pymorphy2

bibliography_file = open('gramsem_bibliography.txt', encoding='utf-8').read().splitlines()
gramsem_keywords = open('gramsem_keywords.txt', encoding='utf-8').read()
gramsem_stopwords = open('gramsem_stopwords.txt', encoding='utf-8').read().splitlines()
dict_bibliography = {}
last_key = None
for e, line in enumerate(bibliography_file):
    if line.startswith('KW'):
        a, b = line.split(' ', 1)
        last_key = b
        dict_bibliography[last_key] = []
    else:
        dict_bibliography[last_key].append(line)

for key in dict_bibliography:
    dict_bibliography[key] = ' '.join(dict_bibliography[key])

ref_regex = r'(([A-Z]\.|ван|дер|van|der|de|[А-ЯЁ][а-яё\-]+|[A-Z][a-zöäüàáèéòó\-]+|др\.)(\s*[&и,]\s*|\s)?)+(\s*et\s*al'
ref_regex += r'\.?)?\s*(\([^\)]+\))?\s*(\d+[a-z]?(\s*[,и]\s*(?=\d))?)+(:\s*\d+-\d+)?|(«[^»]+»(\s*[и,]\s*)?)+'
ref_regex += r'\s*\(([^\)]+)\)'
m = pymorphy2.MorphAnalyzer()
for key in dict_bibliography:
    LES_START = False
    sentences = re.split(r'(?<!с[мр]|ed|ds|ед|al|гл|Гл|гг|\sг|др|ol|.[A-ZА-ЯЁ])\s*\.\s*', dict_bibliography[key])
    keywords_cache = {}
    for e, sentence in enumerate(sentences):
        keywords = []
        stripped = re.sub(r'[«»\(\)]', '', sentence)
        for token in stripped.split():
            token = token.strip('.,!?():;')
            mp = m.parse(token)
            if 'NOUN' not in mp[0].tag:
                continue
            lemma = mp[0].normal_form
            if lemma.endswith('ов'):
                continue
            s_pattern = '^' + lemma + '[^А-ЯЁа-яё]|[^А-ЯЁа-яё]' + lemma + '[^А-ЯЁа-яё]|[^А-ЯЁа-яё]' + lemma + '$'
            additional = []
            for grammeme in ('nomn', 'gent', 'datv', 'accs', 'ablt'):
                try:
                    inf_token = mp[0].inflect({grammeme}).word
                except AttributeError:
                    continue
                additional.append(
                    '^' + inf_token + '[^А-ЯЁа-яё]|[^А-ЯЁа-яё]' + inf_token + '[^А-ЯЁа-яё]|[^А-ЯЁа-яё]' + inf_token + '$'
                )
            s_pattern += '|' + '|'.join(additional)
            s_pattern = s_pattern.strip('|')
            if re.search(s_pattern, gramsem_keywords, re.IGNORECASE) and lemma not in gramsem_stopwords:
                keywords.append(lemma)
                if re.search('[ыи]й$', lemma):
                    keywords.append(lemma[:-2] + 'ость')
        if not keywords:
            i = e
            while i > 0:
                if i in keywords_cache and keywords_cache[i]:
                    keywords = keywords_cache[i]
                    break
        if 'ЛЭС' in sentence:
            LES_START = True

        references = re.finditer(ref_regex, sentence)
        ref_filtered = []
        for reference in references:
            ref = reference.group(0)
            if ('«' in ref or '»' in ref) and not LES_START:
                print(7)
                continue
            ref_filtered.append(ref)
        print(ref_filtered)
