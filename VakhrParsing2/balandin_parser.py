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


mistakes = {
    'ӓ': ['а'],
    'ӱ': ['у'],
    'й': ['и', 'й'],
    'ӧ': ['о'],
    'ё': ['е', 'ё'],
    'б': ['б', 'о'],
    'к': ['к', 'а']
}


def get_alternatives(s):
    stack = [s]
    length = len(s)
    i = 0

    while i < length:
        new_stack = []
        for st in stack:
            if st[i] in mistakes:
                for replacement in mistakes[st[i]]:
                    new_stack.append(''.join([x if j != i else replacement for j, x in enumerate(list(st))]))
        if new_stack:
            stack = new_stack
        i += 1
    return stack


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


class CasualDot(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "CasualDot",
            Accept().add_default(connect=False, insert=False),
            Attach().add_default(connect=True, insert=False)
        )


class CasualDotTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = CasualDot()
        self.extractor = CharSequenceString('.')

    def track(self):
        try:
            return self.parser.get(1).pattern.object_type == "EntryTitle"
        except AttributeError:
            return False


try:
    allocator.start()
except muskrat.allocator.CannotMoveRight:
    print(allocator.units[-10:])

tree = muskrat.txt_tree_generator.TXTTree(parser.objects)
tree.build()


