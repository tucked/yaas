# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function
import argparse
import inspect
import requests
import sys
import os

from . import __version__
from . import config
from . import parsers

YAAS_VERSION = "yaas version {0}".format(__version__)


def version(args):
    """ Print the version. """
    print(YAAS_VERSION)


def main():
    parser = argparse.ArgumentParser(prog="yaas")
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=YAAS_VERSION,
        help=inspect.getdoc(version))

    parser.add_argument(
        '--raw',
        action='store_true',
        default=None,
        help="Print the raw Ambari response.")

    parser.add_argument(
        '--debug',
        action='store_true',
        default=None,
        help="Print Ambari requests and responses.")

    subparsers = parser.add_subparsers()
    commands = [
        parsers.blueprint,
        parsers.cluster,
        parsers.repo,
        parsers.service,
        parsers.task,
        parsers.host,
        ]

    for command in commands:
      command.define_subcommand(subparsers)

    version_parser = subparsers.add_parser(
        'version',
        help=inspect.getdoc(version))
    version_parser.set_defaults(func=version)

    args = parser.parse_args()

    # Leverage defaults unless overriden by environment variables
    # or command line prameters
    config.scheme = os.environ.get('YAAS_SCHEME', config.scheme)
    config.server = os.environ.get('YAAS_SERVER', config.server)
    config.port = os.environ.get('YAAS_PORT', config.port)
    config.username = os.environ.get('YAAS_USER', config.username)
    config.password = os.environ.get('YAAS_PASSWORD', config.password)
    if args.raw is not None:
        config.raw = args.raw
    if args.debug is not None:
        config.debug = args.debug

    try:
        args.func(args)
    except requests.exceptions.ConnectionError:
        print(
            'Ambari is not accessible at {url}.'.format(url=config.href('/')),
            'Use YAAS_SCHEME, YAAS_SERVER, and YAAS_PORT to correct.',
            file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as error:
        print(error.response.json()['message'], file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

