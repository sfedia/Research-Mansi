#!/usr/bin/python3
import os
import re
from random import shuffle

sources = [x for x in os.listdir('.') if re.search('^[^-]+-((small|big)-)?\d+$', x)]

shuffle(sources)

symbols_per_sample = 15
times_repeat = len(sources) // symbols_per_sample + 1
file_postfix_from = 0

i = 0
while i < times_repeat:
    query = " ".join(['"{}"'.format(x) for x in sources[15*i : 15*(i+1)]])
    os.system('montage {0} -tile 15x1 -geometry +0+0 samples/generated{1}.png'.format(query, file_postfix_from))
    i += 1
    file_postfix_from += 1


