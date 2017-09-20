#!/usr/bin/python3
import os, re
l = os.listdir('.')
for file in l:
    if not re.search('gen', file):
        continue

    os.system('mv {0} {1}'.format(file, file.replace('generated', 'mns.unknfa.').replace('.png', '')))
