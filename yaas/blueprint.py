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
        'remove': _remove,
        'show': _show,
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


def _remove(parser, args):
    """ Remove a blueprint form the server. """
    parser.add_argument(
        'name',
        nargs='+',
        help="Specify a blueprint to add to the Ambari server.")
    subargs = parser.parse_args(args)
    for name in subargs.name:
        response = requests.delete(
            config.href('/api/v1/blueprints/{name}'.format(name=name)),
            **config.requests_opts())


def _show(parser, args):
    """ Show a blueprint. """
    parser.add_argument(
        '--fields',
        help="Print blueprint details.")
    parser.add_argument(
        'name',
        nargs='+',
        help="Specify a blueprint to show.")
    subargs = parser.parse_args(args)
    for name in subargs.name:
        response = requests.get(
            config.href('/api/v1/blueprints/{name}'.format(name=name)),
            params={'fields': subargs.fields},
            **config.requests_opts())
        if config.args.raw:
            pprint.pprint(response.json())
            continue
        response.raise_for_status()
        blueprint = response.json()
        print(
            '{name}{stack}'.format(
                name=blueprint['Blueprints']['blueprint_name'],
                stack=' ({name} {version})'.format(
                    name=blueprint['Blueprints']['stack_name'],
                    version=blueprint['Blueprints']['stack_version'])
                    if 'stack_name' in blueprint['Blueprints'] else ''))
        if subargs.fields is not None:
            del blueprint['Blueprints']
            for key, value in blueprint.items():
                if key != 'href':
                    config.print_field(k=key, v=value, indent=4)
            continue
        for host_group in blueprint['host_groups']:
            print(
                '\n{indent}{cardinality} x "{name}"'.format(
                    indent=' '*4,
                    name=host_group['name'],
                    cardinality=host_group['cardinality']))
            for component in sorted(host_group['components']):
                print(
                    '{indent}{name}'.format(
                        indent=' '*4*2,
                        name=component['name']))
