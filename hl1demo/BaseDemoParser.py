from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import Any, List

from hl1demo.exceptions import InvalidMagicException, InvalidDemoProtocolException, InvalidNetProtocolException, \
    InvalidModException
from hl1demo.macros import BaseMacro, InvalidMacroException
from hl1demo.macros.empty_macros import FinalMacro, FirstMacro
from hl1demo.macros.base import FullFrameMacro, ClientDataMacro
from hl1demo.utils import unpack_le, read_binary_string


class BaseDemoParser:
    @dataclass
    class Directory:
        id: int
        name: str
        flags: int
        cd_track: int
        time: float
        frames: int
        offset: int
        length: int
        macros: List

        @staticmethod
        def from_stream(binary_stream: BytesIO):
            (dir_id,) = unpack_le('I', binary_stream.read(4))
            name = read_binary_string(binary_stream, 64)
            flags, cd_track, time, frames, offset, length \
                = unpack_le('IifIII', binary_stream.read(4 + 4 + 4 + 4 + 4 + 4))
            macros = list()
            return BaseDemoParser.Directory(dir_id, name, flags, cd_track, time, frames, offset, length, macros)

    class MalformedDirectoryException(Exception):
        directory_name: str
        directory_offset: int

        def __init__(self, directory: BaseDemoParser.Directory):
            super().__init__(f'Malformed directory \"{directory.name}\" @ Offset {directory.offset}')

            self.directory_name = directory.name
            self.directory_offset = directory.offset

    binary_stream: BytesIO

    demo_protocol: int
    net_protocol: int
    map_name: str
    mod_name: str
    map_crc: int

    directories: List[Directory]

    MAGIC = bytes([0x48, 0x4C, 0x44, 0x45, 0x4D, 0x4F, 0x00, 0x00])  # "HLDEMO  "

    def __init__(self, bs: BytesIO, demo_protocol_target: int, net_protocol_target: int, mod_name_target: str):
        self.binary_stream = bs

        bs.seek(0)

        magic = bs.read(len(BaseDemoParser.MAGIC))
        if magic != BaseDemoParser.MAGIC:
            raise InvalidMagicException(BaseDemoParser.MAGIC, magic)

        self.demo_protocol, self.net_protocol = self.unpack('II', 4 + 4)
        if self.demo_protocol != demo_protocol_target:
            raise InvalidDemoProtocolException(demo_protocol_target, self.demo_protocol)
        if self.net_protocol != net_protocol_target:
            raise InvalidNetProtocolException(demo_protocol_target, self.demo_protocol)

        self.map_name = read_binary_string(self.binary_stream, 260)
        self.mod_name = read_binary_string(self.binary_stream, 260)
        if self.mod_name != mod_name_target:
            raise InvalidModException(mod_name_target, self.mod_name)

        self.map_crc, dir_offset = self.unpack('iI', 4 + 4)

        self.binary_stream.seek(dir_offset)
        (directory_count,) = self.unpack('I', 4)
        self.directories = list()
        for _ in range(directory_count):
            self.directories.append(BaseDemoParser.Directory.from_stream(self.binary_stream))

        for directory in self.directories:
            # TODO: DEBUG
            print(f'Directory \"{directory}\"')

            self.binary_stream.seek(directory.offset)

            last_macro = None
            while not isinstance(last_macro, FinalMacro):
                macro = BaseMacro.from_stream(self.binary_stream)
                last_macro = self.get_macro_by_id(macro)
                directory.macros.append(last_macro)

                # TODO: DEBUG
                # print(last_macro)
            print(len(directory.macros))
            print(directory.length == len(directory.macros))

    def __del__(self):
        self.binary_stream.close()

    def unpack(self, struct_format: str, count: int) -> tuple[Any, ...]:
        return unpack_le(struct_format, self.binary_stream.read(count))

    def get_macro_by_id(self, base_macro: BaseMacro) -> BaseMacro:
        match base_macro.type:
            case 0 | 1:
                return FullFrameMacro.from_base_macro(base_macro, self.binary_stream)
            case 2:
                return FirstMacro.from_base_macro(base_macro, self.binary_stream)
            case 4:
                return ClientDataMacro.from_base_macro(base_macro, self.binary_stream)
            case 5:
                return FinalMacro.from_base_macro(base_macro, self.binary_stream)
        raise InvalidMacroException(base_macro)
