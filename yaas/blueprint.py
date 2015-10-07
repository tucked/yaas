# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import inspect
import pprint
import requests
import sys

from . import config


def command(parser, args):
    """ Interact with Ambari blueprints. """
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
    """ List all blueprints stored on the Ambari server. """
    parser.add_argument(
        '--fields',
        help="Print blueprint details.")
    subargs = parser.parses_args(args)
    response = requests.get(
        config.href('/api/v1/blueprints'),
        params={'fields': subargs.fields},
        **config.requests_opts())
    if config.args.raw:
        pprint.pprint(response.json())
        sys.exit(0)
    response.raise_for_status()
    for item in response.json()['items']:
        print('{name}'.format(name=item['Blueprints']['blueprint_name']))
        del item['Blueprints']['blueprint_name']
        for key, value in item.items():
            if key != 'href':
                config.print_field(k=key, v=value, indent=4)
