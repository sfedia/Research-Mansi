#!/usr/bin/python3
import json
import re

struct = json.loads(open('results.txt').read())

with open('bibliography.txt', 'a') as bibl:
    for link in struct:
        template = '''Название: {0}
        Метаданные: {1}
        Найденные источники для скачивания: {2}'''
        name = struct[link][0]
        source = 'http://www.twirpx.com' + link
        if len(struct[link]) == 1:
            metadata = ''
        else:
            metadata = re.split(r'\.(?=[А-ЯЁа-яё])', struct[link][1])[0] + '.'
        bibl.write('\n\n\n' + template.format(name, metadata, source))
    bibl.close()