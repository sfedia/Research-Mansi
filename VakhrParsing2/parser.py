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