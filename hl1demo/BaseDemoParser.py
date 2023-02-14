from io import BytesIO
from struct import unpack
from typing import Any

from hl1demo.exceptions import InvalidMagicException, InvalidDemoProtocolException, InvalidNetProtocolException, \
    InvalidModException


def unpack_le(struct_format: str, buffer: bytes) -> tuple[Any, ...]:
    return unpack('<' + struct_format, buffer)


class BaseDemoParser:
    binary_stream: BytesIO

    demo_protocol: int
    net_protocol: int
    map_name: str
    mod_name: str

    MAGIC = bytes([0x48, 0x4C, 0x44, 0x45, 0x4D, 0x4F, 0x00, 0x00])  # "HLDEMO  "

    def __init__(self, bs: BytesIO, demo_protocol_target: int, net_protocol_target: int, mod_name_target: str):
        self.binary_stream = bs

        bs.seek(0)

        magic = bs.read(len(BaseDemoParser.MAGIC))
        if magic != BaseDemoParser.MAGIC:
            raise InvalidMagicException(BaseDemoParser.MAGIC, magic)

        self.demo_protocol, self.net_protocol = self.unpack('II', 8)
        if self.demo_protocol != demo_protocol_target:
            raise InvalidDemoProtocolException(demo_protocol_target, self.demo_protocol)
        if self.net_protocol != net_protocol_target:
            raise InvalidNetProtocolException(demo_protocol_target, self.demo_protocol)

        self.map_name = self.binary_stream.read(260).rstrip(b'\x00').decode('ascii')
        self.mod_name = self.binary_stream.read(260).rstrip(b'\x00').decode('ascii')
        if self.mod_name != mod_name_target:
            raise InvalidModException(mod_name_target, self.mod_name)

    def __del__(self):
        self.binary_stream.close()

    def unpack(self, struct_format: str, count: int) -> tuple[Any, ...]:
        return unpack_le(struct_format, self.binary_stream.read(count))
