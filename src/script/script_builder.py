import random
import json
import secrets

from src.script.script import Script
from src.script.web_instruction import WebInstruction
from src.script.js_instruction import JsInstruction
from src.script.string_instruction import StrInstruction
from src.script.statement import *
from src.web_api.web_object import WebObject
from src.web_api.web_api_type import WebApiType
from src.web_api.tag_manager import TagManager
from src.web_api.value_manager import ValueManager
from src.js_api.js_api_type import JsApiType
from src.script.pattern_builder import PatternBuilder
from src.script.poc_builder import PocBuilder


class ScriptBuilder:
    def __init__(self, origin_idx, page_idx, origins=2, pages=2,
            name="sample", prefix=None, max_instruction=100,
            max_state_instruction=20, console_log=True,
            weight_event=0.2, weight_nav=0.2):
        self.origin_idx = origin_idx
        self.page_idx = page_idx
        self.origins = origins
        self.pages = pages

        self.name = name
        self.name_this = self.get_name(self.origin_idx, self.page_idx)

        self.script = Script()
        self.variable_idx = 0
        self.variable_prefix = "v"
        if prefix:
            self.variable_prefix = f"{prefix}_{self.variable_prefix}"
        self.function_idx = 0
        self.function_prefix = "f"
        if prefix:
            self.function_prefix = f"{prefix}_{self.function_prefix}"
        self.max_instruction = max_instruction
        self.max_state_instruction = max_state_instruction
        self.context = {"hash": {}, "Function": [], "all": [],
            "event_candidate": [], "nav_event_candidate": []}
        self.add_context("document", "Document")
        self.add_context("document.body", "HTMLBodyElement")
        self.add_context("console", "Console")
        self.add_context("history", "History")
        self.add_context("window", "Window")

        self.console_log = console_log

        self.pattern_builder = PatternBuilder(self)
        self.poc_builder = PocBuilder(self)

        self.base_url = "http://127.0.0.1:70"

        self.last_var = None
        self.tmp_count = 0

        self.basic_src_candidate = ["data:text/html,a", "data:text/html,", "about:blank", "data:text/xml,"]

        self.WEIGHT_EVENT = weight_event
        self.WEIGHT_NAV = weight_nav

    def get_base_url(self, origin_idx):
        if origin_idx < 10:
            return  f"{self.base_url}0{origin_idx}"
        else:
            return  f"{self.base_url}{origin_idx}"
    
    def get_url(self, origin_idx, page_idx):
        return f"{self.get_base_url(origin_idx)}/{self.get_name(origin_idx, page_idx)}"

    def get_name(self, origin_idx, page_idx):
        return f"{self.name}_{origin_idx}_{page_idx}.html"

    def get_console_log(self, token=None):
        hex = secrets.token_hex(4)
        if token:
             hex = f"{token}-{hex}"
        console_log = f'"[{hex}] {self.get_base_url(self.origin_idx)} " + location.origin'
        return console_log

    def get_origin_violation(self):
        indent = "  "
        func = "function check_origin_violation(fetch, exec){\n"
        func += indent + "if(exec == null){\n" + indent * 2 + "return false;\n" + indent + "}\n"
        func += indent + "if(exec.includes(\"0.0.0.0\")){\n" + indent * 2 + "return false;\n" + indent + "}\n"
        func += indent + "if(fetch == exec){\n" + indent * 2 + "return false;\n" + indent + "}\n"
        func += indent + "return true;\n"
        func += "}"

        return func

    def get_sanitizer(self, token=None):
        hex = secrets.token_hex(4)
        if token:
            hex = f"{token}-{hex}"
        console_log = f'console.log("[{hex}]", "[UXSS]", _origin_fetch_, _origin_exec_);'
        sanitizer = f"var _origin_fetch_ = \"{self.get_base_url(self.origin_idx)}\";\n"
        sanitizer += f"var _origin_exec_ = location.origin;\n"
        sanitizer += "if (check_origin_violation(_origin_fetch_, _origin_exec_)) {\n  " + console_log + "\n}"
        
        return sanitizer

    def get_javascript_console_log(self, token=None):
        return f'javascript:console.log({self.get_console_log(token=token)})'

    def get_random_url(self):
        if (random.random() > 0.9 or (self.page_idx + 1 == self.pages and self.origin_idx + 1 == self.origins)):
            return random.choice(self.basic_src_candidate)
        else:
            y = random.randint(self.page_idx, self.pages - 1)
            if y == self.page_idx:
                x = random.randint(self.origin_idx, self.origins - 1)
            else:
                x = random.randint(1, self.origins - 1)
            return self.get_url(x, y)
        

    def lift(self, guard=False):
        return self.script.lift(guard)

    def add_instructions(self, instructions, register=True):
        for inst in instructions:
            self.add_instruction(inst, register=register)

    def add_instruction(self, instruction, register=True):
        if instruction is None:
            return

        if register:
            self.script.instructions.append(instruction)
        if instruction.__class__.__name__ == "WebInstruction":
            if instruction.api_type != WebApiType.write_property:
                if instruction.name == "createElement":
                    obj = self.get_object_by_tag_name(instruction.params[0][1:-1])
                    self.add_context(instruction.output, obj)
                else:
                    if instruction.output is not None:
                        self.add_context(instruction.output, instruction.get_output_object())
        elif instruction.__class__.__name__ == "JsInstruction":
            if instruction.api_type == JsApiType.operation_equal:
                self.add_context(instruction.output, "Boolean")
            else:
                self.add_context(instruction.output, instruction.obj)
        elif instruction.__class__.__name__ == "IfElseStatement":
            for inst in instruction.if_instructions:
                self.add_instruction(inst, register=False)
            for inst in instruction.else_instructions:
                self.add_instruction(inst, register=False)
        elif instruction.__class__.__name__ == "TryCatchStatement":
            for inst in instruction.try_instructions:
                self.add_instruction(inst, register=False)
            for inst in instruction.catch_instructions:
                self.add_instruction(inst, register=False)
        elif instruction.__class__.__name__ == "FunctionStatement":
            self.add_context(instruction.name, "Function")
            for inst in instruction.instructions:
                self.add_instruction(inst, register=False)
        elif instruction.__class__.__name__ == "EventhandlerStatement":
            self.add_context(instruction.output, "Eventhandler")
            for inst in instruction.instructions:
                self.add_instruction(inst, register=False)

    def add_context(self, variable, obj):
        if not variable:
            return
        if not obj:
            return

        if obj not in self.context.keys():
            self.context[obj] = []

        if obj != "Console":
            self.last_var = variable

        self.context["all"].insert(0, variable)
        self.context[obj].insert(0, variable)
        self.context["hash"][variable] = obj

        try:
            arr = self.get_event_candidate(obj)
            for item in arr:
                self.context["event_candidate"].append(f"{variable}.on{item}")
            arr = self.get_nav_event_candidate(obj)
            for item in arr:
                self.context["nav_event_candidate"].append(f"{variable}.on{item}")
        except:
            pass

    def update_context(self, variable):
        obj = self.get_object_by_variable(variable)
        self.context["all"].insert(0, self.context["all"].pop(self.context["all"].index(variable)))

    def get_new_variable_name(self):
        name = f"{self.variable_prefix}{self.variable_idx}"
        self.variable_idx += 1
        return name

    def get_new_function_name(self):
        name = f"{self.function_prefix}{self.function_idx}"
        self.function_idx += 1
        return name

    def get_property_candidate(self, obj):
        instance = WebObject.create(obj)
        return instance.get_property_candidate()

    def get_property_candidate(self, obj):
        instance = WebObject.create(obj)
        return instance.get_property_candidate()

    def get_writable_property_candidate(self, obj):
        instance = WebObject.create(obj)
        return instance.get_writable_property_candidate()

    def get_property_return(self, obj, name):
        instance = WebObject.create(obj)
        return instance.get_property_return(name)

    def get_method_candidate(self, obj):
        instance = WebObject.create(obj)
        return instance.get_method_candidate()

    def get_method_params(self, obj, name):
        instance = WebObject.create(obj)
        return instance.get_method_params(name)

    def is_method_static(self, obj, name):
        if obj == "Function":
            return False
        instance = WebObject.create(obj)
        return instance.is_method_static(name)

    def get_method_return(self, obj, name):
        instance = WebObject.create(obj)
        return instance.get_method_return(name)

    def get_event_candidate(self, obj):
        instance = WebObject.create(obj)
        return instance.get_event_candidate()

    def get_nav_event_candidate(self, obj):
        nav_event = ["beforeunload", "unload", "DOMContentLoaded", "load"]
        event_list = self.get_event_candidate(obj)
        return list(set(nav_event).intersection(event_list))

    def get_constructor_candidate(self, obj):
        instance = WebObject.create(obj)
        return instance.get_constructor_candidate()

    def get_constructor_return(self, obj, name):
        instance = WebObject.create(obj)
        return instance.get_constructor_return(name)

    def is_constructor_new(self, obj, name):
        instance = WebObject.create(obj)
        return instance.is_constructor_new(name)

    def get_object_by_variable(self, variable):
        try:
            return self.context["hash"][variable]
        except KeyError as e:
            return None

    def get_sorted_order_variable_list(self, arr):
        result = []
        for v in self.context["all"]:
            if v in arr:
                result.append(v)
        return result

    def get_weights(self, n):
        weights = []
        value = 1
        param = 1.1
        for i in range(n):
            weights.append(value)
            value = value / param
        return weights


    def get_random_variable_by_object(self, obj, ref_obj=None):
        if obj == "TagString":
            return TagManager.random_tag()
        elif obj == "EVENT":
            if ref_obj is None:
                return None
            candidate = self.get_event_candidate(ref_obj)
            try:
                return f"'{random.choice(candidate)}'"
            except IndexError as e:
                return None
        elif obj == "Function":
            candidate = self.context["Function"]
            try:
                return f"{random.choice(candidate)}"
            except IndexError as e:
                return None
        elif obj == "IframeSrcString":
            return self.get_random_url()
        elif obj == "SrcString":
            return self.get_random_url()
        elif obj == "ConsoleLogString":
            return self.get_console_log()
        elif obj == "Markup":
            value = f'<script>console.log({self.get_console_log()})<\/script>'
            return f"'{value}'"
        elif obj == "JavascriptConsoleString":
            return f"'{self.get_javascript_console_log()}'"
        elif obj == "URI":
            value = self.get_random_url()
            return f"'{value}'"
        elif obj == "ScriptString":
            value = self.get_script_string()
            return f"'{value}'"
    
        else:
            instance = WebObject.create(obj)
            if instance is not None:
                obj_candidate = instance.get_descendant()
                variable_candidate = []
                try:
                    variable_candidate.extend(self.context[obj])
                except KeyError as e:
                        pass
                for o in obj_candidate:
                    try:
                        variable_candidate.extend(self.context[o])
                    except KeyError as e:
                        pass
                try:
                    if obj == "Console":
                        if random.random() < 0.5:
                            var = "console"
                        else:
                            var = random.choice(variable_candidate)
                        return var
                    else:
                        var_list = self.get_sorted_order_variable_list(variable_candidate)
                        weights = self.get_weights(len(var_list))
                        var = random.choices(var_list, weights=weights, k=1)[0]
                        self.update_context(var)
                        return var

                except IndexError as e:
                    # print(e)
                    return None
            else:
                value = ValueManager.random_bind(obj)
                return value

    def get_object_by_tag_name(self, tag):
        return TagManager.bind(tag)

    def random_generate_instruction(self):
        if random.random() > 0.05:
            try:
                var_list = self.context["all"]
                var = random.choice(var_list)
                self.update_context(var)
                return self.random_generate_instruction_with_input(var)
            except KeyError as e:
                return None
        elif random.random() > 0.01:
            inst = self.generate_web_instruction(None, ['"' + self.get_script_string(guard=False).replace("\n", "").replace('"', '\\"') + '"'], None, "Built-in", WebApiType.call_method, "eval")
            return inst
        else:
            return self.random_generate_call_function()

    def random_generate_weights_instruction(self):
        if random.random() > 0.05:
            try:
                var_list = self.context["all"]
                weights = self.get_weights(len(var_list))
                var = random.choices(var_list, weights=weights, k=1)[0]
                self.update_context(var)
                return self.random_generate_instruction_with_input(var)
            except KeyError as e:
                return None
        else:
            return self.random_generate_call_function()

    def random_generate_call_function(self):
        name = self.get_random_variable_by_object("Function")
        if name is None:
            return None
        api_type = WebApiType.call_method
        params = []
        input = "name"
        output = None
        obj = "Function"
        return self.generate_web_instruction(input, params, output, obj, api_type, name)
        # return None

    def random_generate_instruction_with_input(self, input):
        obj = self.get_object_by_variable(input)
        if obj is None:
            return None
        if WebObject.create(obj) is None:
            return None
        return self.random_generate_instruction_with_input_obj(input, obj)

    def random_generate_instruction_with_obj(self, obj):
        input = self.get_random_variable_by_object(obj)
        if input is None:
            return None
        return self.random_generate_instruction_with_input_obj(input, obj)

    def random_generate_instruction_with_input_obj(self, input, obj):
        # api_type = random.choice(list(WebApiType))
        # return self.random_generate_instruction_with_input_obj_type(input, obj, api_type)

        if random.random() > 0.05 or obj == "Function":
            api_type = random.choice(list(WebApiType))
            return self.random_generate_instruction_with_input_obj_type(input, obj, api_type)
        else:
            api_type = random.choice(list(JsApiType))
            return self.random_generate_js_instruction(input, obj, api_type)

    def random_generate_instruction_with_input_obj_type(self, input, obj, api_type):
        if obj == "Function":
            candidate = self.context["Function"]
        else:
            instance = WebObject.create(obj)
            if instance is None:
                return None
            try:
                if api_type == WebApiType.read_property:
                    candidate = self.get_property_candidate(obj)
                elif api_type == WebApiType.write_property:
                    candidate = self.get_writable_property_candidate(obj)
                elif api_type == WebApiType.construct:
                    candidate = self.get_constructor_candidate(obj)
                else:
                    candidate = self.get_method_candidate(obj)

            except KeyError as e:
                return None

        if len(candidate) == 0:
            return None

        # do not choice skip list
        skip = ["alert", "log", "time", "timeEnd"]
        candidate = [item for item in candidate if item not in skip]

        if len(candidate) == 0:
            return None

        name = random.choice(candidate)

        if api_type == WebApiType.call_method:
            if self.is_method_static(obj, name):
                input = obj

        return self.random_generate_instruction_with_input_obj_type_name(input, obj, api_type, name)

    def random_generate_instruction_with_input_obj_type_name(self, input, obj, api_type, name):
        if obj == "Function":
            param_candidate = []
            output_obj = None
        else:
            instance = WebObject.create(obj)
            if instance is None:
                return None
            try:
                if api_type == WebApiType.call_method:
                    param_candidate = self.get_method_params(obj, name)
                    output_obj = self.get_method_return(obj, name)
                elif api_type == WebApiType.construct:
                    output_obj = self.get_constructor_return(obj, name)
                else:
                    output_obj = self.get_property_return(obj, name)
            except KeyError as e:
                return None

        params = []

        # bind param
        if api_type == WebApiType.call_method:
            for arr in param_candidate:
                param_obj = random.choice(arr)
                param = self.get_random_variable_by_object(param_obj, ref_obj=obj)
                if param is None:
                    return None
                params.append(param)

        # bind output
        if api_type == WebApiType.write_property:
            output = self.get_random_variable_by_object(output_obj)
            if output is None:
                return None
        else:
            if output_obj == None:
                output = None
            else:
                output = self.get_new_variable_name()

        return self.generate_web_instruction(input, params, output, obj, api_type, name)

    def generate_web_instruction(self, input, params, output, obj, api_type, name, keep=True):
        return WebInstruction(input, params, output, obj, api_type, name, keep)

    def random_generate_js_instruction(self, input, obj, api_type):
        if api_type == JsApiType.assign:
            params = []
        else:
            params = [self.get_random_variable_by_object(obj)]

        name = None
        output = self.get_new_variable_name()

        return self.generate_js_instruction(input, params, output, obj, api_type, name)

    def generate_js_instruction(self, input, params, output, obj, api_type, name, keep=True):
        return JsInstruction(input, params, output, obj, api_type, name, keep)

    def generate_random_instructions(self, count=20):
        instructions = []
        insts = self.generate_claim_instruction_console()
        instructions.extend(insts)

        for i in range(count):
            rand = random.random()
            if rand <= self.WEIGHT_NAV:
                rand = random.randint(0, 4)
                if rand == 0:
                    insts = self.pattern_builder.generate_create_iframe_src(ret=True)
                elif rand == 1:
                    insts = self.pattern_builder.generate_set_iframe_src(ret=True)
                elif rand == 2:
                    insts = self.pattern_builder.generate_history_replace(ret=True)
                elif rand == 3:
                    insts = self.pattern_builder.generate_create_a_click(ret=True)
                elif rand == 4:
                    insts = self.pattern_builder.generate_location_replace(ret=True)
                instructions.extend(insts)
            else:
                inst = self.random_generate_instruction()
                if inst is not None:
                    instructions.append(inst)
        return instructions

    def random_generate_if_else(self):
        if random.random() > 0.5:
            obj = "Boolean"
        else:
            obj = "Node"
        cond = self.get_random_variable_by_object(obj)
        if_inst = self.generate_random_instructions(self.max_state_instruction)
        else_inst = self.generate_random_instructions(self.max_state_instruction)
        return self.generate_if_else(cond, if_inst, else_inst)

    def generate_if_else(self, cond, if_inst, else_inst, keep=True):
        return IfElseStatement(cond=cond, if_inst=if_inst, else_inst=else_inst, keep=keep)

    def random_generate_try_catch(self):
        try_inst = self.generate_random_instructions(self.max_state_instruction)
        catch_inst = self.generate_random_instructions(self.max_state_instruction)
        return self.generate_try_catch(try_inst, catch_inst)

    def generate_try_catch(self, try_inst, catch_inst):
        return TryCatchStatement(try_inst=try_inst, catch_inst=catch_inst)

    def random_generate_function(self):
        name = self.get_new_function_name()
        params = []
        # ret = self.get_random_variable_by_object("Node")
        ret = None
        inst = self.generate_random_instructions(self.max_state_instruction)
        return self.generate_function(name, params, ret, inst)

    def generate_function(self, name, params, ret, inst):
        return FunctionStatement(name=name, params=params, ret=ret, inst=inst)

    def random_generate_eventhandler(self):
        output = self.get_new_variable_name()
        params = []
        inst = self.generate_random_instructions(self.max_state_instruction)
        return self.generate_eventhandler(params, output, inst)

    def generate_eventhandler(self, params, output, inst):
        return EventhandlerStatement(params=params, output=output, inst=inst)

    def bind_eventhalder(self):
        try:
            f = random.choice(self.context["Function"])
        except:
            return None
        rand = random.random()
        if rand <= self.WEIGHT_EVENT:
            e = random.choice(self.context["nav_event_candidate"])
        else:
            e = random.choice(self.context["event_candidate"])

        var = e.split(".")[0]
        event = e.split(".")[1]

        if random.random() < 0.5:
            inst = self.generate_web_instruction(var, [], f, self.context["hash"][var], WebApiType.write_property, event)
        else:
            inst = self.generate_web_instruction(var, [f"'{event[2:]}'", f], None, self.context["hash"][var], WebApiType.call_method, "addEventListener")
        return inst

    def get_script_string(self, guard=True):
        sb = ScriptBuilder(self.origin_idx, self.page_idx, max_instruction=10)
        sb.generate()
        return sb.lift(guard=guard)

    def generate_claim_instruction_console(self):
        hex = secrets.token_hex(4)
        insts = []

        text = self.get_sanitizer()
        insts.append(StrInstruction(text))

        text = self.get_origin_violation()
        insts.append(StrInstruction(text))

        return insts

    def generate_claim_instruction_bar(self):
        obj = "Function"
        input = "name"
        inst = self.generate_web_instruction(input, [], None, obj, WebApiType.call_method, "bar", keep=False)
        return inst

    def generate(self):
        count = self.max_instruction

        insts = self.generate_claim_instruction_console()
        self.add_instructions(insts)

        PROB_POC = 0.01
        # PROB_POC = 0.01
        PROB_FUNC = 0.01
        PROB_EVENT = 0.01
        PROB_IF = 0.01
        PROB_TRY = 0.01

        # self.poc_builder.generate_605766()
        # self.poc_builder.generate_613266()
        # self.poc_builder.generate_617495()
        # self.poc_builder.generate_630870()
        # self.poc_builder.generate_655904()
        # self.poc_builder.generate_658535()
        # self.poc_builder.generate_668552()

        # poc = random.choice(self.poc_builder.patterns)
        # poc()

        ## reproduce sucess
        # self.poc_builder.generate_613266()
        # self.poc_builder.generate_617495()


        for i in range(5):
            rand = random.random()
            if rand <= PROB_FUNC:
                rand = random.random()
                if rand > 0.2:
                    inst = self.random_generate_function()
                    self.add_instruction(inst)
                else:
                    inst = self.random_generate_eventhandler()
                    self.add_instruction(inst)
                continue

            rand = random.random()
            if rand <= PROB_EVENT:
                inst = self.bind_eventhalder()
                self.add_instruction(inst)

            rand = random.random()
            if rand <= PROB_IF:
                inst = self.random_generate_if_else()
                self.add_instruction(inst)
                continue

            rand = random.random()
            if rand <= PROB_TRY:
                inst = self.random_generate_try_catch()
                self.add_instruction(inst)
                continue

            rand = random.random()
            if rand <= self.WEIGHT_NAV:
                rand = random.randint(0, 3)
                if rand == 0:
                    self.pattern_builder.generate_create_iframe_src()
                elif rand == 1:
                    self.pattern_builder.generate_location_replace()
                elif rand == 2:
                    self.pattern_builder.generate_history_replace()
                elif rand == 3:
                    self.pattern_builder.generate_create_a_click()

            else:
                inst = self.random_generate_instruction()
                self.add_instruction(inst)

        # # self.poc_builder.generate_605766()

        # for i in range(10):
        #     # rand = random.random()
        #     # if rand <= PROB_POC:
        #     #     poc = random.choice(self.poc_builder.patterns)
        #     #     poc()
        #     #     continue

        #     rand = random.random()
        #     if rand <= PROB_FUNC:
        #         rand = random.random()
        #         if rand > 0.2:
        #             inst = self.random_generate_function()
        #             self.add_instruction(inst)
        #         else:
        #             inst = self.random_generate_eventhandler()
        #             self.add_instruction(inst)
        #         continue

        #     rand = random.random()
        #     if rand <= PROB_EVENT:
        #         inst = self.bind_eventhalder()
        #         self.add_instruction(inst)

        #     rand = random.random()
        #     if rand <= PROB_IF:
        #         inst = self.random_generate_if_else()
        #         self.add_instruction(inst)
        #         continue

        #     rand = random.random()
        #     if rand <= PROB_TRY:
        #         inst = self.random_generate_try_catch()
        #         self.add_instruction(inst)
        #         continue

        #     rand = random.random()
        #     if rand <= self.WEIGHT_NAV:
        #         rand = random.randint(0, 3)
        #         if rand == 0:
        #             self.pattern_builder.generate_create_iframe_src()
        #         elif rand == 1:
        #             self.pattern_builder.generate_location_replace()
        #         elif rand == 2:
        #             self.pattern_builder.generate_history_replace()
        #         elif rand == 3:
        #             self.pattern_builder.generate_create_a_click()

        #     else:
        #         inst = self.random_generate_instruction()
        #         self.add_instruction(inst)

        # poc = random.choice(self.poc_builder.patterns)
        # poc()
        # self.poc_builder.generate_658535()

def main():
    sb = ScriptBuilder(1, 1)
    sb.generate()
    print(sb.lift(guard=True))
    # print(sb.get_sanitizer())
    # print(sb.get_origin_violation())
    

    # print(sb.get_nav_event_candidate("HTMLBodyElement"))
    # print(sb.get_event_candidate("HTMLBodyElement"))
    # print(sb.context)

if __name__ == "__main__":
    main()