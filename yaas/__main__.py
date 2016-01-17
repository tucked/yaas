# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function
import argparse
import inspect
import requests
import sys
import os

from . import __version__
from .client import Client
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
        default=False,
        help="Print the raw Ambari response.")

    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help="Print Ambari requests and responses.")

    subparsers = parser.add_subparsers()
    commands = [
        parsers.blueprint,
        parsers.bootstrap,
        parsers.cluster,
        parsers.repo,
        parsers.service,
        parsers.task,
        parsers.host,
        ]

    for command in commands:
      command.command(subparsers)

    version_parser = subparsers.add_parser(
        'version',
        help=inspect.getdoc(version))
    version_parser.set_defaults(func=version)

    args = parser.parse_args()

    # Leverage defaults unless overriden by environment variables
    # or command line prameters
    kwargs = {}
    if 'YAAS_SCHEME' in os.environ:
        kwargs['scheme'] = os.environ.get('YAAS_SCHEME')
    if 'YAAS_SERVER' in os.environ:
        kwargs['server'] = os.environ.get('YAAS_SERVER')
    if 'YAAS_PORT' in os.environ:
        kwargs['port'] = os.environ.get('YAAS_PORT')
    if 'YAAS_USER' in os.environ:
        kwargs['user'] = os.environ.get('YAAS_USER')
    if 'YAAS_PASSWORD' in os.environ:
        kwargs['password'] = os.environ.get('YAAS_PASSWORD')
    kwargs['raw'] = args.raw
    kwargs['debug'] = args.debug

    client = Client(**kwargs)

    try:
        args.func(client, args)
    except requests.exceptions.ConnectionError:
        print(
            'Ambari is not accessible at {url}.'.format(url=client._href('/')),
            'Use YAAS_SCHEME, YAAS_SERVER, and YAAS_PORT to correct.',
            file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as error:
        print(error.response.json()['message'], file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

