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

