#!/usr/bin/python3

import re


class GetSegment:
    def __init__(self, n_yaml):
        self.n_yaml = n_yaml
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
        elif self.childs_init:
            right_wsed = min(self.childs_init, key=lambda v: abs(v - ws_left - 2))
            if right_wsed >= ws_left + 2 and line[ws_left:].startswith("- type"):
                self.childs_init.remove(right_wsed)
        return True

    def write_to_file(self):
        with open("./segment_%d_o.yaml" % self.n_yaml, "w", encoding="utf-8") as seg_n:
            seg_n.write("\n".join(self.yaml_new))
            seg_n.close()


for n in range(8 + 1):
    segment_n = GetSegment(n)
    segment_n.write_to_file()
