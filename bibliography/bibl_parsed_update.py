#!/usr/bin/python3
import re

rwc = open('rwc.txt', encoding='utf-8').read()
bibl_parsed = open('bibl_parsed.txt', encoding='utf-8').read()[2:]
refs = rwc.split('\n\n')
parsed_refs = bibl_parsed.split('\n\n\n\n')
skip_refs = []
refs_struct = []

for e, reference in enumerate(parsed_refs):
    ref_s = reference.splitlines()
    letter = [x[2] for x in ref_s if x.startswith('#')]
    letter = letter[0] if len(letter) > 0 else None
    year = [x.split()[1] for x in ref_s if x.startswith('YR')]
    year = year[0] if len(year) > 0 else None
    authors = []
    for author in [x for x in ref_s if re.search('^A(1|2)', x)]:
        author = re.sub(r'\s*,.*', '', author.split(' ', 1)[1])
        authors.append(author)
    refs_struct.append([authors, year, letter])


with open('new_ref.txt', 'a', encoding='utf-8') as n_r:
    found = 0
    for i, ref in enumerate(refs):
        print(i)
        ref_string = ref
        ref_string = re.sub(r'\n#.*', '', ref_string)
        if 'PB Сов. энциклопедия' in ref_string:
            n_r.write('\n\n\n' + ref_string)
            continue
        ref = ref.splitlines()
        ref_author = None
        ref_year = None
        ref_letter = None
        ref_tags = []
        for section in ref:
            if section.startswith('A1'):
                author = section.split(' ', 1)[1]
                author = re.sub(r'\s*et\s*al\..*', '', author)
                author = re.sub(r',.*', '', author)
                ref_author = author
            elif section.startswith('YR'):
                year = section.split(' ', 1)[1]
                if re.search(r'[a-z]$', year):
                    ref_letter = re.search(r'[a-z]$', year).group(0)
                    year = re.sub(r'[a-z]$', '', year)
                ref_year = year
            elif section.startswith('K1'):
                ref_tags.append(section)

        found_ref = False
        for e, reference in enumerate(refs_struct):
            if e in skip_refs:
                continue
            if not refs_struct[e][0]:
                continue
            if refs_struct[e][1] and ref_author in refs_struct[e][0] and refs_struct[e][1] == ref_year:
                if ref_letter is None or \
                        (ref_letter is not None and refs_struct[e][2] is not None and ref_letter == refs_struct[e][2]):
                    new_ref = parsed_refs[e] + '\n' + '\n'.join(ref_tags)
                    n_r.write('\n\n\n' + new_ref)
                    found_ref = True
                    skip_refs.append(e)
                    found += 1
                    break
        if not found_ref:
            n_r.write('\n\n\n' + ref_string)
    n_r.close()

print()
print()
print(found)