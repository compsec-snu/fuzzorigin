from src.js_api.js_api_type import JsApiType


class JsInstruction:
    def __init__(self, input, params, output, obj, api_type, name=None, keep=True):
        self.input = input
        self.params = params
        self.output = output
        self.obj = obj
        self.api_type = api_type
        self.name = name
        self.keep = keep

    def lift(self, guard=False, debug=False, indent=0):
        code = ""

        if self.api_type == JsApiType.assign:
            code += f"{self.input}"
        else:
            if self.api_type == JsApiType.operation_addition:
                operation = "+"
            elif self.api_type == JsApiType.operation_minus:
                operation = "-"
            elif self.api_type == JsApiType.operation_multiple:
                operation = "*"
            elif self.api_type == JsApiType.operation_division:
                operation = "/"
            elif self.api_type == JsApiType.operation_equal:
                operation = "=="
            elif self.api_type == JsApiType.operation_not_equal:
                operation = "!="
            code += f"{self.input} {operation} {self.params[0]}"

        if self.output:
            code = f"{self.output} = {code}"

        code += ";"
        if guard:
            code = "try {" + code + "} catch(e) {"
            if debug:
                code += "console.log(e);"
            code += "} "

        code = "  " * indent + code

        return code


def main():
    inst = JsInstruction("v1", [1], "v2", "Integer", JsApiType.operation_addition, None)
    print(inst.lift())


if __name__ == "__main__":
    main()