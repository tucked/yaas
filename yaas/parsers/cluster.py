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

