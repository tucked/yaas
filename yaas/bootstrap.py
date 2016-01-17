# coding: utf-8


class Bootstrap:

    """ Interact with agent bootstrap requests. """

    def __init__(self, client):
        self.client = client

    def agents(self, hosts, sshKey, user, userRunAs=None):
        """ Add a blueprint to the Ambari server. """
        req = {
            'hosts': hosts,
            'sshKey': sshKey,
            'user': user,
            }
        if userRunAs is not None:
            req['userRunAs'] = userRunAs
        response = self.client.request(
            'post',
            '/api/v1/bootstrap',
            json=req)
        return response.json()

    def show(self, requestId):
        """ Show a blueprint. """
        response = self.client.request(
            'get',
            '/api/v1/bootstrap/{requestId}'.format(requestId=requestId))
        return response.json()

