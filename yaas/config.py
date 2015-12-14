# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import json

from . import utils

# These default configs are overriden by environment variables
# when using command line yaas and can be overriden programmatically
scheme = 'http'
server = 'localhost'
port = 8080
username = 'admin'
password = 'admin'

raw = False
debug = False

def requests_opts():
    def response_hook(res, *args, **kwargs):
        if debug:
            print("Request:", res.request.__dict__)
            print("Response:", res.__dict__)
        if raw:
          raw_resp = res.json()
          utils.remove_hrefs(raw_resp)
          print(json.dumps(raw_resp, indent=2))

    opts = {
        'auth': (username, password),
        'headers': {'X-Requested-By': 'Ambari'},
        'hooks': dict(response=response_hook)
        }

    return opts

def href(endpoint):
    return '{scheme}://{server}:{port}{path}'.format(
        scheme=scheme,
        server=server,
        port=port,
        path=endpoint)

