#!/usr/bin/python3
import json
import re


class ParserClient:
    def __init__(self):
        self.balandin_vakhr = open("balandin_vakhr.txt").read()
        self.parser_state = json.loads(open("parser_state.json").read())
        self.parsed_dictionary = json.loads(open("parsed_dictionary.json").read())
        self.start_char = self.parser_state["start_char"]
        self.end_position = self.parser_state["end_position"]
        self.default_ep_incr = 350
        self.default_ep_micro_incr = 40
        self.regex_identifier_length = 50

    def get_text(self):
        return self.balandin_vakhr[self.start_char:]

    def get_char_position(self, regex_identifier, tokens_back=0):
        ri_found = re.search(regex_identifier, self.balandin_vakhr).start()
        if tokens_back < 0:
            ri_found -= 1
            wsn_groups_count = -tokens_back
            wsn_checked = 0
            tkn_checked = 0
            inside_wsn = False
            inside_tkn = False
            while wsn_checked < wsn_groups_count and wsn_checked != tkn_checked:
                if self.balandin_vakhr[ri_found] in [" ", "\n"]:
                    if inside_tkn:
                        inside_tkn = False
                    if not inside_wsn:
                        wsn_checked += 1
                        inside_wsn = True
                else:
                    if inside_wsn:
                        inside_wsn = False
                    if not inside_tkn:
                        tkn_checked += 1
                        inside_tkn = True
                ri_found -= 1

        return ri_found

    def scan_error(self, parser_msg, allocator_units, parser):
        self.save_objects(parser.objects)
        unit_number = int(re.search(r"\d+", parser_msg).group(0))
        failed_sequence = allocator_units[unit_number:]
        regex_identifier = r"[\s\n]+".join([re.escape(unit) for unit in failed_sequence])
        if len(regex_identifier) < self.regex_identifier_length:
            self.end_position += self.default_ep_micro_incr
            self.update_parser_state()
        else:
            bool_cut_left, cut_index = self.prompt_cut()
            if not bool_cut_left:
                self.print_dev_message()
                self.force_reload()
            else:
                self.end_position = self.get_char_position(regex_identifier, cut_index)
                self.update_parser_state()

    def save_objects(self, objs):
        self.parsed_dictionary.append([
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
        if not result:
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

    @staticmethod
    def force_reload():
        print("-- Press (STOP->)RUN to continue --")
        raise Exception()
