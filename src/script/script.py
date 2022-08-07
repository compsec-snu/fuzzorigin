from src.script.web_instruction import WebInstruction
from src.script.statement import *
from src.web_api.web_api_type import WebApiType


class Script:
    def __init__(self):
        self.instructions = []

    def lift(self, guard=False, debug=False, indent=0):
        code = ""
        for inst in self.instructions:
            code += inst.lift(guard, debug, indent) + "\n"
        return code


def main():
    sc = Script()
    inst = WebInstruction("v1", [], "v2", "Node", WebApiType.read_property, "baseURI")
    sc.instructions.append(inst)
    
    state = IfElseStatement()
    inst = WebInstruction("v1", [], "v2", "Node", WebApiType.write_property, "nodeValue")
    state.if_instructions.append(inst)

    sc.instructions.append(state)

    inst = WebInstruction("v1", ["v2"], "v3", "Element", WebApiType.call_method, "appendChild")
    sc.instructions.append(inst)

    state = FunctionStatement("f1", ["v1"])
    inst = WebInstruction("v1", [], "v2", "Node", WebApiType.read_property, "baseURI")
    state.instructions.append(inst)
    sc.instructions.append(state)

    state = TryCatchStatement()
    inst = WebInstruction("v1", [], None, "Node", WebApiType.read_property, "baseURI")
    state.try_instructions.append(inst)
    inst = WebInstruction("v1", ["v2"], "v3", "Element", WebApiType.call_method, "appendChild")
    state.catch_instructions.append(inst)
    sc.instructions.append(state)


if __name__ == "__main__":
    main()
