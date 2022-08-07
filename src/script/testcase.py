from src.script.web_page import WebPage

class Testcase:
    def __init__(self, name, origins, pages):
        self.data = {}
        self.name = name
        self.origins = origins
        self.pages = pages

        for o in range(self.origins):
            self.data[o] = {}
            # for p in range(pages):
            #     self.data[o][p]
    
    def add(self, html, origin, page):
        self.data[origin][page] = html

    def get(self, origin, page):
        return self.data[origin][page]
