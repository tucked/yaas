# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import inspect
import pprint
import requests
import sys

from . import config


def command(parser, args):
    """ Interact with registered hosts. """
    subparsers = parser.add_subparsers(dest='subcommand')
    subcommands = {
        'list': _list,
        }
    for name, fn in subcommands.items():
        subparsers.add_parser(name, help=inspect.getdoc(fn))
    subargs, extra = parser.parse_known_args(args)
    subcommands[subargs.subcommand](
        subparsers.choices[subargs.subcommand],
        extra)


def _list(parser, args):
    """ List all registered hosts. """
    parser.add_argument(
        '--fields',
        help="Print host details.")
    subargs, extra = parser.parse_known_args(args)
    response = requests.get(
        config.href('/api/v1/hosts'),
        params={'fields': subargs.fields},
        **config.requests_opts())
    if config.args.raw:
        pprint.pprint(response.json())
        sys.exit(0)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print(response.json()['message'], file=sys.stderr)
        sys.exit(1)
    for item in response.json()['items']:
        line = []
        line_keys = ['host_name', 'cluster_name']
        for key in line_keys:
            if key in item['Hosts']:
                line.append(item['Hosts'][key])
        print(' - '.join(line))
        for key, value in item['Hosts'].items():
            if key not in line_keys:
                print('{indent}{key}: {value}'.format(
                    indent=' '*4, key=key, value=value))
