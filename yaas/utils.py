# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

def remove_hrefs(el):
    if type(el) is dict:
        if 'href' in el:
            del el['href']
        for k, v in el.items():
            remove_hrefs(v)
    elif type(el) is list:
        for array_el in el:
            remove_hrefs(array_el)

def print_field(k, v, indent=0):
    k = str(k).replace('_', ' ')
    if not v:
        return
    elif type(v) is dict:
        print('{indent}{key}'.format(indent=' '*indent, key=k))
        for key, value in v.items():
            print_field(k=key, v=value, indent=indent+4)
    elif type(v) is list:
        print('{indent}{key}'.format(indent=' '*indent, key=k))
        for i in range(len(v)):
            print_field(k=i, v=v[i], indent=indent+4)
    else:
        print(
            '{indent}{key}: {value}'.format(
                indent=' '*indent,
                key=k,
                value=v))

