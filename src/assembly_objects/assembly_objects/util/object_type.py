from enum import Enum

class ObjectType(Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2
    NONE = -1


def get_object_type(min_length):
    if 24 <= min_length <= 53:
        return ObjectType.SMALL
    elif 63 <= min_length <= 92:
        return ObjectType.MEDIUM
    elif 112 <= min_length <= 141:
        return ObjectType.LARGE
    else:
        return ObjectType.NONE
