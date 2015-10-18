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

def print_field(k, v, indent=0):
    k = str(k).replace('_', ' ')
    if type(v) is dict:
        print('{indent}{key}:'.format(indent=' '*indent, key=k))
        for key, value in v.items():
            print_field(k=key, v=value, indent=indent+4)
    elif type(v) is list:
        print('{indent}{key}:'.format(indent=' '*indent, key=k))
        for i in range(len(v)):
            print_field(k=i, v=v[i], indent=indent+4)
    else:
        print(
            '{indent}{key}: {value}'.format(
                indent=' '*indent,
                key=k,
                value=' '.join(v) if type(v) is list else v))

