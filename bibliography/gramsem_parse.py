#!/usr/bin/python3
import re
import string
import pymorphy2

refworks_code = ''
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

extracted_objects = []
ref_regex = r'(([A-Z]\.|ван|дер|van|der|de|[А-ЯЁ][а-яё\-]+|[A-Z][a-zöäüàáèéòó\-]+|др\.)(\s*[&и,]\s*|\s)?)+(\s*et\s*al'
ref_regex += r'\.?)?\s*(\([^\)]+\))?\s*(\d+[a-z]?(\s*[,и]\s*(?=\d))?)+(:\s*\d+-\d+)?|(«[^»]+»(\s*[и,]\s*)?)+'
ref_regex += r'\s*\(([^\)]+)\)'
m = pymorphy2.MorphAnalyzer()
for key in dict_bibliography:
    print(key)
    LES_START = False
    sentences = re.split(r'(?<!с[мр]|ed|ds|ед|al|гл|Гл|гг|\sг|др|ol|.[A-ZА-ЯЁ])\s*\.\s*', dict_bibliography[key])
    keywords_cache = {}
    for e, sentence in enumerate(sentences):
        print(e)
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
                i -= 1
        if 'ЛЭС' in sentence:
            LES_START = True

        references = re.finditer(ref_regex, sentence)
        ref_filtered = []
        for reference in references:
            ref = reference.group(0)
            if ('«' in ref or '»' in ref) and not LES_START:
                continue
            ref_filtered.append(ref)

        if not ref_filtered:
            continue

        ref_parsed = []

        for ref in ref_filtered:
            if '«' not in ref:
                obj = {}
                if ':' in ref:
                    obj['pages'] = re.search(r':\s*(\d+-\d+)', ref).group(1)
                    ref = re.sub(':.*', '', ref)
                    obj['type'] = 'book,part'
                else:
                    obj['type'] = 'book,whole'
                ref = re.sub(r'\d+[a-z]?\s*[,и]\s*\d+[a-z]?', '', ref)
                obj['years'] = re.findall(r'\d+[a-z]?', ref)
                ref = re.sub('\d+[a-z]?', '', ref)
                obj['marks'] = re.findall(r'(?<=\()[^\)]+', ref)
                ref = re.sub(r'\([^\)]+\)', '', ref)
                ref = ref.strip(' ')
                ref = re.sub(r'\s{2,}', ' ', ref)
                authors_formatted = []
                authors = re.split(r'\s*,\s*|\s+[и&]\s+', ref)
                for author in authors:
                    if re.search('[A-ZА-ЯЁ]\.(\s*[A-ZА-ЯЁ]\.)?', author):
                        init = re.search('[A-ZА-ЯЁ]\.(\s*[A-ZА-ЯЁ]\.)?', author).group(0)
                        author = author.replace(init, '').strip()
                        authors_formatted.append([author, init])
                    else:
                        authors_formatted.append([author])
                obj['authors'] = authors_formatted
                obj['tags'] = keywords
                for year in obj['years']:
                    m_obj = obj
                    m_obj['years'] = year
                    extracted_objects.append(m_obj)
            else:
                articles = re.findall(r'(?<=«)[^»]+', ref)
                authr = re.findall(r'(?<=\()[^\)]+', ref)
                authors = []
                for a in authr:
                    authors += re.split(r'\s*,\s*|\s+[и&]\s+', a)
                authors_formatted = []
                for author in authors:
                    if re.search('[A-ZА-ЯЁ]\.(\s*[A-ZА-ЯЁ]\.)?', author):
                        init = re.search('[A-ZА-ЯЁ]\.(\s*[A-ZА-ЯЁ]\.)?', author).group(0)
                        author = author.replace(init, '').strip()
                        authors_formatted.append([author, init])
                    else:
                        authors_formatted.append([author])
                for article in articles:
                    obj = dict()
                    obj['type'] = 'article,les'
                    obj['authors'] = authors_formatted
                    obj['name'] = article
                    obj['tags'] = keywords
                    extracted_objects.append(obj)

for obj in extracted_objects:
    code = ''
    if obj['type'] == 'book,whole':
        code += 'RT Book, Whole\n'
    elif obj['type'] == 'book,part':
        code += 'RT Book, Section\n'
    elif obj['type'] == 'article,les':
        code += 'RT Book, Section\n'
    for e, author in enumerate(obj['authors']):
        code += 'A' + str(e + 1) + ' ' + ', '.join(author) + '\n'
    if 'name' in obj:
        code += 'T1' + ' ' + obj['name'] + '\n'
    if obj['type'] == 'article,les':
        code += '\n'.join([
            'T2 Лингвистический энциклопедический словарь',
            'PP М.',
            'PB Сов. энциклопедия',
            'FD 1990',
            'YR 1990',
            'OP 683'
        ]) + '\n'
    if 'years' in obj:
        code += 'FD' + ' ' + obj['years'] + '\n'
        code += 'YR' + ' ' + obj['years'] + '\n'
    if 'pages' in obj:
        first, last = obj['pages'].split('-')
        code += 'SP {}'.format(first) + '\n'
        code += 'OP {}'.format(last) + '\n'
    for tag in obj['tags']:
        code += 'K1' + ' ' + tag + '\n'

    refworks_code += code + '\n'

    # PAGES INSERTION

with open('rwc.txt', 'w', encoding='utf-8') as rwc:
    rwc.write(refworks_code)
    rwc.close()