# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import inspect

from ..service import Service
from .. import utils

def command(parent_parser):
  parser = parent_parser.add_parser(
      'service',
      help=inspect.getdoc(Service))

  subcommands = [
      ]

  subparsers = parser.add_subparsers()
  for subcommand in subcommands:
      subcommand(subparsers)

