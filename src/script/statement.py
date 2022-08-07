class IfElseStatement:
    def __init__(self, cond=None, if_inst=[], else_inst=[], keep=True):
        self.condition = cond
        self.if_instructions = [x for x in if_inst if x is not None]
        self.else_instructions = [x for x in else_inst if x is not None]
        self.keep = keep

    def lift(self, guard=False, debug=False, indent=0):
        if self.condition:
            try:
                cond = self.condition.lift()
            except:
                cond = str(self.condition)
        else:
            cond = 'true'

        if guard:
            indent += 1
        code = "  " * indent + f"if ({cond}) " + "{\n"
        
        for inst in self.if_instructions:
            if inst is None:
                continue
            code += inst.lift(guard, debug, indent+1) + "\n"
        code += "  " * indent + "}\n"
        code += "  " * indent + "else {\n"
        for inst in self.else_instructions:
            if inst is None:
                continue
            code += inst.lift(guard, debug, indent+1) + "\n"
        code += "  " * indent + "}"
        if guard:
            indent -= 1
            code = "  " * indent + "try {\n" + code + "\n" + "  " * indent + "} catch(e) {"
            if debug:
                code += "console.log(e);"
            code += "}"
        return code

class TryCatchStatement:
    def __init__(self, try_inst=[], catch_inst=[], keep=True):
        self.try_instructions = [x for x in try_inst if x is not None]
        self.catch_instructions = [x for x in catch_inst if x is not None]
        self.keep = keep

    def lift(self, guard=False, debug=False, indent=0):
        code = "  " * indent + "try {\n"
        
        for inst in self.try_instructions:
            if inst is None:
                continue
            code += inst.lift(False, debug, indent+1) + "\n"
        code += "  " * indent + "}\n"
        code += "  " * indent + "catch (e) {\n"
        for inst in self.catch_instructions:
            if inst is None:
                continue
            code += inst.lift(guard, debug, indent+1) + "\n"
        code += "  " * indent + "}"
        return code

class FunctionStatement:
    def __init__(self, name="f", params=[], ret=None, inst=[], keep=True):
        self.name = name
        self.params = params
        self.ret = ret
        self.instructions = [x for x in inst if x is not None]
        self.keep = keep

    def lift(self, guard=False, debug=False, indent=0):
        code = "  " * indent + f"function {self.name} ({', '.join(self.params)}) " + "{\n"
        
        for inst in self.instructions:
            if inst is None:
                continue
            code += inst.lift(guard, debug, indent+1) + "\n"
        code += "  " * indent + "}"
        return code


class EventhandlerStatement:
    def __init__(self, params=[], output=None, inst=[], keep=True):
        self.params = params
        self.instructions = [x for x in inst if x is not None]
        self.output = output
        self.keep = keep

    def lift(self, guard=False, debug=False, indent=0):
        code = f"get handleEvent ({', '.join(self.params)}) " + "{\n"
        
        for inst in self.instructions:
            if inst is None:
                continue
            code += inst.lift(guard, debug, indent+1) + "\n"
        if self.output is not None:
            code = self.output + " = {" + code 
        code = "  " * indent + code
        code += "  " * indent + "}"

        if self.output is not None:
            code += "};"

        return code


def main():
    inst = EventhandlerStatement(output="v1")
    print(inst.lift(indent=1))

    inst = EventhandlerStatement()
    print(inst.lift(indent=1))

if __name__ == "__main__":
    main()