import os
from dataclasses import dataclass
from io import BytesIO

from hl1demo.data_types import ClientData
from hl1demo.macros import BaseMacro


@dataclass
class ClientDataMacro(BaseMacro):
    client_data: ClientData

    def __str__(self):
        return 'ClientDataMacro(' \
               f'time: {self.time}, frame: {self.frame},' \
               f'client_data: {self.client_data}' \
               ')'

    @staticmethod
    def from_base_macro(base_macro: BaseMacro, binary_stream: BytesIO):
        return ClientDataMacro(base_macro.type, base_macro.time, base_macro.frame,
                               ClientData.from_stream(binary_stream))
