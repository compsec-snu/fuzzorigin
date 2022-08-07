import json
import random

class TagManager:
    __grammar = None

    @classmethod
    def init(cls):
        if cls.__grammar is None:
            with open("src/web_api/tag.json") as f:
                cls.__grammar = json.load(f)

    @classmethod
    def bind(cls, name):
        cls.init()
        if name in cls.__grammar:
            try:
                obj = cls.__grammar[name]
                if obj:
                    return obj
                else:
                    return "HTMLElement"
            except KeyError as e:
                return "HTMLElement"

    @classmethod
    def tags(cls):
        cls.init()
        return list(cls.__grammar.keys())

    @classmethod
    def random_tag(cls):
        cls.init()
        tag = random.choice(list(cls.__grammar.keys()))
        return f"'{tag}'"


def main():
    candidate = TagManager.tags()
    print(candidate)

    obj = TagManager.bind("a")
    print(obj)

if __name__ == "__main__":
    main()