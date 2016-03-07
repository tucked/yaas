# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

def remove_key_recursively(el, key):
    if type(el) is dict:
        if key in el:
            del el[key]
        for k, v in el.items():
            remove_key_recursively(v, key)
    elif type(el) is list:
        for array_el in el:
            remove_key_recursively(array_el, key)

def remove_hrefs(el):
    remove_key_recursively(el, 'href')

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

