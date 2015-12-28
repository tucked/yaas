# coding: utf-8

""" Interact with registered hosts. """

from __future__ import absolute_import
from __future__ import print_function

import inspect
import pprint
import requests
import sys

from . import config
from . import utils


def ls():
    """ List all registered hosts. """
    response = requests.get(
        config.href('/api/v1/hosts'),
        **config.requests_opts())
    return [item['Hosts']['host_name'] for item in response.json()['items']]


def show(host_name):
    """ Show registered host info. """
    print(config.href('/api/v1/hosts/{host}'.format(host=host_name)))
    response = requests.get(
        config.href('/api/v1/hosts/{host}'.format(host=host_name)),
        **config.requests_opts())
    response.raise_for_status()
    raw_host_info = response.json()
    utils.remove_hrefs(raw_host_info)
    return raw_host_info
