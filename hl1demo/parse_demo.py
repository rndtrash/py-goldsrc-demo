import os
from io import BytesIO

from hl1demo.BaseDemoParser import BaseDemoParser, DEMO_MAGIC
from hl1demo.CS16DemoParser import CS16DemoParser
from hl1demo.HL25DemoParser import HL25DemoParser
from hl1demo.exceptions import InvalidMagicException, UnknownDemoFormat
from hl1demo.utils import unpack_le, read_binary_string

DEMO_FORMAT_REGISTRY = {
    (5, 47, 'cstrike'): CS16DemoParser,
    (5, 48, 'valve'): HL25DemoParser
}


def parse_demo(bs: BytesIO) -> BaseDemoParser:
    bs.seek(0)

    magic = bs.read(len(DEMO_MAGIC))
    if magic != DEMO_MAGIC:
        raise InvalidMagicException(DEMO_MAGIC, magic)

    demo_protocol, net_protocol = unpack_le('II', bs.read(4 + 4))

    bs.seek(260, os.SEEK_CUR)  # skip the map name
    mod_name = read_binary_string(bs, 260)

    demo_format_tuple = (demo_protocol, net_protocol, mod_name)
    if demo_format_tuple not in DEMO_FORMAT_REGISTRY:
        raise UnknownDemoFormat(*demo_format_tuple)

    return DEMO_FORMAT_REGISTRY[demo_format_tuple](bs)
