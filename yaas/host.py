# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

from . import utils

class Host:
    """ Interact with registered hosts. """

    def __init__(self, config):
        self.config = config

    def ls(self):
        """ List all registered hosts. """
        response = self.config.request('get', '/api/v1/hosts')
        return [item['Hosts']['host_name'] for item in response.json()['items']]


    def show(self, host_name):
        """ Show registered host info. """
        response = self.config.request('get', '/api/v1/hosts/{host}'.format(host=host_name))
        raw_host_info = response.json()
        utils.remove_hrefs(raw_host_info)
        return raw_host_info

