# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import json

from . import utils

class Blueprint:
    """ Interact with Ambari blueprints. """

    def __init__(self, client):
        self.client = client

    def add(self, blueprint, blueprint_name, validate_topology=True):
        """ Add a blueprint to the Ambari server. """
        self.client.request(
            'post',
            '/api/v1/blueprints/{name}'.format(name=blueprint_name),
            data=json.dumps(blueprint),  # `json=blueprint` would be better, but it doesn't work!
            params={'validate_topology': validate_topology})

    def ls(self):
        """ List all blueprints stored on the Ambari server. """
        response = self.client.request('get', '/api/v1/blueprints')
        return [item['Blueprints']['blueprint_name'] for item in response.json()['items']]


    def rm(self, blueprint_name):
        """ Remove a blueprint form the server. """
        self.client.request(
            'delete',
            '/api/v1/blueprints/{name}'.format(name=blueprint_name))

    def show(self, blueprint_name):
        """ Show a blueprint. """
        response = self.client.request(
            'get',
            '/api/v1/blueprints/{name}'.format(name=blueprint_name))
        raw_blueprint = response.json()
        utils.remove_hrefs(raw_blueprint)
        return raw_blueprint
