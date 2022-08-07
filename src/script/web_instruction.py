from src.web_api.web_object import WebObject
from src.web_api.web_api_type import WebApiType

class WebInstruction:
    def __init__(self, input, params, output, obj, api_type, name, keep=True):
        self.input = input
        self.params = params
        self.output = output
        self.obj = obj
        self.api_type = api_type
        self.name = name
        self.keep = keep

    def lift(self, guard=False, debug=False, indent=0):
        code = ""

        if self.input and self.obj != "Function" and self.obj != "Built-in":
            code += f"{self.input}."

        if self.api_type == WebApiType.call_method or self.api_type == WebApiType.construct:
            if self.name == "item":
                code = code[:-1] + f"[{', '.join(map(str, self.params))}]"
            else:
                code += f"{self.name}"
                code += f"({', '.join(map(str, self.params))})"

        else:
            code += f"{self.name}"

        if self.api_type == WebApiType.construct:
            code = "new " + code

        if self.output:
            if self.api_type == WebApiType.read_property or \
                    self.api_type == WebApiType.call_method or \
                    self.api_type == WebApiType.construct:
                code = f"{self.output} = {code}"
            if self.api_type == WebApiType.write_property:
                code = f"{code} = {self.output}"

        code += ";"
        if guard:
            code = "try {" + code + "} catch(e) {"
            if debug:
                code += "console.log(e);"
            code += "} "

        code = "  " * indent + code

        return code

    def get_input_object(self):
        return WebObject.create(self.obj)

    def get_output_object(self):
        instance = WebObject.create(self.obj)
        if instance is not None:
            if self.api_type == WebApiType.call_method:
                return instance.get_method_return(self.name)
            elif self.api_type == WebApiType.construct:
                return instance.get_constructor_return(self.name)
            else:
                return instance.get_property_return(self.name)


def main():
    inst = WebInstruction("v1", [], "v2", "Node", WebApiType.read_property, "baseURI")
    print(inst.lift())


if __name__ == "__main__":
    main()