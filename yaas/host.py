# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import inspect
import pprint
import requests
import sys

from . import common


def command(parser, args):
    """ Interact with registered hosts. """
    subparsers = parser.add_subparsers(dest='subcommand')
    subcommands = {
        'list': _list,
        'show': _show,
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
        common.href('/api/v1/hosts'),
        params={'fields': subargs.fields},
        **common.requests_opts())
    if common.args.raw:
        pprint.pprint(response.json())
        sys.exit(0)
    response.raise_for_status()
    for item in response.json()['items']:
        line = []
        line_keys = ['host_name', 'cluster_name']
        for key in line_keys:
            if key in item['Hosts']:
                line.append(item['Hosts'][key])
        print(' - '.join(line))
        for key, value in item['Hosts'].items():
            if key not in line_keys:
                config.print_field(k=key, v=value, indent=4)


def _show(parser, args):
    """ Show registered host info. """
    parser.add_argument(
        '--hardware',
        action='store_true',
        default=False,
        help="Print hardware specs.")
    subargs, extra = parser.parse_known_args(args)
    for host_name in extra:
        response = requests.get(
            common.href('/api/v1/hosts/{host}'.format(host=host_name)),
            **common.requests_opts())
        if common.args.raw:
            pprint.pprint(response.json())
            sys.exit(0)
        response.raise_for_status()
        res=response.json()
        print(
            '[{state}] {host} ({ip}) - {status}'.format(
                host=res['Hosts']['host_name'],
                ip=res['Hosts']['ip'],
                state=res['Hosts']['host_state'],
                status=res['Hosts']['host_status']))
        for alert in res['alerts']['detail']:
            if alert['status'] != 'OK':
                print(
                    '{indent}{service} {status} {desc}: {message}'.format(
                        indent=' '*4,
                        service=alert['service_name'],
                        status=alert['status'],
                        desc=alert['description'],
                        message=alert['output']))
        if subargs.hardware:
            print(
                '{indent}{cores}-core {memory}B {os} {rack}'.format(
                    indent=' '*4,
                    cores=res['Hosts']['cpu_count'],
                    memory=res['Hosts']['total_mem'],
                    os=res['Hosts']['os_type'],
                    rack=res['Hosts']['rack_info']))
            for disk in res['Hosts']['disk_info']:
                print(
                    '{indent}{mount} {type} {percent} ({used}B/{size}B)'.format(
                        indent=' '*8,
                        mount=disk['mountpoint'],
                        type=disk['type'],
                        percent=disk['percent'],
                        used=disk['used'],
                        size=disk['size']))
