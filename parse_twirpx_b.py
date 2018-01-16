#!/usr/bin/python3
import re

twirpx_b = open('bibliography/twirpx_bibliography.txt', encoding='utf-8').read().splitlines()

biblio_src = []
biblio_parsed = []

for i, line in enumerate(twirpx_b):
    if line.startswith('Название:'):
        if len(biblio_src):
            parsed_object = {}
            biblio_src[-1]['name'] = re.sub(r'\s*\([а-яё]+\.\)', '', biblio_src[-1]['name'])
            biblio_src[-1]['name'] = biblio_src[-1]['name'].replace('Название:', '').strip()
            authors_rx = r'(([А-ЯЁ][а-яё]+\s+[А-ЯЁ]\.\s*[А-ЯЁ]\.)(,\s*)?)+'
            author_search = re.search(authors_rx, biblio_src[-1]['name'])
            author_list = []
            if author_search:
                authors = author_search.group(0)
                biblio_src[-1]['name'] = re.sub(authors_rx + r'\.?\s*', '', biblio_src[-1]['name'])
                authors = re.split(r'\s*,\s*', authors)
                for author in authors:
                    surname = re.search(r'^[А-ЯЁ][^\s]+', author).group(0)
                    first_name = re.search(r'[А-ЯЁ]\.\s*[А-ЯЁ]\.', author).group(0)
                    author_list.append([surname, first_name])
            title = biblio_src[-1]['name']
            # metadata
            metadata = biblio_src[-1]['metadata']
            pc_search = re.search(r'(\d+)(,|\[\d+\])*\s*(с(тр)?\.?)', metadata)
            pages_count = None
            if pc_search:
                pages_count = pc_search.group(0)
            sp_search = re.search(r'[Cс](тр)?\.?\s*((\d+[,-]?)+)', metadata)
            selected_pages = None
            if sp_search:
                selected_pages = sp_search.group(0)
            year_search = re.search(r'(20|1[89]).{2}', metadata)
            year = None
            if year_search:
                year = year_search.group(0)

        biblio_src.append({})
        biblio_src[-1]['name'] = line
    elif line.startswith('Метаданные:'):
        biblio_src[-1]['metadata'] = line
    elif line.startswith('Найденные'):
        biblio_src[-1]['source'] = line

print()