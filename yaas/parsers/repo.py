# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import inspect
import json
import sys

from ..repo import Repo
from .. import utils

def command(parent_parser):
    parser = parent_parser.add_parser(
        'repo',
        help=inspect.getdoc(Repo))

    subcommands = [
        repo_ls,
        repo_show,
        repo_rm,
        repo_add,
        repo_update,
        repo_generate,
        ]

    subparsers = parser.add_subparsers()
    for subcommand in subcommands:
        subcommand(subparsers)

def repo_ls(parent_parser):
    def ls(client, args):
        repo_versions = client.repo.ls()
        for repo_version in repo_versions:
            # TODO: things like build number or display name
            print("{0} {1} (id: {2})".format(
                repo_version['stack_name'],
                repo_version['stack_version'],
                repo_version['repo_id']))
            for os, repo_urls in repo_version['operating_systems'].items():
                print("  {0}".format(os))
                for repo_url in repo_urls:
                    print("    {0}".format(repo_url))

    parser = parent_parser.add_parser(
        'ls',
        help=inspect.getdoc(Repo.ls))
    parser.set_defaults(func=ls)

def repo_show(parent_parser):
    def show(client, args):
        raw_repo = client.repo.show(
            args.stack_name,
            args.stack_version,
            args.repo_id)
        print(json.dumps(raw_repo, indent=2))

    parser = parent_parser.add_parser(
        'show',
        help=inspect.getdoc(Repo.show))
    parser.set_defaults(func=show)
    parser.add_argument(
        'stack_name',
        help="Stack name (e.g. HDP)")
    parser.add_argument(
        'stack_version',
        help="Two-digit stack version (e.g. 2.3)")
    parser.add_argument(
        'repo_id',
        help="Repository id (e.g. 1)")

def repo_rm(parent_parser):
    def rm(client, args):
        client.repo.rm(args.stack_name, args.stack_version, args.repo_id)

    parser = parent_parser.add_parser(
        'rm',
        help=inspect.getdoc(Repo.rm))
    parser.set_defaults(func=rm)
    parser.add_argument(
        'stack_name',
        help="Stack name (e.g. HDP)")
    parser.add_argument(
        'stack_version',
        help="Two-digit stack version (e.g. 2.3)")
    parser.add_argument(
        'repo_id',
        help="Repository id (e.g. 1)")

def repo_add(parent_parser):
    def add(client, args):
        raw_repo = None
        if args.file:
            with open(args.file, 'r') as f:
                raw_repo = f.read()
        else:
            raw_repo = sys.stdin.read()

        client.repo.add(args.stack_name, args.stack_version, raw_repo)

    parser = parent_parser.add_parser(
        'add',
        help=inspect.getdoc(Repo.add))
    parser.set_defaults(func=add)
    parser.add_argument(
        'stack_name',
        help="Stack name (e.g. HDP)")
    parser.add_argument(
        'stack_version',
        help="Two-digit stack version (e.g. 2.3)")
    parser.add_argument(
        '-f',
        '--file',
        nargs='?',
        help="Add repository with given repo information")

def repo_update(parent_parser):
    def update(client, args):
        raw_repo = None
        if args.file:
            with open(args.file, 'r') as f:
                raw_repo = f.read()
        else:
            raw_repo = sys.stdin.read()

        client.repo.update(
            args.stack_name,
            args.stack_version,
            args.repo_id,
            raw_repo)

    parser = parent_parser.add_parser(
        'update',
        help=inspect.getdoc(Repo.update))
    parser.set_defaults(func=update)
    parser.add_argument(
        'stack_name',
        help="Stack name (e.g. HDP)")
    parser.add_argument(
        'stack_version',
        help="Two-digit stack version (e.g. 2.3)")
    parser.add_argument(
        'repo_id',
        help="Repo id (e.g. 1)")
    parser.add_argument(
        '-f',
        '--file',
        nargs='?',
        help="Add repository with given repo information")

def repo_generate(parent_parser):
    def generate(client, args):
        generated_repo = client.repo.generate(
            repository_version=args.repository_version,
            display_name=args.display_name,
            os_types=args.os_types)
        print(json.dumps(generated_repo, indent=2))

    parser = parent_parser.add_parser(
        'generate',
        help=inspect.getdoc(Repo.generate))
    parser.set_defaults(func=generate)
    parser.add_argument(
        '-r',
        '--repository-version',
        default=None,
        help="4 digit repository version (e.g. 2.3.0.0)")
    parser.add_argument(
        '-d',
        '--display-name',
        default=None,
        help="A unique name for this repository")
    parser.add_argument(
        '-o',
        '--os-types',
        nargs='*',
        default=[],
        help="OS family (e.g. redhat6)")
