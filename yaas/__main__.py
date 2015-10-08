# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function
import argparse
import inspect
import sys
import os

from . import __version__
from . import blueprint
from . import cluster
from . import config
from . import host
from . import repo
from . import service
from . import task

YAAS_VERSION = "yaas version {0}".format(__version__)

def version(parser, args):
    """print the yaas version"""
    print(YAAS_VERSION)

def main():
    config.scheme = os.environ.get('YAAS_SCHEME', config.scheme)
    config.server = os.environ.get('YAAS_SERVER', config.server)
    config.port = os.environ.get('YAAS_PORT', config.port)
    config.username = os.environ.get('YAAS_USER', config.username)
    config.password = os.environ.get('YAAS_PASSWORD', config.password)

    parser = argparse.ArgumentParser(prog="yaas")

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=YAAS_VERSION,
        help="print the yaas version")

    parser.add_argument(
        '--verbose',
        action='store_true',
        default=False,
        help="print ambari api requests and responses")

    subparsers = parser.add_subparsers(dest="command")

    commands = {
        'version' : version,
        'blueprint': blueprint.command,
        'cluster': cluster.command,
        'repo': repo.command,
        'service': service.command,
        'task': task.command,
        'host': host.command,
        }

    for name, fn in commands.items():
        subparsers.add_parser(name, help=inspect.getdoc(fn))

    args, extra = parser.parse_known_args(sys.argv[1:])
    config.command = args

    if args.command != 'version' and config.server is None:
        parser.error("An Ambari server must be specified " \
            "through environment variable YAAS_SERVER.")

    commands[args.command](subparsers.choices[args.command], extra)

if __name__ == '__main__':
    main()

