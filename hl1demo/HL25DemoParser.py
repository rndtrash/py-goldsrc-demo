from hl1demo.BaseDemoParser import BaseDemoParser
from hl1demo.macros import BaseMacro


class HL25DemoParser(BaseDemoParser):
    def __init__(self, bs):
        super().__init__(bs, 5, 48, 'valve')

    def get_macro_by_id(self, base_macro: BaseMacro) -> BaseMacro:
        # TODO: add HL25-specific macros

        return BaseDemoParser.get_macro_by_id(self, base_macro)
