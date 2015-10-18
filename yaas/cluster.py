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
        return [item['Clusters']['cluster_name'] for item in response.json()['items']]

    def create(self, cluster_name, template):
        """ Create an Ambari hadoop cluster. """
        self.client.request(
            'post',
            '/api/v1/clusters/{name}'.format(name=cluster_name),
            data=json.dumps(template))

    def show(self, cluster_name, format=None):
        """Show basic cluster information or export in a specified format"""
        if format is None:
            response = self.client.request(
                'get',
                '/api/v1/clusters/{name}'.format(name=cluster_name),
                params={'fields': 'alerts_summary,alerts_summary_hosts,hosts/host_components,services'})
            raw_resp = response.json()

            service_alerts = {}
            for alert_state, num_hosts in raw_resp['alerts_summary'].items():
                service_alerts[alert_state] = num_hosts

            host_alerts = {}
            for alert_state, num_hosts in raw_resp['alerts_summary_hosts'].items():
                host_alerts[alert_state] = num_hosts

            services = [service['ServiceInfo']['service_name'] for service in raw_resp['services']]

            hosts = {}
            for host in raw_resp['hosts']:
                host_name = host['Hosts']['host_name']
                hosts[host_name] = []
                for host_component in host['host_components']:
                    hosts[host_name].append(host_component['HostRoles']['component_name'])
            return {
                'service_alerts': service_alerts,
                'host_alerts': host_alerts,
                'hosts': hosts,
                'services': services,
                }
        else:
            response = self.client.request(
                'get',
                '/api/v1/clusters/{name}'.format(name=cluster_name),
                params={'format': format})
            raw_resp = response.json()
            utils.remove_hrefs(raw_resp)
            return raw_resp

    def destroy(self, cluster_name):
        """Delete cluster from ambari. Requires all services in cluster to be stopped"""
        self.client.request(
                'delete',
                '/api/v1/clusters/{name}'.format(name=cluster_name))

