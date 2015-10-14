# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function

import json

from . import utils

class Cluster:
    """ Interact with an Ambari-managed hadoop cluster """

    def __init__(self, client):
        self.client = client

    def ls(self):
        """ List all clusters. """
        response = self.client.request('get', '/api/v1/clusters')
        return [item['Cluster']['cluster_name'] for item in response.json()['items']]

    def create(self, cluster_name, template):
        """ Create an Ambari hadoop cluster. """
        self.client.request(
                'post',
                '/api/v1/clusters/{name}'.format(name=cluster_name),
                data=json.dumps(template))

