#!/usr/bin/python3
import os

for i in range(17):
    os.system(
    'tesseract mns.unknfa.exp{0}.png mns.unknfa.exp{0} box.train'.format(
        i
    ))
