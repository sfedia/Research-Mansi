#!/usr/bin/python3
import os, re

for l in os.listdir('.'):
    if not re.search('tiff', l):
        continue
    os.system('mv {0} {1}'.format(l, l.replace('.png.', '.')))
