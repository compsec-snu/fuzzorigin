import secrets

class WebPage:
    def __init__(self, html=None, event_handlers=[], body_script=[],
                 foo_bar=None):
        self.html = html
        self.event_handlers = event_handlers
        self.body_script = body_script

        self.handler = False
        if len(self.event_handlers) > 0:
            self.handler = True
            self.event_handler1 = event_handlers[0]
            self.event_handler2 = event_handlers[1]
            

        self.loader = False

        if len(self.event_handlers) > 2:
            self.loader = True
            self.load_handler1 = event_handlers[2]
            self.load_handler2 = event_handlers[3]
            self.load_handler3 = event_handlers[4]
            self.load_handler4 = event_handlers[5]

        self.foo_bar = foo_bar

    def to_string(self, skip=False, debug=False):
        code = self.html
        if skip:
            return code

        head_script = \
            "<script>\n"

        if self.loader:
            head_script += \
            "function eventhandler1() {\n" + \
            self.event_handler1.lift(guard=True, debug=debug) + "}\n" + \
            "function eventhandler2() {\n" + \
            self.event_handler2.lift(guard=True, debug=debug) + "}\n"

        if self.loader:
            head_script += \
                "function load_handler1() {\n" + \
                self.load_handler1.lift(guard=True, debug=debug) + "}\n" + \
                "function load_handler2() {\n" + \
                self.load_handler2.lift(guard=True, debug=debug) + "}\n" + \
                "function load_handler3() {\n" + \
                self.load_handler3.lift(guard=True, debug=debug) + "}\n" + \
                "function load_handler4() {\n" + \
                self.load_handler4.lift(guard=True, debug=debug) + "}\n" 

        head_script += "</script>\n"
        code = code.replace('<head_script>', head_script)

        if "<foo_bar>" in code:
            code = code.replace('<foo_bar>', self.foo_bar)

        for script in self.body_script:
            lift = \
                "<script>\n" + \
                    "window.addEventListener('beforeunload', load_handler1)\n" + \
                    "window.addEventListener('unload', load_handler2)\n" + \
                    "window.addEventListener('DOMContentLoaded', load_handler3)\n" + \
                    "window.addEventListener('load', load_handler4)\n" + \
                script.lift(guard=True, debug=debug) + "\n" + \
                "</script>\n"

            code = code.replace('<body_script>', lift, 1)
        return code