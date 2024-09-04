from enum import Enum

class ObjectType(Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2
    NONE = -1


def calculate_object_type(min_length):
    if 24 <= min_length <= 54:
        return ObjectType.SMALL
    elif 63 <= min_length <= 93:
        return ObjectType.MEDIUM
    elif 109 <= min_length <= 142:
        return ObjectType.LARGE
    else:
        return ObjectType.NONE
