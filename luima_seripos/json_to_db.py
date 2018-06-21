#!/usr/bin/python3

import json
import os


downloaded = [fn for fn in os.listdir('./downloaded') if fn.endswith('.json')]

for j, d_file in enumerate(downloaded):
    dwl_json = json.loads(open('./downloaded/' + d_file).read())
    with open('./dwl_json_txt/' + d_file.replace('.json', '.txt'), 'w', encoding='utf-8') as djt:
        djt.write(dwl_json['text'])
        djt.close()
    print(j)
