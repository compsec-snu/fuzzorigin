from enum import Enum
from enum import auto

class JsApiType(Enum):
    assign = auto()
    operation_addition = auto()
    operation_minus = auto()
    operation_multiple = auto()
    operation_division = auto()
    operation_equal = auto()
    operation_not_equal = auto()
    