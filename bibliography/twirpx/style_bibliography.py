#!/usr/bin/python3
import html.parser
import re

bibl = open('bibliography.txt').read()

with open('bibliography.txt', 'w') as bibl_output:
    bibl = re.sub('&[^;]+;', lambda m: html.parser.unescape(m.group(0)), bibl)
    bibl_output.write(bibl)
    bibl_output.close()