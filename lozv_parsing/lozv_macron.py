#!/usr/bin/python3

lozv_source = open('lozv.txt', encoding='utf-8').read()
with open('lozv_macronized.txt', 'a', encoding='utf-8') as lm:
    for j, char in enumerate(lozv_source):
        if j < len(lozv_source) - 1 and lozv_source[j + 1] == '#':
            lm.write(char + u"\u0304")
        elif char == '#':
            pass
        else:
            lm.write(char)
    lm.close()