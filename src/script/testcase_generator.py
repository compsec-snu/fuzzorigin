import random
import os

from src.script.testcase import Testcase
from src.script.web_page import WebPage
from src.script.script import Script
from src.script.script_builder import ScriptBuilder

from tools.domato import generator


class TestcaseGenerator:
    def __init__(self, origins=2, pages=5, console_log=True,
            weight_event=0.2, weight_nav=0.2):
        self.origins = origins
        self.pages = pages
        self.console_log = console_log
        self.weight_event = weight_event
        self.weight_nav = weight_nav

    def generate_web_page(self, name, origin, page, origins, pages):
        html = generator.generate()

        count = html.count("<body_script>")
        body_script = []

        context = {}
        variable_idx = 0
        function_idx = 0

        for i in range(count):
            sb = ScriptBuilder(origin, page, origins=origins, pages=pages,
                name=name, console_log=self.console_log, weight_event=self.weight_event, weight_nav=self.weight_nav)
            if i != 0:
                sb.context = context
                sb.variable_idx = variable_idx
                sb.function_idx = function_idx

            sb.generate()
            body_script.append(sb.script)
            context = sb.context
            variable_idx = sb.variable_idx
            function_idx = sb.function_idx

        event_handler = []
        prefix = ["eh1", "eh2", "load1", "load2", "load3", "load4"]

        for i in range(len(prefix)):
            sb = ScriptBuilder(origin, page, origins=origins, pages=pages,
                name=name, prefix=prefix[i], max_instruction=5, console_log=self.console_log,
                weight_event=self.weight_event, weight_nav=self.weight_nav)
            sb.generate()
            event_handler.append(sb.script)

        # foo_bar = self.get_foo_bar(typ)

        web = WebPage(html=html, event_handlers=event_handler, body_script=body_script,
                      foo_bar="")

        return web

    def get_foo_bar(self, typ):
        if typ == "main" or "sub":

            foo_bar = """
                Function.foo = function() {
                    console.log("[foo] [TRUE] http://127.0.0.1:7000 http://127.0.0.1:7000");
                };
                """
        else:
            foo_bar = """
                function bar() {
                    try{
                        var p = fetch.call(parent);
                        var f = p.constructor.constructor;
                        f.foo();
                    } catch(e) {}
                }
                """
        return foo_bar
        

    def generate(self, name):
        tc = Testcase(name, self.origins, self.pages)
        for origin in range(self.origins):
            for page in range(self.pages):
                html = self.generate_web_page(name, origin, page, self.origins, self.pages)
                tc.add(html, origin, page)
        return tc


def get_base_url(base_url, origin_idx):
    if origin_idx < 10:
        return  f"{base_url}0{origin_idx}"
    else:
        return  f"{base_url}{origin_idx}"

def get_url(name, base_url, origin_idx, page_idx):
    return f"{get_base_url(base_url, origin_idx)}/{get_name(name, origin_idx, page_idx)}"

def get_name(name, origin_idx, page_idx):
    return f"{name}_{origin_idx}_{page_idx}.html"

def to_server(tc):
    base = "new_servers/data"
    for origin in range(tc.origins):
        for page in range(tc.pages):
            print(f"[+] write {origin},{page}/{tc.origins},{tc.pages}")
            name = get_name(tc.name, origin, page)
            dest = os.path.join(base, f"idx_{origin}", name)

            code = tc.get(origin, page).to_string(debug=True)

            with open(dest, "w") as f:
                f.write(code)

def main():
    tg = TestcaseGenerator(5, 10)
    print("[+] generate tc1")
    name = "sample"
    tc = tg.generate(name)
    to_server(tc)

if __name__ == "__main__":
    main()
