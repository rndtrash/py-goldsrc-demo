#!/usr/bin/env python3

import os
import argparse
from io import BytesIO

from py_goldsrc_demo.parse_demo import parse_demo

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='demos/2008-de_inferno.dem')
    args = parser.parse_args()

    with open(os.path.abspath(args.filename), 'rb') as f:
        demo = parse_demo(BytesIO(f.read()))
        print(demo)
