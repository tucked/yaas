# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import inspect

from . import config


def command(parser, args):
    """ Interact with server agents. """
    subparsers = parser.add_subparsers(dest='subcommand')
    subcommands = {
        'list': host_list
        }
    for name, fn in subcommands.items():
        subparsers.add_parser(name, help=inspect.getdoc(fn))
    subargs, extra = parser.parse_known_args(args)
    subcommands[subargs.subcommand](
        subparsers.choices[subargs.subcommand],
        extra)


@config.request('/api/v1/hosts')
def host_list(parser, args, response):
    """ List all server agents. """
    for item in response.json()['items']:
        print(item['Hosts']['host_name'])
