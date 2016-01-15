# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import inspect

from ..repo import Repo
from .. import utils

def command(parent_parser):
  parser = parent_parser.add_parser(
      'repo',
      help=inspect.getdoc(Repo))

  subcommands = [
      ]

  subparsers = parser.add_subparsers()
  for subcommand in subcommands:
      subcommand(subparsers)

