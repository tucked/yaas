# coding: utf-8

import argparse
import inspect
import sys

from . import __version__

def version(parser, args):
    """print the yaas version"""
    print "yaas version %s" % __version__

def hello(parser, args):
    """show an elephant"""
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
    subparsers = parser.add_subparsers(dest="command")

    commands = {
        'version' : version,
        'hello' : hello
        }

    for name, fn in commands.iteritems():
        subparsers.add_parser(name, help=inspect.getdoc(fn))

    args, extra = parser.parse_known_args(sys.argv[1:])

    commands[args.command](subparsers.choices[args.command], extra)

