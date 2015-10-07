# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import pprint
import requests

# These default configs are overriden based on
# command line arguments or environment variables.

scheme = 'http'
server = None   # Must be overriden
port = 8080
username = 'admin'
password = 'admin'
command = None


def request(endpoint):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            r = requests.get(
                '{scheme}://{server}:{port}{path}'.format(
                    scheme=scheme,
                    server=server,
                    port=port,
                    path=endpoint),
                auth=(username, password),
                headers={'X-Requested-By': 'Ambari'})
            if command.verbose:
                pprint.pprint(r.json())
            else:
                fn(*args, response=r, **kwargs)
        return wrapper
    return decorator
