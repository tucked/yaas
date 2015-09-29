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
    config.server_url = os.environ.get('YAAS_SERVER_URL', config.server_url)
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
    config.args = args

    if args.command != 'version' and config.server_url is None:
        parser.error("Ambari server URL must be specified " \
            "through environment variable YAAS_SERVER_URL")

    commands[args.command](subparsers.choices[args.command], extra)

