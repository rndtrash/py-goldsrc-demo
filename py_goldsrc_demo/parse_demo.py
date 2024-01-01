import os
from io import BytesIO

from py_goldsrc_demo.BaseDemoParser import BaseDemoParser, DEMO_MAGIC
from py_goldsrc_demo.CS16DemoParser import CS16DemoParser
from py_goldsrc_demo.HL25DemoParser import HL25DemoParser
from py_goldsrc_demo.exceptions import InvalidMagicException, UnknownDemoFormat
from py_goldsrc_demo.utils import unpack_le, read_binary_string

DEMO_FORMAT_REGISTRY = {
    (5, 47, 'cstrike'): CS16DemoParser,
    (5, 48, 'valve'): HL25DemoParser
}


def parse_demo(bs: BytesIO) -> BaseDemoParser:
    """Call this function with a binary stream of your file to get a BaseDemoParser object"""
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
