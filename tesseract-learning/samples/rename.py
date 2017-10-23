#!/usr/bin/python3
import re
import os

files = os.listdir('.')
for f in files:
    if re.search('\.\d', f):
        new_f = re.sub('\.(?=\d)', '.exp', f)
        os.system('mv %s %s' % (f, new_f))
