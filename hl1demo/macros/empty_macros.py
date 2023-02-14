from dataclasses import dataclass
from io import BytesIO

import hl1demo
from hl1demo.macros import BaseMacro


@dataclass
class FirstMacro(BaseMacro):
    @staticmethod
    def from_base_macro(base_macro: BaseMacro, binary_stream: BytesIO):
        return FirstMacro(base_macro.type, base_macro.time, base_macro.frame)


@dataclass
class FinalMacro(BaseMacro):
    @staticmethod
    def from_base_macro(base_macro: BaseMacro, binary_stream: BytesIO):
        return FinalMacro(base_macro.type, base_macro.time, base_macro.frame)
