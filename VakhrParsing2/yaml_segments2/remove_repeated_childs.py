#!/usr/bin/python3

import re


class GetSegment:
    def __init__(self, n_yaml):
        self.yaml_file = open("./segment_%d.yaml" % n_yaml, encoding="utf-8").read()
        self.yaml_new = []
        self.childs_init = list()
        for line in self.yaml_file.splitlines():
            result_on_line = self.process_line(line)
            if result_on_line:
                self.yaml_new.append(line)

    def process_line(self, line):
        ws_left = len(re.search(r'^\s*', line).group(0))
        if re.search(r'^\s*childs:\s*$', line):
            if ws_left not in self.childs_init:
                self.childs_init.append(ws_left)
                return True
            else:
                return False
        elif (ws_left + 2) in self.childs_init and line[ws_left + 2:].startswith("- type"):
            self.childs_init.remove(ws_left + 2)
        return True


