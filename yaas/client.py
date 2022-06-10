# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import json
import pprint
import requests

from .bootstrap import Bootstrap
from .cluster import Cluster
from .host import Host
from .repo import Repo
from .service import Service
from .task import Task
from . import utils

# These default configs are overriden by environment variables
# when using command line yaas and can be overriden programmatically
class Client:
    """ Client for interacting with the Ambari API """
    def __init__(
            self,
            scheme='http',
            server='localhost',
            port=8080,
            username='admin',
            password='admin',
            raw=False,
            debug=False):
        self.scheme = scheme
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.raw = raw
        self.debug = debug

        self.bootstrap = Bootstrap(self)
        self.cluster = Cluster(self)
        self.host = Host(self)
        self.repo = Repo(self)

    def blueprint_add(self, blueprint_name, blueprint, validate_topology=True):
        self.request(
            'post',
            '/api/v1/blueprints/{name}'.format(name=blueprint_name),
            data=json.dumps(blueprint.serialize()),  # `json=blueprint` would be better, but it doesn't work!
            params={'validate_topology': validate_topology})

    def blueprint_list(self):
        response = self.request('get', '/api/v1/blueprints')
        return [item['Blueprints']['blueprint_name'] for item in response.json()['items']]


    def blueprint_remove(self, blueprint_name):
        self.request(
            'delete',
            '/api/v1/blueprints/{name}'.format(name=blueprint_name))

    def blueprint_get(self, blueprint_name):
        response = self.request(
            'get',
            '/api/v1/blueprints/{name}'.format(name=blueprint_name))
        return Blueprint(response.json())

    def request(self, method, path, *args, **kwargs):
        """
        Provides a thin wrapper around the requests module
        to make a request for a given HTTP method and path
        """
        for key, value in self._requests_opts().items():
            if key not in kwargs:
                kwargs[key] = value

        func = getattr(requests, method.lower())
        response = func(self._href(path), *args, **kwargs)
        response.raise_for_status()
        return response

    def _requests_opts(self):
        def response_hook(res, *args, **kwargs):
            if self.debug:
                print("Request:", pprint.pprint(res.request.__dict__))
                print("Response:", pprint.pprint(res.__dict__))
            if self.raw:
                raw_resp = res.json()
                utils.remove_hrefs(raw_resp)
                print(json.dumps(raw_resp, indent=2))

        opts = {
                'auth': (self.username, self.password),
                'headers': {'X-Requested-By': 'Ambari'},
                'hooks': dict(response=response_hook)
                }

        return opts

    def _href(self, endpoint):
        return '{scheme}://{server}:{port}{path}'.format(
                scheme=self.scheme,
                server=self.server,
                port=self.port,
                path=endpoint)

