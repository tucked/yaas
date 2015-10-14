# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
import argparse
import inspect
import json
import pprint
import requests
import sys

from . import common

def command(parser, args):
    """Create, modify, and view clusters"""
    subparsers = parser.add_subparsers(dest="command")

    commands = {
        'list': _list,
        'create': _create,
        'show': _show,
        'destroy': _destroy,
        'start': _start,
        'stop': _stop,
        }

    for name, fn in commands.iteritems():
      subparsers.add_parser(name, help=inspect.getdoc(fn))

    sub_args, extra = parser.parse_known_args(args)
    commands[sub_args.command](subparsers.choices[sub_args.command], extra)

def _list(parser, args):
    """ List all clusters. """
    parser.add_argument(
        '-f',
        '--fields',
        help="Print cluster details.")
    list_args, extra = parser.parse_known_args(args)
    response = requests.get(
        common.href('/api/v1/clusters'),
        params={'fields': list_args.fields},
        **common.requests_opts())
    if common.args.raw:
        pprint.pprint(response.json())
        sys.exit(0)
    response.raise_for_status()
    res = response.json()
    for item in res['items']:
        line = []
        for key in ('cluster_name', 'version'):
            if key in item['Clusters']:
                line.append(item['Clusters'][key])
        print(' - '.join(line))
        if list_args.fields:
            for key, value in item.items():
                common.print_field(k=key, v=value, indent=4)

def _create(parser, args):
    pass

def _show(parser, args):
    pass

def _destroy(parser, args):
    pass

def _start(parser, args):
    pass

def _stop(parser, args):
    pass

