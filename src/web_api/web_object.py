import json


class WebObject():
    __grammar = None
    __instance = {}

    @classmethod
    def __getInstance(cls, name):
        return cls.__instance[name]
    
    @classmethod
    def create(cls, name):
        if not cls.__grammar:
            with open("src/web_api/grammar.json") as f:
                print('[+] load web api grammar')
                cls.__grammar = json.load(f)
                # print(cls.__grammar)

        if name in cls.__grammar:
            if name in cls.__instance:
                return cls.__getInstance(name)
            else:
                cls.__instance[name] = cls(name, cls.__grammar[name])
                return cls.__getInstance(name)
        else:
            return None

    def __init__(self, name, meta):
        self.name = name
        self.inherit = [WebObject.create(name) for name in meta["inherit"]]
        self.constructors = meta["constructors"]
        self.properties = meta["properties"]
        self.methods = meta["methods"]
        self.events = meta["events"]
        self.descendant = []

        try:
            self.inherit.remove(None)
        except ValueError as e:
            pass

        for i in self.inherit:
            self.properties = {**i.properties, **self.properties}
            self.methods = {**i.methods, **self.methods}
            self.events = self.events + i.events
            i.set_descendant(self.name)
        self.events = list(set(self.events))

    def get_property_candidate(self):
        return list(self.properties.keys())

    def get_writable_property_candidate(self):
        prop = list(a for a in self.properties.keys() if not self.properties[a]['read_only'])
        event = ["on" + sub for sub in self.events]
        return prop + event

    def get_property_return(self, name):
        if name.startswith("on"):
            return "Function"
        return self.properties[name]["ret"]

    def get_method_candidate(self):
        return list(self.methods.keys())

    def get_method_params(self, name):
        return self.methods[name]["params"]

    def is_method_static(self, name):
        return self.methods[name]["static"]

    def get_method_return(self, name):
        return self.methods[name]["ret"]

    def get_event_candidate(self):
        return self.events

    def get_constructor_candidate(self):
        return list(self.constructors.keys())

    def is_constructor_new(self, name):
        return self.constructors[name]["new"]

    def get_constructor_return(self, name):
        return self.constructors[name]["ret"]

    def set_descendant(self, name):
        self.descendant.append(name)
        for i in self.inherit:
            i.set_descendant(name)

    def get_descendant(self):
        return self.descendant

def object_test():
    with open("src/web_api/grammar.json") as f:
        grammar = json.load(f)

    done = list(grammar.keys())
    todo = []

    for obj in done:
        instance = WebObject.create(obj)

        arr = instance.get_property_candidate()
        for name in arr:
            ret = instance.get_property_return(name)
            
            if ret not in done:
                todo.append(ret)

        arr = instance.get_method_candidate()
        for name in arr:
            ret = instance.get_method_return(name)
            if ret not in done:
                todo.append(ret)

    todo = list(set(todo))
    print(todo)

def main():
    # obj = WebObject.create("aa")
    # obj2 = WebObject.create("bb")

    # # Node
    # obj3 = WebObject.create("Node")
    # print(obj3.name)
    # print(obj3.inherit)
    # print(obj3.get_property_candidate())
    # print(obj3.get_writable_property_candidate())
    # print(obj3.get_property_return("baseURI"))
    # print(obj3.get_method_candidate())
    # print(obj3.get_method_params("appendChild"))
    # print(obj3.get_method_return("appendChild"))
    # print(obj3.get_event_candidate())

    # # Element
    obj4 = WebObject.create("Element")
    print(obj4.name)
    print(obj4.inherit)
    print(obj4.get_property_candidate())
    print(obj4.get_writable_property_candidate())
    print(obj4.get_property_return("onmousemove"))
    
    # print(obj4.get_property_return("attributes"))
    # print(obj4.get_method_candidate())
    # print(obj4.get_method_params("addEventListener"))
    # print(obj4.get_method_return("addEventListener"))
    # print(obj4.get_event_candidate())

    # object_test()

    # h = WebObject.create("HTMLElement")
    # print(h.descendant)
    # # print([i.name for i in obj.inherit])

    # n = WebObject.create("Node")
    # print(n.descendant)

    # e = WebObject.create("Element")
    # print(e.descendant)

    # d = WebObject.create("Document")
    # print(d.descendant)

    # a = WebObject.create("DocumentFragment")
    # print(a.descendant)

    # a = WebObject.create("GlobalEventHandlers")
    # print(a.descendant)

    # print(n.descendant)
    # print(e.descendant)


if __name__ == "__main__":
    main()