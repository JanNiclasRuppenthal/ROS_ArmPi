from enum import Enum


class RecognitionState(Enum):
    END_SCENARIO = 0,
    PUT_DOWN_OBJECT = 1,
    CONTINUE_TO_ASSEMBLY = 2,
    NONE = -1
