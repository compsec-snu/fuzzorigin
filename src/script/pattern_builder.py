import random

from src.js_api.js_api_type import JsApiType
from src.script.web_instruction import WebInstruction
from src.script.statement import *
from src.web_api.web_object import WebObject
from src.web_api.web_api_type import WebApiType


class PatternBuilder:
    def __init__(self, script_builder):
        self.script_builder = script_builder

    def generate_create_iframe(self):
        i = self.script_builder.get_new_variable_name()
        de = self.script_builder.get_new_variable_name()
        
        inst = self.script_builder.generate_web_instruction("document", ["'iframe'"], i, "Document", WebApiType.call_method, "createElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction("document", [], de, "Document", WebApiType.read_property, "documentElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(de, [i], None, "Element", WebApiType.call_method, "appendChild")
        self.script_builder.add_instruction(inst)

        cd = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(i, [], cd, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(cd, [], None, "Document", WebApiType.call_method, "open")
        self.script_builder.add_instruction(inst)

        cw = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(i, [], cw, "HTMLIFrameElement", WebApiType.read_property, "contentWindow")
        self.script_builder.add_instruction(inst)

    def generate_create_iframe_src(self, ret=False):
        insts = []

        i = self.script_builder.get_new_variable_name()
        de = self.script_builder.get_new_variable_name()

        inst = self.script_builder.generate_web_instruction("document", ["'iframe'"], i, "Document", WebApiType.call_method, "createElement")
        if not ret:
            self.script_builder.add_instruction(inst)
        else:
            insts.append(inst)

        inst = self.script_builder.generate_web_instruction("document", [], de, "Document", WebApiType.read_property, "documentElement")
        if not ret:
            self.script_builder.add_instruction(inst)
        else:
            insts.append(inst)

        inst = self.script_builder.generate_web_instruction(de, [i], None, "Element", WebApiType.call_method, "appendChild")
        if not ret:
            self.script_builder.add_instruction(inst)
        else:
            insts.append(inst)

        src = self.script_builder.get_random_url()
        inst = self.script_builder.generate_web_instruction(i, [], f"'{src}'", "HTMLIFrameElement", WebApiType.write_property, "src")
        if not ret:
            self.script_builder.add_instruction(inst)
        else:
            insts.append(inst)

        if ret:
            return insts

    def generate_set_iframe_src(self, ret=False):
        insts = []
        try:
            i = random.choice(self.script_builder.context["HTMLIFrameElement"])
        except:
            return insts
        
        src = self.script_builder.get_random_url()
        inst = self.script_builder.generate_web_instruction(i, [], f"'{src}'", "HTMLIFrameElement", WebApiType.write_property, "src")
        if not ret:
            self.script_builder.add_instruction(inst)
        else:
            insts.append(inst)

        if ret:
            return insts

    def generate_create_form_action(self, i):
        i_onload = self.script_builder.get_new_function_name()
        i_onload_inst = []

        d = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(i, [], d, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(d, [], None, "Document", WebApiType.call_method, "open")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(i, [], i_onload, "HTMLIFrameElement", WebApiType.write_property, "onload")
        self.script_builder.add_instruction(inst)

        x = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(d, ["'form'"], x, "Document", WebApiType.call_method, "createElement")
        i_onload_inst.append(inst)

        action = self.script_builder.get_javascript_console_log()
        inst = self.script_builder.generate_web_instruction(x, [], f"'{action}'", "HTMLFormElement", WebApiType.write_property, "action")
        i_onload_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(x, [], None, "HTMLFormElement", WebApiType.call_method, "submit")
        i_onload_inst.append(inst)

        inst = self.script_builder.generate_function(i_onload, [], None, i_onload_inst)
        self.script_builder.add_instruction(inst)

        src = self.script_builder.get_random_url()
        inst = self.script_builder.generate_web_instruction(i, [], f"'{src}'", "HTMLIFrameElement", WebApiType.write_property, "src")
        self.script_builder.add_instruction(inst)

    def generate_location_replace(self, ret=False):
        insts = []
        src = self.script_builder.get_random_url()
        inst = self.script_builder.generate_web_instruction("location", [f"'{src}'"], None, "Location", WebApiType.call_method, "replace")
        if not ret:
            self.script_builder.add_instruction(inst)
        else:
            insts.append(inst)
            return insts

    def generate_history_replace(self, ret=False):
        insts = []
        src = self.script_builder.get_random_url()
        inst = self.script_builder.generate_web_instruction("history", ["''", "''", f"'{src}'"], None, "History", WebApiType.call_method, "replaceState")
        if not ret:
            self.script_builder.add_instruction(inst)
        else:
            insts.append(inst)
            return insts
    
    def generate_create_a_click(self, ret=False):
        insts = []
        a = self.script_builder.get_new_variable_name()
        de = self.script_builder.get_new_variable_name()
        
        inst = self.script_builder.generate_web_instruction("document", ["'a'"], a, "Document", WebApiType.call_method, "createElement")
        if not ret:
            self.script_builder.add_instruction(inst)
        else:
            insts.append(inst)

        inst = self.script_builder.generate_web_instruction("document", [], de, "Document", WebApiType.read_property, "documentElement")
        if not ret:
            self.script_builder.add_instruction(inst)
        else:
            insts.append(inst)

        inst = self.script_builder.generate_web_instruction(de, [a], None, "Element", WebApiType.call_method, "appendChild")
        if not ret:
            self.script_builder.add_instruction(inst)
        else:
            insts.append(inst)

        src = self.script_builder.get_random_url()
        inst = self.script_builder.generate_web_instruction(a, [], f"'{src}'", "HTMLAnchorElement", WebApiType.write_property, "href")
        if not ret:
            self.script_builder.add_instruction(inst)
        else:
            insts.append(inst)

        target = random.choice(['_blank', '_self', '_parent', '_top'])
        inst = self.script_builder.generate_web_instruction(a, [], f"'{target}'", "HTMLAnchorElement", WebApiType.write_property, "target")
        if not ret:
            self.script_builder.add_instruction(inst)
        else:
            insts.append(inst)

        inst = self.script_builder.generate_web_instruction(a, [], None, "HTMLAnchorElement", WebApiType.call_method, "click")
        if not ret:
            self.script_builder.add_instruction(inst)
        else:
            insts.append(inst)

        if ret:
            return insts


def main():
    from src.script.script_builder import ScriptBuilder
    sb = ScriptBuilder(1, 1)
    pb = PatternBuilder(sb)

    pb.generate_create_iframe_src()
    pb.generate_set_iframe_src()

    print(sb.script.lift())


if __name__ == "__main__":
    main()
