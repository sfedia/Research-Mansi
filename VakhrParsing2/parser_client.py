#!/usr/bin/python3
import json
import re


class ParserClient:
    def __init__(self):
        self.balandin_vakhr = open('balandin_vakhr.txt', 'r', encoding='utf-8').read()
        self.balandin_vakhr = self.balandin_vakhr.replace("\ufeff", "")
        self.bv_length = len(self.balandin_vakhr)
        self.parser_state = json.loads(open("parser_state.json").read())
        self.parsed_dictionary = json.loads(open("parsed_dictionary.json").read())
        self.start_char = self.parser_state["start_char"]
        self.end_position = self.parser_state["end_position"]
        self.default_ep_incr = 350
        self.default_ep_micro_incr = 40
        self.regex_identifier_length = 50

    def get_text(self):
        text = ("А\n" if self.start_char else "") + self.balandin_vakhr[self.start_char:]
        print("-->", text[:20])
        print("===")
        return text

    def get_char_position(self, regex_identifier, tokens_back=0):
        ri_found = re.search(regex_identifier, self.balandin_vakhr).start()
        if not tokens_back:
            return ri_found
        index_minus = 20
        rim = ri_found - index_minus
        while rim > 0 and len(re.split(r'[\n\s]', self.balandin_vakhr[rim:ri_found])) < -tokens_back \
                and self.balandin_vakhr[rim-1] in [" ", "\n"]:
            rim -= index_minus
        field = self.balandin_vakhr[rim:ri_found]
        tokens = field.split()
        return re.search(re.escape(tokens[tokens_back]), field).start() + rim

    def scan_error(self, parser_msg, allocator_units, parser):
        self.save_objects(parser.objects)
        unit_number = int(re.search(r"\d+", str(parser_msg)).group(0))
        print("Next:", " ".join(allocator_units[unit_number:][:10]))
        print("===")
        failed_sequence = allocator_units[unit_number:]
        regex_identifier = r"[\s\n]+".join([re.escape(unit) for unit in failed_sequence])
        if len(regex_identifier) < self.regex_identifier_length:
            self.end_position += self.default_ep_micro_incr
            self.update_parser_state()
            self.force_reload()
        else:
            bool_cut_left, cut_index = self.prompt_cut()
            if not bool_cut_left:
                self.print_dev_message()
                self.force_reload()
            else:
                self.start_char = self.get_char_position(regex_identifier, cut_index)
                self.end_position += self.default_ep_incr
                self.update_parser_state()
                self.force_reload()

    def json_parsing_object(self, parsing_object):
        return {
            "content": parsing_object.content,
            "properties": parsing_object.pattern.properties.dict_properties(None),
            "childs": [self.json_parsing_object(o) for o in parsing_object.connected_objects]
        }

    def save_objects(self, parsed_objects):
        objs = [self.json_parsing_object(o) for o in parsed_objects]
        self.parsed_dictionary["objects"].append([
            self.start_char,
            self.end_position,
            objs
        ])
        with open("parsed_dictionary.json", "w") as pd:
            pd.write(json.dumps(self.parsed_dictionary))
            pd.close()

    @staticmethod
    def prompt_cut():
        result = input("Can we cut out the left side? [Y(INT=0)/(int<0)/n]:")
        if not result or result == "y":
            return True, 0
        elif result == "n":
            return False, None
        else:
            return True, int(result)

    def update_parser_state(self):
        self.parser_state["start_char"] = self.start_char
        self.parser_state["end_position"] = self.end_position
        with open("parser_state.json", "w") as ps_json:
            ps_json.write(json.dumps(self.parser_state))
            ps_json.close()

    @staticmethod
    def print_dev_message():
        print("- Stopped for development -")

    def force_reload(self):
        print(
            "Characters processed: %d/%d (%d%%)" % (
                self.end_position, self.bv_length, self.end_position / self.bv_length * 100
            )
        )
        print("-- Press (STOP->)RUN to continue --")
        #raise Exception()
