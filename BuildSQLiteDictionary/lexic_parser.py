#!/usr/bin/python3

import muskrat
from muskrat.parser import *
from muskrat.allocator import *
from muskrat.connectivity import Accept, Attach
from muskrat.xml_generator import *


def format_token(token):
    return token


def is_independent(token):
    return True


class LexicTracker(Tracker):
    def __init__(self, *args):
        super().__init__(*args)


class MeaningLinear(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "MeaningLinear",
            Accept().add_default(connect=False, insert=False).add_option(
                by_type("MeaningLinear"), connect=False, insert=True
            ).add_option(
                by_type("LexicalCommentary"), connect=True, insert=False
            ),
            Attach().add_default(connect=False, insert=False).add_option(
                by_type("MeaningLinear"), connect=False, insert=True
            )
        )


class MeaningLinearTr(LexicTracker):
    def __init__(self, *args):
        super().__init__(*args)
        self.pattern = MeaningLinear()
        self.extractor = RegexString(r'[^,;\(\)]+')

    def track(self):
        this = re.search(r'^[^,;\(\)]+', self.current()).group(0)
        indep = is_independent(this)
        if not indep:
            self.pattern.properties.add_property("non-independent")

        try:
            pe = self.parser.get(1)
            if pe.pattern.object_type == "MeaningLinear":
                if not pe.pattern.properties.property_exists("non-independent"):
                    self.pattern.insertion_prepend_value = True
                    self.pattern.prepended_value = " "
        except AttributeError:
            pass

        return True


class LexicalCommentary(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "LexicalCommentary",
            Accept().add_default(connect=False, insert=False),
            Attach().add_default(connect=False, insert=False).add_option(
                by_type("MeaningLinear"), connect=True, insert=False
            )
        )


class LexicalCommentaryTr(LexicTracker):
    def __init__(self, *args):
        super().__init__(*args)
        self.pattern = LexicalCommentary()
        self.extractor = CharSequenceString("(")

    def track(self):
        return re.search(r'^\([^\)]+\)', self.current()) is not None


class LexicalCommentaryStop(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "LexicalCommentaryStop",
            Accept().add_default(connect=False, insert=False),
            Attach().add_default(connect=False, insert=False)
        )


class LexicalCommentaryStopTr(LexicTracker):
    def __init__(self, *args):
        super().__init__(*args)
        self.pattern = LexicalCommentaryStop()
        self.extractor = CharSequenceString(")")

    def track(self):
        return True


class CommaSeparator(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "CommaSeparator",
            Accept().add_default(connect=False, insert=False),
            Attach().add_default(connect=False, insert=False)
        )


class CommaSeparatorTr(LexicTracker):
    def __init__(self, *args):
        super().__init__(*args)
        self.pattern = CommaSeparator()
        self.extractor = CharSequenceString(",")

    def track(self):
        return True


class SemicolonSeparator(Pattern):
    def __init__(self):
        Pattern.__init__(
            self,
            "SemicolonSeparator",
            Accept().add_default(connect=False, insert=False),
            Attach().add_default(connect=False, insert=False)
        )


class SemicolonSeparatorTr(LexicTracker):
    def __init__(self, *args):
        super().__init__(*args)
        self.pattern = SemicolonSeparator()
        self.extractor = CharSequenceString(",")

    def track(self):
        return True


class LexicParser:
    def __init__(self, parse_string):
        self.parser = Parser()
        self.lexic_allocator = Allocator(parse_string, NullVoid(), self.parser)
        self.lexic_allocator.cursor.tracker_family = [LexicTracker]
        self.lexic_allocator.cursor.add_dynamic_mapper(
            start_if=lambda p, c: p.get(1).pattern.object_type == "LexicalCommentary",
            finalize_if=lambda p, c: p.get(1).pattern.object_type == "LexicalCommentaryStop",
            depend_on=lambda p, c: p.get(1),
            left_depth_limit=1
        )
