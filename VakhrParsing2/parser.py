#!/usr/bin/python3


class Dictionary:
    def __init__(self):
        self.independent_objects = []

    def get_last(self):
        for obj in reversed(self.independent_objects):
            if obj.connected_objects:
                return obj.connected_objects[-1]
            else:
                return obj

    def get_last_by_type(self, obj_type):
        for obj in reversed(self.independent_objects):
            for conn_obj in reversed(obj.connected_objects):
                if conn_obj.object_type == obj_type:
                    return conn_obj
            if obj.object_type == obj_type:
                return obj

    def append(self, obj):
        self.independent_objects.append(obj)


class ParsingObject:
    def __init__(self, content, object_type):
        self.connected_objects = []
        self.content = content
        self.properties = {}
        self.object_type = object_type

    def connect(self, object2connect):
        self.connected_objects.append(object2connect)

    def insert_content(self, content2insert, update_function=None):
        self.content += content2insert
        if update_function is not None:
            self.content = update_function(self.content)


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