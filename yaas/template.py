# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import inspect
import pprint
import sys

from . import config


def command(parser, args):
    """ Interact with Ambari cluster creation templates. """
    subparsers = parser.add_subparsers(dest='subcommand')
    subcommands = {
        'create': _create,
        }
    for name, fn in subcommands.items():
        subparsers.add_parser(name, help=inspect.getdoc(fn))
    subargs, extra = parser.parse_known_args(args)
    subcommands[subargs.subcommand](
        subparsers.choices[subargs.subcommand],
        extra)


def _create(parser, args):
    """ Generate a cluster creation template. """

    parser.add_argument(
        '--blueprint',
        help="Specify a blueprint for the template.")
    parser.add_argument(
        '--default-password',
        help="Specify a default password for the template.")
    parser.add_argument(
        'group_hosts',
        metavar='group:host[,host[...]]',
        nargs='*',
        help="Add one or more hosts to a host groups.")
    subargs = parser.parse_args(args)

    template = {'host_groups': []}
    if subargs.blueprint is not None:
        template['blueprint'] = subargs.blueprint
    if subargs.default_password is not None:
        template['default_password'] = subargs.default_password
    for group_hosts in subargs.group_hosts:
        group, hosts = group_hosts.split(':')
        hosts = hosts.split(',')
        host_group = {
            'name': group,
            'hosts': [],
        }
        for host in hosts:
            host_group['hosts'].append({'fqdn': host})
        template['host_groups'].append(host_group)

    if config.args.raw:
        pprint.pprint(template)
        sys.exit(0)
    for k, v in template.items():
        config.print_field(k=k, v=v)
