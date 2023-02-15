import os
from dataclasses import dataclass
from io import BytesIO

from hl1demo.data_types import Camera, ClientData
from hl1demo.macros import BaseMacro
from hl1demo.utils import unpack_le


@dataclass
class FullFrameMacro(BaseMacro):
    # TODO: actually store the data
    camera: Camera

    def __str__(self):
        return 'FullFrameMacro(' \
               f'time: {self.time}, frame: {self.frame},' \
               f'camera: {self.camera}' \
               ')'

    @staticmethod
    def from_base_macro(base_macro: BaseMacro, binary_stream: BytesIO):
        binary_stream.seek(4, os.SEEK_CUR)

        camera = Camera.from_stream(binary_stream)

        binary_stream.seek(436, os.SEEK_CUR)

        (frame_data_length,) = unpack_le('I', binary_stream.read(4))
        # TODO: read the frame data
        binary_stream.seek(frame_data_length, os.SEEK_CUR)

        return FullFrameMacro(base_macro.type, base_macro.time, base_macro.frame,
                              camera)


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
