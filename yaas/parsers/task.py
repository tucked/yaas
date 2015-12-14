# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import inspect

from .. import task
from .. import config
from .. import utils

def define_subcommand(parent_parser):
  parser = parent_parser.add_parser(
      'task',
      help=inspect.getdoc(task))

  subcommands = [
      ]

  subparsers = parser.add_subparsers()
  for subcommand in subcommands:
      subcommand(subparsers)

