import os
from io import BytesIO

from py_goldsrc_demo.parse_demo import parse_demo


def test_smoke():
    with open('demos/bootcamp_test_short.dem', 'rb') as f:
        parse_demo(BytesIO(f.read()))
