#!/usr/bin/python3

import muskrat
from muskrat.parser import *
from muskrat.allocator import *
from muskrat.connectivity import Accept, Attach


parser = Parser()

text = open('balandin_vakhr.txt', 'r', encoding='utf-8').read()
text = text.replace("\ufeff", "")

allocator = Allocator(text, WhitespaceVoid(), parser)
allocator.end_position = 20


class CharHeader(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "CharHeader",
            Accept().add_default(connect=False, insert=False),
            Attach().add_default(connect=False, insert=False)
        )


class CharHeaderTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = CharHeader()
        self.extractor = RegexString(r'[А-ЯЁ]')
        self.takes_all = True

    def track(self):
        return True


try:
    allocator.start()
except muskrat.allocator.CannotMoveRight:
    print(allocator.units[-10:])

tree = muskrat.txt_tree_generator.TXTTree(parser.objects)
tree.build()


