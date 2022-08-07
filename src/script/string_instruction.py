from src.web_api.web_object import WebObject
from src.web_api.web_api_type import WebApiType

class StrInstruction:
    def __init__(self, text, keep=True):
        self.text = text
        self.keep = keep

    def lift(self, guard=False, debug=False, indent=0):
        code = self.text
        if guard:
            code = "try {" + code + "} catch(e) {"
            if debug:
                code += "console.log(e);"
            code += "} "

        code = "  " * indent + code

        return code
