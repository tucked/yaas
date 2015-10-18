# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import argparse
import inspect
import json
import pprint
import requests
import sys

from . import config


def command(parser, args):
    """ Interact with Ambari blueprints. """
    subparsers = parser.add_subparsers(dest='subcommand')
    subcommands = {
        'add': _add,
        'list': _list,
        }
    for name, fn in subcommands.items():
        subparsers.add_parser(name, help=inspect.getdoc(fn))
    subargs, extra = parser.parse_known_args(args)
    subcommands[subargs.subcommand](
        subparsers.choices[subargs.subcommand],
        extra)


def _add(parser, args):
    """ Add a blueprint to the Ambari server. """
    parser.add_argument(
        '--validate-topology',
        help="Specify whether to validate a blueprint on upload.")
    parser.add_argument(
        'blueprint',
        nargs='*',
        help="Specify a blueprint to add to the Ambari server.")
    subargs = parser.parse_args(args)
    blueprints = [] if len(subargs.blueprint) > 0 else [sys.stdin.read()]
    for blueprint_file in subargs.blueprint:
        with open(blueprint_file, 'r') as f:
            blueprints.append(f.read())
    for blueprint in blueprints:
        blueprint = json.loads(blueprint)
        response = requests.post(
            config.href(
                '/api/v1/blueprints/{name}'.format(
                    name=blueprint['Blueprints']['blueprint_name'])),
            data=json.dumps(blueprint),  # `json=blueprint` would be better, but it doesn't work!
            params={'validate_topology': subargs.validate_topology},
            **config.requests_opts())
        response.raise_for_status()


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
