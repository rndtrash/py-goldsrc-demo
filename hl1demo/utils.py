from io import BytesIO
from struct import unpack
from typing import Any


def unpack_le(struct_format: str, buffer: bytes) -> tuple[Any, ...]:
    return unpack('<' + struct_format, buffer)


def read_binary_string(binary_stream: BytesIO, length: int):
    return binary_stream.read(length).rstrip(b'\x00').decode('ascii')
