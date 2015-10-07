# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import inspect
import pprint
import requests

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
    response = requests.get(
        config.href('/api/v1/hosts'),
        **config.requests_opts())
    if config.args.raw:
        pprint.pprint(response.json())
    else:
        for item in response.json()['items']:
            print(item['Hosts']['host_name'])
