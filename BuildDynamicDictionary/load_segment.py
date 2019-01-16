#!/usr/bin/python3

from collections import Counter
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
        self.pos_options = []
        self.rus_meanings = []
        self.common_pos = None

    def get_pos(self, update=False):
        if self.common_pos is not None and not update:
            return self.common_pos
        else:
            self.common_pos = Counter(self.pos_options).most_common(1)[0][0]
            return self.common_pos


dict_entries = []


def dump_dict_entries(file_path):
    all_json = []
    for entry in dict_entries:
        entry_json = {
            "lemma": entry.lemma,
            "rus_meanings": entry.rus_meanings,
            "pos_options": entry.pos_options
        }
        all_json.append(entry_json)
    with open(file_path, "w") as fp:
        fp.write(json.dumps(all_json))
        fp.close()


def load_dict_entries(file_path):
    entries_list = []
    loaded_entries = json.loads(open(file_path).read())
    for entry_ in loaded_entries:
        entries_list.append(WordEntry(entry_["lemma"]))
        entries_list[-1].rus_meanings = entry_["rus_meanings"]
        entries_list[-1].pos_options = entry_["pos_options"]
    return entries_list


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
        this_entry = WordEntry(entry.content)
        meanings = [[]]
        for e, obj in enumerate(prs.parser.objects):
            if obj.pattern.object_type == "MeaningLinear":
                formatted = lexic_parser.lexic_parser_functions.format_token(obj.content)
                ind_check = lexic_parser.lexic_parser_functions.is_independent(formatted)
                if ind_check:
                    if e == 0:
                        if type(ind_check) == tuple:
                            this_entry.pos_options.extend(ind_check[2])
                        elif len(formatted) < 3:
                            this_entry.pos_options.append(None)
                    meanings[-1].append(formatted)
            elif obj.pattern.object_type in ["CommaSeparator", "SemicolonSeparator"]:
                meanings.append([])
        if [] in meanings:
            meanings.remove([])
        this_entry.rus_meanings = meanings
        dict_entries.append(this_entry)
        print(meanings)

print()
