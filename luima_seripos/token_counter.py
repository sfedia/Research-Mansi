#!/usr/bin/python3

import json
import os


dbj_files = os.listdir('db_json')

good_tokens = 0
uncrt_tokens = 0

for f in dbj_files:
    jf = json.loads(open('db_json/' + f).read())
    print('File:', 'db_json/' + f)
    try:
        good_length = sum([len(x.split()) for x in jf["content"]["good"] if x])
    except KeyError:
        good_length = sum([len(x.split()) for x in jf["content"]["correct"] if x])
    try:
        uncrt_length = sum([len(x[1].split()) for x in jf["content"]["uncertain"] if x and x[1]])
    except KeyError:
        uncrt_length = sum([len(x[1].split()) for x in jf["content"]["defective"] if x and x[1]])

    good_tokens += good_length
    uncrt_tokens += uncrt_length
    print(good_length, uncrt_length)

print('Good:', good_tokens, 'Defective:', uncrt_tokens, '[Sum]:', good_tokens + uncrt_tokens)