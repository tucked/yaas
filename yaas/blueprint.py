# coding: utf-8

""" Interact with Ambari blueprints. """

from __future__ import absolute_import
from __future__ import print_function

import json
import pprint
import requests
import sys

from . import config
from . import utils

def add(blueprint, blueprint_name, validate_topology=True):
    """ Add a blueprint to the Ambari server. """
    response = requests.post(
        config.href(
            '/api/v1/blueprints/{name}'.format(name=blueprint_name)),
        data=json.dumps(blueprint),  # `json=blueprint` would be better, but it doesn't work!
        params={'validate_topology': validate_topology},
        **config.requests_opts())

    response.raise_for_status()

def ls():
    """ List all blueprints stored on the Ambari server. """
    response = requests.get(
        config.href('/api/v1/blueprints'),
        **config.requests_opts())

    response.raise_for_status()
    return [item['Blueprints']['blueprint_name'] for item in response.json()['items']]


def rm(blueprint_name):
    """ Remove a blueprint form the server. """
    response = requests.delete(
        config.href('/api/v1/blueprints/{name}'.format(name=blueprint_name)),
        **config.requests_opts())

    response.raise_for_status()


def show(blueprint_name):
    """ Show a blueprint. """
    response = requests.get(
        config.href('/api/v1/blueprints/{name}'.format(name=blueprint_name)),
        **config.requests_opts())
    response.raise_for_status()
    raw_blueprint = response.json()
    utils.remove_hrefs(raw_blueprint)
    return raw_blueprint
