#!/usr/bin/python3

import json
import os
import re


downloaded = [fn for fn in os.listdir('./downloaded') if fn.endswith('.json')]
write_txt = False

for j, d_file in enumerate(downloaded):
    dwl_json = json.loads(open('./downloaded/' + d_file).read())
    dwl_text = dwl_json['text']
    reg_corrections = {
        "": "А̄",
        "": "а̄",
        "": "Я̄",
        "": "я̄",
        "": "Е̄",
        "": "е̄",
        "": "Э̄",
        "": "э̄",
        "": "О̄",
        "": "о̄",
        "": "Ю̄",
        "": "ю̄",
        "": "Ы̄",
        "": "ы̄",
        "": "Ё̄",
        "": "ё̄"
    }
    for fr in reg_corrections:
        dwl_text = dwl_text.replace(fr, reg_corrections[fr])

    dwl_text = re.sub(r'(.[\.:,!\?—])([^\d\s\t\n\.:,!\?—»"])', '\g<1> \g<2>', dwl_text)
    dwl_text = re.sub(r'\s+([\.,!\?])', '\g<1>', dwl_text)
    dwl_text = re.sub(r'([а-яёӈӣӯ])([А-ЯЁӇӢӮ])', '\g<1> \g<2>', dwl_text)
    dwl_text = re.sub(r'([А-Яа-яЁӇӢӮёӈӣӯ])(\d)', '\g<1> \g<2>', dwl_text)
    dwl_text = re.sub(r'”([А-Яа-яЁӇӢӮёӈӣӯ])', '” \g<1>', dwl_text)

    if not write_txt:
        new_json = {
            "title": dwl_json["title"],
            "url": dwl_json["url"],
            "content": {
                "correct": [dwl_text],
                "defective": []
            }
        }
        print('Saving new JSON of %s (%d/%d)...' % (d_file, j + 1, len(downloaded)))
        with open('./db_json/' + d_file, 'w') as njf:
            njf.write(json.dumps(new_json))
            njf.close()
    else:
        print('Saving text of %s (%d/%d)...' % (d_file, j + 1, len(downloaded)))
        with open('./dwl_json_txt/' + d_file.replace('json', 'txt'), 'w', encoding='utf-8') as txt:
            txt.write(dwl_text)
            txt.close()

