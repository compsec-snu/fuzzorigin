from enum import Enum
from enum import auto

class WebApiType(Enum):
    read_property = auto()
    write_property = auto()
    call_method = auto()
    construct = auto()