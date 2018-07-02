#!/usr/bin/python3


class Dictionary:
    def __init__(self):
        self.independent_objects = []

    def get(self, index=0):
        counter = 0
        for obj in reversed(self.independent_objects):
            if obj.connected_objects:
                if counter == index:
                    return obj.connected_objects[-1]
                else:
                    counter += 1
            else:
                if counter == index:
                    return obj
                else:
                    counter += 1

    def get_by_type(self, obj_type, in_list=0):
        counter = 0
        for obj in reversed(self.independent_objects):
            for conn_obj in reversed(obj.connected_objects):
                if conn_obj.object_type == obj_type:
                    if counter == in_list:
                        return conn_obj
                    else:
                        counter += 1
            if obj.object_type == obj_type:
                if counter == in_list:
                    return obj
                else:
                    counter += 1

    def append(self, obj):
        self.independent_objects.append(obj)


class ParsingObject:
    def __init__(self, content, object_type, using_methods):
        self.connected_objects = []
        self.using_methods = using_methods
        self.content = content
        self.properties = {}
        self.object_type = object_type

    def connect(self, object2connect):
        self.connected_objects.append(object2connect)

    def insert_content(self, content2insert, update_function=None):
        self.content += content2insert
        if update_function is not None:
            self.content = update_function(self.content)


class UsingMethods:
    def __init__(self):
        self.__methods = {}

    def connect_method(self, object_types):
        self.__methods['connect'] = object_types

    def append_method(self):
        self.__methods['append'] = True

    def insert_back_method(self):
        self.__methods['insert_back'] = True

    def insert_forward_method(self):
        self.__methods['insert_forward'] = True

    def able_to(self, method, obj):
        if method not in self.__methods:
            return False
        elif type(self.__methods[method]) == bool:
            return True
        elif obj.object_type in self.__methods[method]:
            return True
        else:
            return False


class ObjectGrouping:
    def __init__(self, object_type):
        self.object_type = object_type
        self.groups = []

    def add_group(self, group_key, update_function=None):
        if update_function:
            group_key = update_function(group_key)
        self.groups.append(ObjectGroup(group_key))

    def append_to_last_group(self, obj):
        self.groups[-1].append_object(obj)

    def get_last(self):
        if self.groups:
            return self.groups[-1].get_last()

    def get_last_by_type(self, object_type):
        if object_type == self.object_type:
            return self.get_last()

    def connect(self, object2connect):
        self.get_last().connect(object2connect)

    def insert_content(self, content2insert, update_function=None):
        self.get_last().insert_content(content2insert, update_function)


class ObjectGroup:
    def __init__(self, group_key):
        self.group_key = group_key
        self.subobjects = []

    def get_last(self):
        return self.subobjects[-1]


class LineProcessing:
    def __init__(self, line_text):
        self.line_units = line_text.split()
        self.current_index = 0

    def current(self):
        return self.line_units[self.current_index]

    def next(self, add=0):
        return self.line_units[self.current_index + 1 + add]


class ParsingUnit:
    def __init__(self, line_units, unit_index):
        self.content = line_units[unit_index]

    def what(self):
        ...