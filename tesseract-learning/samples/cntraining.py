#!/usr/bin/python3
import re
import os
query = 'cntraining '
ex = [7]
files = [ \
'mns.unknfa.exp' + str(i) + '.tr' for i in range(17) if i not in ex \
]
query += ' '.join(files)

os.system(query)
