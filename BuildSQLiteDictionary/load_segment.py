#!/usr/bin/python3

import json
import muskrat
from muskrat.parser import *
from muskrat.allocator import *
from muskrat.connectivity import Accept, Attach
from muskrat.xml_generator import *


class LoadedSegment:
    def __init__(self, index):
        self.json_segment = open("../VakhrParsing2/json_segments2/segment_%d.json" % index).read()
        self.json_segment = json.loads(self.json_segment)
        self.parser_objects = [
            self.generate_object(jd) for jd in self.json_segment if jd["type"] == "EntryTitle"
        ]

    def generate_object(self, json_dict):
        props = PatternProperties()
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
                obj.connected_objects.append(self.generate_object(child))
        else:
            obj.connected_objects = []
        return obj


segment1 = LoadedSegment(0)
for entry in segment1.parser_objects:
    print(entry.content)
    try:
        this_parser = XMLQuery(entry.connected_objects)
    except TypeError:
        print("failed")
        continue
    mobs = this_parser.root.xpath("//object[@type='MeaningEntity' or @type='MeaningPunct']")
    print([o.get("content") for o in mobs])
