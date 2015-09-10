# coding: utf-8

import argparse
import sys

from . import __version__

def version(args):
    print "yaas version %s" % __version__

def hello(args):
    print "                .-.._       "
    print "          __  /`     '.     "
    print "       .-'  `/   (   a \    "
    print "      /      (    \,_   \   "
    print "     /|       '---` |\ =|   "
    print "    ` \    /__.-/  /  | |   "
    print "       |  / / \ \  \   \_\  "
    print "       |__|_|  |_|__\       "

def main():
    parser = argparse.ArgumentParser(prog="yaas")
    subparsers = parser.add_subparsers()

    version_parser = subparsers.add_parser(
        'version',
        help="print Yaas version")
    version_parser.set_defaults(func=version)

    hello_parser = subparsers.add_parser(
        'hello',
        help="show a greeting")
    hello_parser.set_defaults(func=hello)

    args = parser.parse_args()
    args.func(args)
