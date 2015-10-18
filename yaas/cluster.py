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
    """Create a cluster"""
    parser.add_argument(
        'name',
        help="Cluster name")
    parser.add_argument(
        '-t',
        '--template',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help="Cluster creation template")
    create_args, _ = parser.parse_known_args(args)

    response = requests.post(
        common.href('/api/v1/clusters/' + create_args.name),
        data=create_args.template.read(),
        **common.requests_opts())
    if common.args.raw:
        pprint.pprint(response.json())
        sys.exit(0)
    response.raise_for_status()

def _show(parser, args):
    """Show basic cluster information or export in a specified format"""
    parser.add_argument(
        'cluster',
        nargs='+',
        help="Shut down all services in cluster")
    parser.add_argument(
        '-f',
        '--format',
        action='store',
        help="Export cluster in specified format (e.g. blueprint)")
    show_args, _ = parser.parse_known_args(args)
    if args.format is not None:
        response = requests.get(
            common.href('/api/v1/clusters/' + cluster),
            params={'format': args.format},
            **common.requests_opts())
        response.raise_for_status()
        if not common.args.raw:
            response.raise_for_status()
        pprint.pprint(response.json())
        sys.exit(0)
    for cluster in show_args.cluster:
        response = requests.get(
            common.href('/api/v1/clusters/' + cluster),
            **common.requests_opts())
        if common.args.raw:
            pprint.pprint(response.json())
            sys.exit(0)
        response.raise_for_status()
        res = response.json()

        print("Alerts")
        for alert_state, num_hosts in res['alerts']['summary'].items():
            print('\t{0} - {1}'.format(alert_state, num_hosts))
        print("Services")
        for service in res['services']:
            print("\t" + service['ServiceInfo']['service_name'])
        print("Hosts")
        for host in res['hosts']:
            print("\t" + host['Hosts']['host_name'])

def _destroy(parser, args):
    """Delete cluster from ambari. Requires all services in cluster to be stopped"""
    parser.add_argument(
        'cluster',
        nargs='+',
        help="Remove cluster from ambari (requires cluster to be stopped)")
    destroy_args, _ = parser.parse_known_args(args)
    for cluster in destroy_args.cluster:
        response = requests.delete(
            common.href('/api/v1/clusters/' + cluster),
            **common.requests_opts())
        if common.args.raw:
            pprint.pprint(response.json())
            sys.exit(0)
        response.raise_for_status()

def _start(parser, args):
    pass

def _stop(parser, args):
    pass

