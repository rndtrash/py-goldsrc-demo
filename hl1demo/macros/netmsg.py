import os
from dataclasses import dataclass
from io import BytesIO

from hl1demo.data_types import NetMsg
from hl1demo.macros import BaseMacro


@dataclass
class NetMsgMacro(BaseMacro):
    net_msg: NetMsg

    def __str__(self):
        return f'NetMsgMacro(net_msg: {self.net_msg})'

    @staticmethod
    def from_base_macro(base_macro: BaseMacro, binary_stream: BytesIO):
        net_msg = NetMsg.from_stream(binary_stream)

        return NetMsgMacro(base_macro.type, base_macro.time, base_macro.frame, net_msg)
