#!/usr/bin/env python3

import os
import argparse
from io import BytesIO

from hl1demo.CS16DemoParser import CS16DemoParser

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='demos/2008-de_inferno.dem')
    args = parser.parse_args()

    with open(os.path.abspath(args.filename), 'rb') as f:
        demo = CS16DemoParser(BytesIO(f.read()))
        print(demo)
