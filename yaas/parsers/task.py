# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import inspect

from ..task import Task
from .. import utils

def command(parent_parser):
  parser = parent_parser.add_parser(
      'task',
      help=inspect.getdoc(Task))

  subcommands = [
      ]

  subparsers = parser.add_subparsers()
  for subcommand in subcommands:
      subcommand(subparsers)

