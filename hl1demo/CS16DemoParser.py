from hl1demo.BaseDemoParser import BaseDemoParser


class CS16DemoParser(BaseDemoParser):
    def __init__(self, bs):
        super().__init__(bs, 5, 47, 'cstrike')