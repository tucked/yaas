from __future__ import absolute_import
from __future__ import print_function

from . import utils

class Repo:
    """ Interact with Ambari stack repository configurations. """

    def __init__(self, client):
        self.client = client

    def ls(self):
        """ List all configured repositories. """
        response = self.client.request(
            'get',
            '/api/v1/stacks',
            params={'fields': 'versions/repository_versions/operating_systems/repositories/*'})
        res = response.json()

        repos = []
        for stack in res['items']:
            for version in stack['versions']:
                for repo_version in version['repository_versions']:
                    version = {
                        'stack_name': repo_version['RepositoryVersions']['stack_name'],
                        'stack_version': repo_version['RepositoryVersions']['stack_version'],
                        'repo_id': repo_version['RepositoryVersions']['id'],
                        'operating_systems': {}
                        }
                    for os in repo_version['operating_systems']:
                        version['operating_systems'][os["OperatingSystems"]["os_type"]] = []
                        for repo in os['repositories']:
                            version['operating_systems'][os["OperatingSystems"]["os_type"]].append(repo['Repositories']['base_url'])
                    repos.append(version)
        return repos

    def show(self, stack_name, stack_version, repo_id):
        """ List all configured repositories. """
        response = self.client.request(
            'get',
            '/api/v1/stacks/{0}/versions/{1}/repository_versions/{2}?fields=operating_systems/repositories/*'.format(
                stack_name, stack_version, repo_id))
        res = response.json()
        utils.remove_hrefs(res)
        return res

    def rm(self, stack_name, stack_version, repo_id):
        """ Delete specified repository. """
        response = self.client.request(
            'delete',
            '/api/v1/stacks/{0}/versions/{1}/repository_versions/{2}'.format(
                stack_name, stack_version, repo_id))

    def update(self, stack_name, stack_version, repo_id, repo):
        """ Update the specified repository. """
        response = self.client.request(
            'put',
            '/api/v1/stacks/{0}/versions/{1}/repository_versions/{2}'.format(
                stack_name, stack_version, repo_id))

    def add(self, stack_name, stack_version, repo):
        """ Add the specified repository. """
        response = self.client.request(
            'post',
            '/api/v1/stacks/{0}/versions/{1}/repository_versions/'.format(
                stack_name, stack_version))

    def generate(self, repository_version=None, display_name=None, os_types=[]):
        repo = {
                'RepositoryVersions': {
                    'repository_version': repository_version,
                    'display_name': display_name,
                },
                'operating_systems': [],
            }
        for os in os_types:
            repo['operating_systems'].append({
                'OperatingSystems': {
                    'os_type': os,
                    },
                'repositories': [
                    {
                        'Repositories' : {
                            'base_url' : '',
                            'repo_id' : '',
                            'repo_name' : '',
                            },
                        },
                    {
                        'Repositories' : {
                            'base_url' : '',
                            'repo_id' : '',
                            'repo_name' : '',
                            },
                        },
                    ],
                })
        return repo

