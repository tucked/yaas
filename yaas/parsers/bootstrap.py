# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import getpass
import inspect

from ..bootstrap import Bootstrap


def command(parent_parser):
    parser = parent_parser.add_parser(
        'bootstrap',
        help=inspect.getdoc(Bootstrap))

    subcommands = [
        bootstrap_agents,
        bootstrap_show,
        ]

    subparsers = parser.add_subparsers()
    for subcommand in subcommands:
        subcommand(subparsers)


def bootstrap_agents(parent_parser):

    """ Install and configure ambari-agent on specified hosts. """

    def agents(client, args):
        with open(args.ssh_key, 'r') as f:
            ssh_key = f.read()
        res = client.bootstrap.agents(
            hosts=args.hosts,
            sshKey=ssh_key,
            user=args.user,
            userRunAs=args.userRunAs)
        if not client.raw:
            print(
                'Request {id} {status} {log}'.format(
                    id=res['requestId'],
                    status=res['status'],
                    log=res['log']))

    parser = parent_parser.add_parser(
        'agents',
        help=inspect.getdoc(Bootstrap.agents))
    parser.set_defaults(func=agents)
    parser.add_argument(
        '-k', '--ssh-key',
        required=True,
        help="Specify the private SSH key for a public SSH key on the hosts.")
    parser.add_argument(
        '-u', '--user',
        default=getpass.getuser(),
        help="Specify the SSH user.")
    parser.add_argument(
        '-r', '--userRunAs',
        help="Specify the SSH user.")
    parser.add_argument(
        'host',
        nargs='+',
        help="Specify one or more hosts to bootstrap agents on.")


def bootstrap_show(parent_parser):

    """ Show information about bootstrap requests. """

    def show(client, args):
        for req in args.id:
            res = client.bootstrap.show(requestId=req)
            if not client.raw:
                print(
                    'Request {id} {status}'.format(
                        id=req,
                        status=res['status']))
                if args.log:
                    print(('\n'+res['log']).replace('\n', '\n'+(' '*4)))
                for host_status in res['hostsStatus']:
                    print(
                        '{indent}{hostname} {status} (status: {code})'.format(
                            indent=' '*4,
                            hostname=host_status['hostName'],
                            status=host_status['status'],
                            code=host_status['statusCode']))
                    if args.log:
                        print(('\n'+host_status['log']).replace('\n', '\n'+(' '*8)))

    parser = parent_parser.add_parser(
        'show',
        help=inspect.getdoc(Bootstrap.show))
    parser.set_defaults(func=show)
    parser.add_argument(
        '-l', '--log',
        action='store_true', default=False,
        help="Show bootstrap logs.")
    parser.add_argument(
        'id',
        nargs='+',
        help="Specify one or more bootstrap request IDs to show.")

