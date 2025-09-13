from typing import Any, TypeAlias

JSON: TypeAlias = dict[str, Any]


class Model:
    def __init__(self, payload: JSON):
        self.payload = payload


class Field:
    def __init__(self, path):
        self.path = path.split('.')

    def __get__(self, instance, owner):
        if instance is None:
            return self
        data = instance.payload
        for key in self.path:
            if key in data:
                data = data[key]
            else:
                return None
        return data

    def __set__(self, instance, value):
        data = instance.payload
        for key in self.path[:-1]:
            if key in data:
                data = data[key]
            else:
                return
        last_key = self.path[-1]
        if last_key in data:
            data[last_key] = value
