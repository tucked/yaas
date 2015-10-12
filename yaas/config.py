# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

# These default configs are overriden by environment variables.
scheme = 'http'
server = 'localhost'
port = 8080
username = 'admin'
password = 'admin'
args = None


def print_request_and_response(res, *args, **kwargs):
    print("Request:", res.request.__dict__)
    print("Response:", res.__dict__)


def requests_opts():
    opts = {
        'auth': (username, password),
        'headers': {'X-Requested-By': 'Ambari'},
        }

    if args.debug:
        opts['hooks'] = {
            'response': print_request_and_response,
            }

    return opts


def href(endpoint):
    return '{scheme}://{server}:{port}{path}'.format(
        scheme=scheme,
        server=server,
        port=port,
        path=endpoint)
