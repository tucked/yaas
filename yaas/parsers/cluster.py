# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import inspect

from .. import cluster
from .. import config
from .. import utils

def define_subcommand(parent_parser):
  parser = parent_parser.add_parser(
      'cluster',
      help=inspect.getdoc(cluster))

  subcommands = [
      ]

  subparsers = parser.add_subparsers()
  for subcommand in subcommands:
      subcommand(subparsers)

