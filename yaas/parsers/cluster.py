# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import inspect
import json

from ..cluster import Cluster
from .. import utils

def command(parent_parser):
    parser = parent_parser.add_parser(
        'cluster',
        help=inspect.getdoc(Cluster))

    subcommands = [
        cluster_ls,
        cluster_create,
        cluster_show,
        cluster_rm,
        cluster_start,
        cluster_stop,
        ]

    subparsers = parser.add_subparsers()
    for subcommand in subcommands:
        subcommand(subparsers)

def cluster_ls(parent_parser):
    def ls(client, args):
        cluster_list = client.cluster.ls()
        if not client.raw:
            for cluster_name in cluster_list:
                print('{name}'.format(name=cluster_name))

    parser = parent_parser.add_parser(
        'ls',
        help=inspect.getdoc(Cluster.ls))
    parser.set_defaults(func=ls)

def cluster_create(parent_parser):
    def create(client, args):
        raw_template = None
        if args.file:
            with open(args.file, 'r') as f:
                raw_template = f.read()
        else:
            raw_template = sys.stdin.read()
        client.cluster.create(
                cluster_name=args.name,
                template=json.loads(raw_template))

    parser = parent_parser.add_parser(
        'create',
        help=inspect.getdoc(Cluster.create))
    parser.set_defaults(func=create)
    parser.add_argument(
        'name',
        help="Name of the cluster to be used in later API calls")
    parser.add_argument(
        '--file',
        help="Specify a cluster creation template to use (default: stdin).")

def cluster_show(parent_parser):
    def show(client, args):
        for cluster_name in args.clusters:
            cluster_info = client.cluster.show(cluster_name, format=args.format)
            if not client.raw:
                if args.format is not None:
                    print(json.dumps(cluster_info, indent=2))
                else:
                    print("Service Alerts")
                    for alert_state, num_hosts in cluster_info['service_alerts'].items():
                        print('\t{0} - {1}'.format(alert_state, num_hosts))

                    print("Host Alerts")
                    for alert_state, num_hosts in cluster_info['host_alerts'].items():
                        print('\t{0} - {1}'.format(alert_state, num_hosts))

                    print("Services")
                    for service in cluster_info['services']:
                        print("\t" + service)

                    print("Hosts")
                    for host_name, host_components in cluster_info['hosts'].items():
                        print("\t" + host_name)
                        for host_component in host_components:
                            print("\t\t" + host_component)

    parser = parent_parser.add_parser(
        'show',
        help=inspect.getdoc(Cluster.show))
    parser.set_defaults(func=show)
    parser.add_argument(
        'clusters',
        nargs='+',
        help="Show basic information about cluster(s)")
    parser.add_argument(
        '-f',
        '--format',
        help="Export cluster in specified format (e.g. blueprint)")

def cluster_rm(parent_parser):
    def rm(client, args):
        for cluster_name in args.clusters:
            client.cluster.rm(cluster_name)

    parser = parent_parser.add_parser(
        'rm',
        help=inspect.getdoc(Cluster.rm))
    parser.set_defaults(func=rm)
    parser.add_argument(
        'clusters',
        nargs='+',
        help="Remove cluster from ambari (requires cluster to be stopped)")

def cluster_start(parent_parser):
    def start(client, args):
        for cluster_name in args.clusters:
            client.cluster.start(cluster_name)

    parser = parent_parser.add_parser(
        'start',
        help=inspect.getdoc(Cluster.start))
    parser.set_defaults(func=start)
    parser.add_argument(
        'clusters',
        nargs='+',
        help="Start all services in cluster")

def cluster_stop(parent_parser):
    def stop(client, args):
        for cluster_name in args.clusters:
            client.cluster.stop(cluster_name)

    parser = parent_parser.add_parser(
        'stop',
        help=inspect.getdoc(Cluster.stop))
    parser.set_defaults(func=stop)
    parser.add_argument(
        'clusters',
        nargs='+',
        help="Stop all services in cluster")

