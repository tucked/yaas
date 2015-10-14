# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import inspect

from ..cluster import Cluster
from .. import utils

def command(parent_parser):
    parser = parent_parser.add_parser(
        'cluster',
        help=inspect.getdoc(Cluster))

    subcommands = [
        cluster_ls,
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

