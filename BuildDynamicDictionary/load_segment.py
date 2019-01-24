#!/usr/bin/python3

from collections import Counter
import datrie
import json
import BuildDynamicDictionary.lexic_parser as lexic_parser
import muskrat
from muskrat.parser import *
from muskrat.allocator import *
from muskrat.connectivity import Accept, Attach
from muskrat.xml_generator import *


class ObjectGenFailed(Exception):
    pass


class LoadedSegment:
    def __init__(self, index):
        self.json_segment = open("../VakhrParsing2/json_segments2/segment_%d.json" % index).read()
        self.json_segment = json.loads(self.json_segment)
        self.parser_objects = [
            self.generate_object(jd) for jd in self.json_segment if jd["type"] == "EntryTitle"
        ]

    def generate_object(self, json_dict):
        if "content" not in json_dict:
            raise ObjectGenFailed()
        props = PatternProperties()
        if "properties" in json_dict:
            for (p, v) in json_dict["properties"].items():
                props.add_property(p, v)
        obj = ParsingObject(
            json_dict["content"],
            Pattern(
                json_dict["type"],
                Accept().add_default(),
                Attach().add_default(),
                properties=props
            )
        )
        if "childs" in json_dict and json_dict["childs"] is not None:
            for child in json_dict["childs"]:
                try:
                    obj.connected_objects.append(self.generate_object(child))
                except ObjectGenFailed:
                    pass
        else:
            obj.connected_objects = []
        return obj


class WordEntry:
    def __init__(self, lemma):
        self.lemma = lemma
        self.full_lemma = lemma
        self.reduce_lemma()
        self.pos_options = []
        self.rus_meanings = []
        self.common_pos = None

    def reduce_lemma(self):
        self.lemma = re.sub(r'[ёуеыаоэяию]ӈкве$', '', self.lemma)

    def dynamic_lemma(self, wf):
        if wf.endswith("ь"):
            return self.full_lemma
        return self.lemma

    def get_pos(self, update=False):
        if self.common_pos is not None and not update:
            return self.common_pos
        else:
            self.common_pos = Counter(self.pos_options).most_common(1)[0][0]
            return self.common_pos


dict_entries = datrie.Trie(ranges=[(u'\u0410', u'\u044f'), (u'\u0020', u'\u002f')])


for n in range(9):
    segment1 = LoadedSegment(n)
    for entry in segment1.parser_objects:
        try:
            this_parser = XMLQuery(entry.connected_objects)
        except TypeError:
            continue
        mobs = this_parser.root.xpath("//object[@type='MeaningEntity' or @type='MeaningPunct']")
        ws_result = " ".join([o.get("content") for o in mobs])
        prs = lexic_parser.LexicParser(ws_result)
        try:
            prs.lexic_allocator.start()
        except CannotMoveRight:
            pass
        except TypeError:
            pass
        this_entry = WordEntry(entry.content)
        meanings = [[]]
        first = True
        for e, obj in enumerate(prs.parser.objects):
            if obj.pattern.object_type == "MeaningLinear":
                print('ft:', obj.content)
                formatted = lexic_parser.lexic_parser_functions.format_token(obj.content)
                ind_check = lexic_parser.lexic_parser_functions.is_independent(formatted)
                if ind_check:
                    if first:
                        if type(ind_check) == tuple:
                            this_entry.pos_options.extend(ind_check[2])
                        elif len(formatted) < 3:
                            this_entry.pos_options.append(None)
                        first = False
                    meanings[-1].append(formatted)
            elif obj.pattern.object_type in ["CommaSeparator", "SemicolonSeparator"]:
                meanings.append([])
                first = True
        meanings = [m for m in meanings if m != []]
        this_entry.rus_meanings = meanings
        dict_entries[this_entry.lemma] = this_entry
        print(meanings)

dict_entries.save('dict_entries.trie')
print()
