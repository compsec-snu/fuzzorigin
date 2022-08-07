import json
import random
import string

class ValueManager:
    __grammar = None

    @classmethod
    def init(cls):
        if cls.__grammar is None:
            with open("src/web_api/value.json") as f:
                cls.__grammar = json.load(f)

    @classmethod
    def bind(cls, name):
        cls.init()
        if name in cls.__grammar:
            try:
                arr = cls.__grammar[name]
                if arr:
                    return arr
                else:
                    return []
            except KeyError as e:
                return []

    @classmethod
    def random_bind(cls, name):
        cls.init()
        if name in cls.__grammar:
            try:
                arr = cls.__grammar[name]
                if arr:
                    value = random.choice(arr)
                    if name.endswith("String"):
                        value = f"'{value}'"
                    return value
                else:
                    return "null"
            except KeyError as e:
                return "null"
        elif name == "Integer":
            return str(random.randrange(100))
        elif name == "Double":
            return str(random.random() * 100)
        elif name == "String":
            N = random.randrange(10) + 1
            value = ''.join(random.choices(string.ascii_letters + string.digits, k=N))
            return f"'{value}'"
        elif name == "DOMString":
            N = random.randrange(10) + 1
            value = ''.join(random.choices(string.ascii_letters + string.digits, k=N))
            return f"'{value}'"
        elif name == "URI":
            value = "http://127.0.0.1"
            return f"'{value}'"
        elif name == "DomainString":
            value = "127.0.0.1"
            return f"'{value}'"
        # elif name == "Markup":
        #     value = "<script>alert(location)<\/script>"
        #     return f"'{value}'"
        else:
            return "null"

    @classmethod
    def values(cls):
        cls.init()
        return list(cls.__grammar.keys())



def main():
    candidate = ValueManager.bind("rtlltrString")
    print(candidate)

    value = ValueManager.random_bind("Boolean")
    print(value)

    value = ValueManager.random_bind("Integer")
    print(value)

    value = ValueManager.random_bind("Double")
    print(value)

    value = ValueManager.random_bind("String")
    print(value)

    values = ValueManager.values()
    print(values)

if __name__ == "__main__":
    main()