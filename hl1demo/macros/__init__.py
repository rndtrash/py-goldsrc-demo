from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

from hl1demo.utils import unpack_le


@dataclass
class BaseMacro:
    type: int
    time: float
    frame: int

    @staticmethod
    def from_stream(binary_stream: BytesIO):
        frame_type, time, frame = unpack_le('BfI', binary_stream.read(1 + 4 + 4))
        return BaseMacro(frame_type, time, frame)

    @staticmethod
    def from_base_macro(base_macro: BaseMacro, binary_stream: BytesIO):
        pass


class InvalidMacroException(Exception):
    macro_type: int
    macro_time: float
    macro_frame: int

    def __init__(self, macro: BaseMacro):
        super().__init__(
            f'Invalid macro with ID {macro.type} @ Frame {macro.frame}, {macro.time} seconds(?)'
            # TODO: are those really seconds?
        )
        self.macro_type = macro.type
        self.macro_time = macro.time
        self.macro_frame = macro.frame
