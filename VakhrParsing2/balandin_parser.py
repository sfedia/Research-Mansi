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


class EntryTitle(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "EntryTitle",
            Accept().add_default(connect=True, insert=True),
            Attach().add_default(connect=False, insert=False)
        )


class EntryTitleTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = EntryTitle()
        self.extractor = CharString("-ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяёӇӈӓәӛӦӧӨөӰӱ")

    def track(self):
        prev_title = self.parser.get(1, lambda o: o.pattern.object_type == "EntryTitle")
        if not prev_title:
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


class IndexMarker(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "IndexMarker",
            Accept().add_default(connect=True, insert=False),
            Attach().add_option(
                muskrat.filters.by_type("EntryTitle"), connect=True, insert=False
            ).add_default(connect=False, insert=False)
        )


class IndexMarkerTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = IndexMarker()
        self.extractor = RegexString(r'[IV]+')

    def track(self):
        try:
            return self.parser.get(1).pattern.object_type in ("EntryTitle", "CasualDot")
        except AttributeError:
            return False


et_im = ["EntryTitle", "IndexMarker"]


class LexMarker(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "LexMarker",
            Accept().add_default(connect=False, insert=False),
            Attach().add_default(connect=True, insert=False)
        )
        self.focus_on = lambda p, c: p.get(1, lambda o: o.pattern.object_type in et_im)


class LexMarkerTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = LexMarker()
        self.extractor = RegexString(
            r'(анатом|арифм|арх|глаг|грам|кого-л|кого-н|межд|политич|посл|прист|част|что-л|что-н)\.?'
        )
        self.takes_all = True

    def track(self):
        return True


class MeaningIndex(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "MeaningIndex",
            Accept().add_default(connect=True, insert=False),
            Attach().add_default(connect=True, insert=False)
        )


class MeaningIndexTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = MeaningIndex()
        self.extractor = RegexString(r'\d\.?')

    def track(self):
        self.parser.get(1).pattern.object_type in [""]


try:
    allocator.start()
except muskrat.allocator.CannotMoveRight:
    print(allocator.units[-10:])

tree = muskrat.txt_tree_generator.TXTTree(parser.objects)
tree.build()


