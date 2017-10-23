#!/usr/bin/python3
import re
import os
query = 'unicharset_extractor '
files = ['mns.unknfa.exp' + str(i) + '.box' for i in range(17)]
query += ' '.join(files)

os.system(query)
