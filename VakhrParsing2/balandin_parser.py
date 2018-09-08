#!/usr/bin/python3

import is_russian
import muskrat
from muskrat.parser import *
from muskrat.allocator import *
from muskrat.filters import *
from muskrat.connectivity import Accept, Attach
import parser_client
import string


vakhr_alphabet = "АаӓәӛБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнӇӈОоӦӧӨөПпРрСсТтУуӰӱФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя’'°-."

dict_alph = [
    "Ааӓәӛ", "Бб", "Вв", "Гг", "Дд", "ЕеЁё", "Жж", "Зз", "Ии", "Йй", "Кк", "Лл", "Мм", "Нн", "Ӈӈ",
    "ОоӦӧӨө", "Пп", "Рр", "Сс", "Тт", "УуӰӱ", "Фф", "Хх", "Цц", "Чч", "Шш", "Щщ", "Ъъ", "Ыы", "Ьь", "Ээ", "Юю", "Яя"
]

checker = is_russian.Checker(import_op=False)


def here_or_btw(prev, char):
    return find_in_da(char) - find_in_da(prev) <= 1


def find_in_da(char):
    for j, da in enumerate(dict_alph):
        if char in da:
            return j
    return -1


def a_gt_b(a, b):
    punct = "’'°-." + string.punctuation
    for pct in punct:
        a = a.replace(pct, "")
        b = b.replace(pct, "")
    if len(a) == len(b) == 1 and a.lower() == b.lower():
        return False
    return a == sorted(
        [a, b], key=lambda word: [(vakhr_alphabet.index(c) if c in vakhr_alphabet else -1) for c in word]
    )[1]


def ngram_a_gt_b(a_ngram, b_ngram, a_next):
    if a_gt_b(a_ngram, b_ngram):
        return True
    for nxt in a_next:
        a_ngram += " " + nxt
        if a_gt_b(a_ngram, b_ngram):
            return True
    return False


class OptionEntitiesCompare:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @staticmethod
    def compare(a, b):
        return len(b) > 0.13 * len(a) * len(a)

    def connect(self):
        if not self.compare(self.a, self.b) or not self.compare(self.b, self.a):
            return self.a + self.b, True
        else:
            return self.a, False


def entry_title_norus_check(entry_title):
    if len(entry_title) >= 4:
        chars2check = ["ь"]
        for ch in chars2check:
            if ch in entry_title:
                cr = checker.check(entry_title)
                if cr:
                    return False
                break
    return True


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
            Accept().add_default(connect=True, insert=True).add_option(
                by_type("MeaningEntity"), connect=True, insert=False
            ),
            Attach().add_default(connect=False, insert=False).add_option(
                by_type("EntryTitle"), connect=False, insert=True
            ).add_option(
                by_type("EntryTitleComma"), connect=True, insert=False
            )
        )
        self.insertion_prepend_value = True


class EntryTitleTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = EntryTitle()
        self.extractor = CharString("-ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяёӇӈӓәӛӦӧӨөӰӱ")

    def track(self):
        try:
            if self.next().startswith("/"):
                return False

            if not entry_title_norus_check(self.current()):
                return False

            pe = self.parser.get(1)
            lb_tests = False  # ?
            if pe.pattern.object_type in ["MeaningEntity", "OptionEntity", "UsageExample", "OptionUsageExample"]:
                etp = self.parser.get(
                    1,
                    condition=lambda o: o.pattern.object_type == "EntryTitle" and not
                    o.pattern.properties.property_exists("after-comma")
                )
                cetp = len(etp.content.split()) - len(self.current().split())
                if not cetp:
                    return a_gt_b(self.current(), etp.content) and here_or_btw(etp.content[0], self.current()[0])
                else:
                    return ngram_a_gt_b(
                        self.current(), etp.content, [
                            self.next(k + 1) for k in range(cetp)
                            if re.search(r'[А-ЯЁа-яё]', self.next(k + 1))
                        ]
                    ) and here_or_btw(etp.content[0], self.current()[0])
            elif pe.pattern.object_type == "EntryTitleComma":
                self.pattern.properties = PatternProperties()
                self.pattern.properties.add_property('after-comma')
                return True
            elif pe.pattern.object_type in ["CharHeader"]:
                return True
            elif pe.pattern.object_type == "EntryTitle":
                try:
                    pt = self.parser.get(2, condition=lambda o: o.pattern.object_type == "EntryTitle")
                    pel = len(pe.content.split())
                    ptl = len(pt.content.split())
                    if pel > ptl:
                        return False
                    elif pel == ptl:
                        return pt.content == pe.content
                    else:
                        return a_gt_b(self.current(), pt.content.split()[pel - ptl])
                except AttributeError:
                    return False
            else:
                return False
        except AttributeError:
            return False


class EntryTitleComma(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "EntryTitleComma",
            Accept().add_default(connect=True, insert=False),
            Attach().add_default(connect=True, insert=False)
        )


class EntryTitleCommaTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = EntryTitleComma()
        self.extractor = CharSequenceString(",")

    def track(self):
        try:
            return self.parser.get(1).pattern.object_type == "EntryTitle"
        except AttributeError:
            return False


class AltTitle(Pattern):
    ...


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
        self.focus_on = lambda p, c: p.get(condition=lambda o: o.pattern.object_type == "EntryTitle")


class IndexMarkerTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = IndexMarker()
        self.extractor = RegexString(r'[IV]+')

    def track(self):
        try:
            return self.parser.get(1).pattern.object_type in ("EntryTitle", "CasualDot", "OptionUsageExample")
        except AttributeError:
            return False


et_im = ["EntryTitle", "IndexMarker"]


class LexMarker(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "LexMarker",
            Accept().add_default(connect=False, insert=False).add_option(
                by_type("MeaningEntity"), connect=True, insert=False
            ),
            Attach().add_default(connect=True, insert=False)
        )
        self.focus_on = lambda p, c: p.get(1, lambda o: o.pattern.object_type in et_im)


class LexMarkerTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = LexMarker()
        self.extractor = RegexString(
            r'(анатом|арифм|арх|глаг|грам|кого-л|кого-н|межд|политич|посл|прист|союз|част|что-л|что-н)\.?'
        )
        self.takes_all = True

    def track(self):
        try:
            if self.parser.get(1).pattern.object_type == "IndexMarker":
                self.pattern.properties.add_property("after-im")
        except AttributeError:
            pass
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
        self.insertion_prepend_value = True
        self.focus_on = lambda p, c: p.get(1, condition=lambda o: o.pattern.object_type in [
            "IndexMarker", "MeaningIndex", "LexMarker", "EntryTitle"
        ] and not o.pattern.properties.property_exists("after-im"))


class MeaningEntityTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = MeaningEntity()
        self.extractor = CharString("-ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяёӇӈӓәӛӦӧӨөӰӱ()")

    def track(self):
        try:
            pe = self.parser.get(1)
            if pe.pattern.object_type in [
                "LexMarker", "IndexMarker", "EntryTitle", "MeaningIndex", "MeaningEntity"
            ]:
                return True
            elif pe.pattern.object_type == "MeaningPunct":
                etp = self.parser.get(condition=lambda o: o.pattern.object_type == "EntryTitle")
                if etp.content[0].istitle():
                    return self.current()[0].istitle()
                else:
                    return not self.current()[0].istitle()
            else:
                return False
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
        self.extractor = CharString(
            "?!.,-()ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяёӇӈӓәӛӦӧӨөӰӱ—"
        )

    def track(self):
        try:
            pe = self.parser.get(1)
            if pe.pattern.object_type == "UsageExample":
                return True
            elif pe.pattern.object_type == "MeaningPunct":
                if pe.content == ",":
                    return False
                else:
                    return True
            else:
                return False
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
        char_string = r"'\-\.°ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяёӇӈӓәӛӦӧӨөӰӱ’"
        self.extractor = RegexString(r"/|[" + char_string + r"]+[°\*][" + char_string + r"]*")

    def track(self):
        if self.current()[0] != "/":
            try:
                pe = self.parser.get(1)
                if pe.pattern.object_type == "MeaningEntity":
                    self.pattern.properties = PatternProperties()
                    self.pattern.properties.add_property("is-entity")
                    self.pattern.properties.add_property("option-related")
                    return True
                else:
                    return False
            except AttributeError:
                return False
        else:
            return True


class OptionIndex(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "OptionIndex",
            Accept().add_default(connect=True, insert=False),
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
            Accept().add_default(connect=False, insert=False).add_option(
                muskrat.filters.by_type("OptionEntity"), connect=False, insert=True
            ),
            Attach().add_default(connect=True, insert=False).add_option(
                muskrat.filters.by_type("OptionEntity"), connect=False, insert=True
            ).add_option(
                muskrat.filters.by_type("OptionIndex"), connect=True, insert=False
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
            if self.parser.get(1).pattern.object_type == "OptionEntity":
            if self.parser.get(1).pattern.object_type == "OptionUsageExample":
                return False
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


class OptionUsageExample(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "OptionUsageExample",
            Accept().add_default(connect=False, insert=True),
            Attach().add_default(connect=True, insert=True),
            focus_on=lambda p, c: p.get(
                condition=lambda o: o.pattern.object_type in ["OptionSlash", "OptionIndex", "OptionUsageExample"]
            )
        )
        self.properties = PatternProperties()
        self.properties.add_property("option-related")
        self.insertion_prepend_value = True


class OptionUsageExampleTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = OptionUsageExample()
        self.extractor = CharString(
            "?!'-,.°()ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяёӇӈӓәӛӦӧӨөӰӱ’—"
        )

    def track(self):
        try:
            if self.parser.get(1).pattern.object_type == "OptionPunct" \
                    and self.parser.get(2).pattern.object_type == "OptionEntity" \
                    and self.current()[0].istitle() and not self.parser.get(2).content[0].istitle():
                return True
            elif self.parser.get(1).pattern.object_type == "OptionUsageExample":
                # should be sophisticated condition group (?)
                if re.search(r'[!\?\.]$', self.parser.get(1).content):
                    return False
                else:
                    return True
            else:
                return False
        except AttributeError:
            return False


class CasualChars(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "CasualChars",
            Accept().add_default(connect=False, insert=False),
            Attach().add_default(connect=False, insert=True)
        )
        self.insertion_prepend_value = True


class CasualCharsTr(Tracker):
    def __init__(self, *args):
        Tracker.__init__(self, *args)
        self.pattern = CasualChars()
        self.extractor = CharList(["—", "!"])

    def track(self):
        return True


client = parser_client.ParserClient()
use_client = False

parser = Parser()

if use_client:
    text = client.get_text()
    allocator = Allocator(text, WhitespaceVoid(), parser)
    allocator.end_position = client.end_position
    try:
        allocator.start()
    except muskrat.allocator.CannotMoveRight as parser_msg:
        tree = muskrat.txt_tree_generator.TXTTree(parser.objects)
        tree.build()
        print('===')
        print(parser_msg)
        print('===')
        client.scan_error(parser_msg, allocator.units, parser)
else:
    text = open('balandin_vakhr.txt', 'r', encoding='utf-8').read()
    text = text.replace("\ufeff", "")
    allocator = Allocator(text, WhitespaceVoid(), parser)
    allocator.end_position = 1500
    try:
        allocator.start()
    except muskrat.allocator.CannotMoveRight as parser_msg:
        tree = muskrat.txt_tree_generator.TXTTree(parser.objects)
        tree.build()
        print('===')
        print(parser_msg)
        print('===')
        print(allocator.units[-10:])

et_superior = TrackerBox(["EntryTitle", "OptionEntity"], {"EntryTitle": 0, "OptionEntity": 1})
allocator.tracker_boxes.append(et_superior)
#options_superior = TrackerBox(["OptionEntity"], {"OptionEntity": 0})
#allocator.tracker_boxes.append(options_superior)
#allocator.end_position = 840
#print(parser_msg)
#print(allocator.units[-10:])
#print(len(allocator.units))
#tree = muskrat.txt_tree_generator.TXTTree(parser.objects)
#tree.build()
tree = muskrat.txt_tree_generator.TXTTree(parser.objects)
tree.build()
