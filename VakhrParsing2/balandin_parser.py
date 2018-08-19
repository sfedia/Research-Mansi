#!/usr/bin/python3

import is_russian
import muskrat
from muskrat.parser import *
from muskrat.allocator import *
from muskrat.connectivity import Accept, Attach


parser = Parser()

text = open('balandin_vakhr.txt', 'r', encoding='utf-8').read()
text = text.replace("\ufeff", "")

allocator = Allocator(text, WhitespaceVoid(), parser)
allocator.end_position = 60


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
        try:
            return self.parser.get(1).pattern.object_type != "UsageExample"
        except AttributeError:
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
        self.focus_on = lambda p, c: p.get(condition=lambda o: o.pattern.object_type in ["IndexMarker", "EntryTitle"])


class MeaningIndexTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = MeaningIndex()
        self.extractor = RegexString(r'\d\.?')

    def track(self):
        try:
            return not self.parser.get(1).pattern.properties.property_exists("option-related")
        except AttributeError:
            return True


class MeaningEntity(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "MeaningEntity",
            Accept().add_default(
                connect=False, insert=False
            ).add_option(
                muskrat.filters.by_type("MeaningEntity"), connect=False, insert=True
            ).add_option(
                LogicalOR(muskrat.filters.by_type("UsageExample"), muskrat.filters.by_type("MeaningPunct")),
                connect=True, insert=False
            ),
            Attach().add_default(connect=True, insert=True)  # insert=True?
        )


class MeaningEntityTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = MeaningEntity()
        self.extractor = CharString("-ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяёӇӈӓәӛӦӧӨөӰӱ")

    def track(self):
        try:
            return self.parser.get(1).pattern.object_type in ("LexMarker", "IndexMarker", "EntryTitle", "MeaningIndex")
        except AttributeError:
            return False


class MeaningPunct(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "MeaningPunct",
            Accept().add_default(connect=False, insert=False),
            Attach().add_default(connect=True, insert=False)
        )


class MeaningPunctTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = MeaningPunct()
        self.extractor = CharString(";,")

    def track(self):
        try:
            return self.parser.get(1).pattern.object_type == "MeaningEntity"
        except AttributeError:
            return False


class UsageExample(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "UsageExample",
            Accept().add_default(connect=False, insert=True),
            Attach().add_default(connect=True, insert=True)
        )
        self.focus_on = lambda p, c: p.get(
            condition=lambda o: o.pattern.object_type in ["MeaningEntity", "UsageExample"]
        )
        self.insertion_prepend_value = True


class UsageExampleTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = UsageExample()
        self.extractor = CharString("?!.-ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяёӇӈӓәӛӦӧӨөӰӱ")

    def track(self):
        try:
            return self.parser.get(1).pattern.object_type in ["MeaningPunct", "UsageExample"]
        except AttributeError:
            return False


class OptionSlash(Pattern):
    def __init__(self):
        pp = PatternProperties()
        pp.add_property("option-related")
        Pattern.__init__(
            self,
            "OptionSlash",
            Accept().add_default(connect=True, insert=False),
            Attach().add_default(connect=True, insert=False),
            properties=pp
        )
        self.focus_on = lambda p, c: p.get(condition=lambda o: o.pattern.object_type in ["IndexMarker", "EntryTitle"])


class OptionSlashTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = OptionSlash()
        self.extractor = CharSequenceString("/")

    def track(self):
        return True


class OptionIndex(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "OptionIndex",
            Accept().add_default(connect=False, insert=False),
            Attach().add_default(connect=True, insert=False)
        )
        self.focus_on = lambda p, c: p.get(condition=lambda o: o.pattern.object_type == "OptionSlash")
        self.properties = PatternProperties()
        self.properties.add_property("option-related")


def option_related(psr):
    return psr.get(1).pattern.properties.property_exists("option-related")


class OptionIndexTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = OptionIndex()
        self.extractor = RegexString(r"\d\.?")

    def track(self):
        try:
            return option_related(self.parser)
        except AttributeError:
            return False


class OptionEntity(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "OptionEntity",
            Accept().add_default(connect=False, insert=True),
            Attach().add_default(connect=True, insert=False).add_option(
                muskrat.filters.by_type("OptionEntity"), connect=False, insert=True
            ),
            focus_on=lambda p, c: p.get(condition=lambda o: o.pattern.object_type in ["OptionIndex", "OptionSlash"])
        )
        self.properties = PatternProperties()
        self.properties.add_property("option-related")


class OptionEntityTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = OptionEntity()
        self.extractor = CharString(
            "'-.°ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяёӇӈӓәӛӦӧӨөӰӱ’"
        )

    def track(self):
        try:
            if not option_related(self.parser):
                return False
            if self.parser.get(1).pattern.object_type == "OptionPunct" \
                    and self.parser.get(2).pattern.object_type == "OptionEntity":
                if self.current()[0].istitle() and not self.parser.get(2).content[0].istitle():
                    return False
                return True
            return True
        except AttributeError:
            return False


class OptionPunct(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "OptionPunct",
            Accept().add_default(connect=False, insert=False),
            Attach().add_default(connect=True, insert=False),
            focus_on=lambda p, c: p.get(condition=lambda o: o.pattern.object_type in ["OptionIndex", "OptionSlash"])
        )
        self.properties = PatternProperties()
        self.properties.add_property("option-related")


class OptionPunctTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = OptionPunct()
        self.extractor = CharString(";,")

    def track(self):
        try:
            return option_related(self.parser)
        except AttributeError:
            return False


try:
    allocator.start()
except muskrat.allocator.CannotMoveRight:
    print(allocator.units[-10:])

tree = muskrat.txt_tree_generator.TXTTree(parser.objects)
tree.build()
