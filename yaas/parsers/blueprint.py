# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import inspect
import json
import sys

from .. import blueprint
from .. import config
from .. import utils

def define_subcommand(parent_parser):
    parser = parent_parser.add_parser(
        'blueprint',
        help=inspect.getdoc(blueprint))

    subcommands = [
        blueprint_add,
        blueprint_ls,
        blueprint_rm,
        blueprint_show,
        ]

    subparsers = parser.add_subparsers()
    for subcommand in subcommands:
        subcommand(subparsers)

def blueprint_add(parent_parser):
    def add(args):
        raw_blueprint = None
        if args.file:
            with open(args.file, 'r') as f:
                raw_blueprint = f.read()
        else:
            raw_blueprint = sys.stdin.read()

        blueprint.add(
            blueprint=json.loads(raw_blueprint),
            blueprint_name=args.name,
            validate_topology=args.validate_topology)

    parser = parent_parser.add_parser(
        'add',
        help=inspect.getdoc(blueprint.add))
    parser.set_defaults(func=add)
    parser.add_argument(
        'name',
        help="Name of the blueprint to be used in later API calls")
    parser.add_argument(
        '--validate-topology',
        help="Specify whether to validate a blueprint on upload.")
    parser.add_argument(
        '--file',
        help="Specify a blueprint to add to the Ambari server.")

def blueprint_ls(parent_parser):
    def ls(args):
        bps = blueprint.ls()
        if not config.raw:
            for bp_name in bps:
                print('{name}'.format(name=bp_name))

    parser = parent_parser.add_parser(
        'ls',
        help=inspect.getdoc(blueprint.ls))
    parser.set_defaults(func=ls)

def blueprint_rm(parent_parser):
    def rm(args):
        for name in args.name:
            blueprint.rm(name)

    parser = parent_parser.add_parser(
        'rm',
        help=inspect.getdoc(blueprint.rm))
    parser.set_defaults(func=rm)
    parser.add_argument(
        'name',
        nargs='+',
        help="Specify a blueprint to add to the Ambari server.")

def blueprint_show(parent_parser):
    def show(args):
        for name in args.name:
            res = blueprint.show(name)
            if not config.raw:
                print(
                    '{name} {stack}'.format(
                        name=res['Blueprints']['blueprint_name'],
                        stack='({name} {version})'.format(
                            name=res['Blueprints']['stack_name'],
                            version=res['Blueprints']['stack_version'])))
                for host_group in res['host_groups']:
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

    parser = parent_parser.add_parser(
        'show',
        help=inspect.getdoc(blueprint.show))
    parser.set_defaults(func=show)
    parser.add_argument(
        'name',
        nargs='+',
        help="Specify a blueprint to show.")

