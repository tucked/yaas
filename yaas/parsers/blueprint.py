# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import json
import sys

from .. import objects

def command(parent_parser):
    parser = parent_parser.add_parser(
        'blueprint',
        help="Interact with Ambari blueprints")

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
    def add(client, args):
        if args.file:
            with open(args.file, 'r') as f:
                raw_blueprint = f.read()
        else:
            raw_blueprint = sys.stdin.read()

        blueprint = objects.Blueprint.parse(json.loads(raw_blueprint))
        client.blueprint_add(
            blueprint_name=args.name,
            blueprint=blueprint,
            validate_topology=args.validate_topology)

    parser = parent_parser.add_parser(
        'add',
        help="Add a blueprint to the Ambari server")
    parser.set_defaults(func=add)
    parser.add_argument(
        'name',
        help="Name of the blueprint to be used in later API calls")
    parser.add_argument(
        'file',
        nargs='?',
        help="Specify a blueprint file to use (default: stdin)")
    parser.add_argument(
        '--validate-topology',
        help="Specify whether to validate a blueprint on upload.")

def blueprint_ls(parent_parser):
    def ls(client, args):
        bps = client.blueprint_list()
        if not client.raw:
            for bp_name in bps:
                print('{name}'.format(name=bp_name))

    parser = parent_parser.add_parser(
        'ls',
        help="List names of blueprints on the Ambari server")
    parser.set_defaults(func=ls)

def blueprint_rm(parent_parser):
    def rm(client, args):
        for name in args.name:
            client.blueprint_remove(name)

    parser = parent_parser.add_parser(
        'rm',
        help="Remove a blueprint from the Ambari server")
    parser.set_defaults(func=rm)
    parser.add_argument(
        'name',
        nargs='+',
        help="Specify a blueprint to add to the Ambari server.")

def blueprint_show(parent_parser):
    def show(client, args):
        for name in args.name:
            blueprint = client.blueprint_get(name)

            print('{name} ({stack_name} {stack_version})'.format(
                name=blueprint.blueprint_name,
                stack_name=blueprint.stack_name,
                stack_version=blueprint.stack_version))

            if blueprint.security is not None:
                print('Security: {type}'.format(type=blueprint.security.type))

            for host_group in blueprint.host_groups:
                print('\n{indent}{cardinality} x "{name}"'.format(
                    indent=' '*4,
                    name=host_group.name,
                    cardinality=host_group.cardinality))

                for component in host_group.components:
                    print('{indent}{name}'.format(
                        indent=' '*4*2,
                        name=component))

    parser = parent_parser.add_parser(
        'show',
        help="Print a summary of an Ambari blueprint")
    parser.set_defaults(func=show)
    parser.add_argument(
        'name',
        nargs='+',
        help="Specify a blueprint to show.")

