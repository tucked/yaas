# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import inspect

from .. import host
from .. import config
from .. import utils

def define_subcommand(parent_parser):
  parser = parent_parser.add_parser(
      'host',
      help=inspect.getdoc(host))

  subcommands = [
      host_ls,
      host_show,
      ]

  subparsers = parser.add_subparsers()
  for subcommand in subcommands:
      subcommand(subparsers)

def host_ls(parent_parser):
    def ls(args):
        host_list = host.ls()
        if not config.raw:
            for host_name in host_list:
                print('{name}'.format(name=host_name))
    parser = parent_parser.add_parser(
        'ls',
        help=inspect.getdoc(host.ls))
    parser.set_defaults(func=ls)

def host_show(parent_parser):
    def show(args):
        for host_name in args.hosts:
            host_info = host.show(host_name)
            if not config.raw:
                print(
                    '[{state}] {host} ({ip}) - {status}'.format(
                        host=host_info['Hosts']['host_name'],
                        ip=host_info['Hosts']['ip'],
                        state=host_info['Hosts']['host_state'],
                        status=host_info['Hosts']['host_status']))
                if 'alerts' in host_info:
                    for alert in host_info['alerts']['detail']:
                        if alert['status'] != 'OK':
                            print(
                                '{indent}{service} {status} {desc}: {message}'.format(
                                    indent=' '*4,
                                    service=alert['service_name'],
                                    status=alert['status'],
                                    desc=alert['description'],
                                    message=alert['output']))
                if args.hardware:
                    print(
                        '{indent}{cohost_info}-core {memory}B {os} {rack}'.format(
                            indent=' '*4,
                            cohost_info=host_info['Hosts']['cpu_count'],
                            memory=host_info['Hosts']['total_mem'],
                            os=host_info['Hosts']['os_type'],
                            rack=host_info['Hosts']['rack_info']))
                    for disk in host_info['Hosts']['disk_info']:
                        print(
                            '{indent}{mount} {type} {percent} ({used}B/{size}B)'.format(
                                indent=' '*8,
                                mount=disk['mountpoint'],
                                type=disk['type'],
                                percent=disk['percent'],
                                used=disk['used'],
                                size=disk['size']))

    parser = parent_parser.add_parser(
        'show',
        help=inspect.getdoc(host.show))
    parser.set_defaults(func=show)
    parser.add_argument(
        '--hardware',
        action='store_true',
        default=False,
        help="Print hardware specs.")
    parser.add_argument(
            'hosts',
            nargs='+',
            help="host name(s) to show")

