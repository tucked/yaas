# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import collections

class Configuration(collections.defaultdict):
    def __init__(self):
        super(Configuration, self).__init__(dict)

    @classmethod
    def parse(cls, raw):
        ret = cls()
        for config_block in raw:
            for name, configs in config_block.items():
                ret[name].update(configs)
        return ret

    def serialize(self):
        ret = []
        for name, configs in self.items():
            ret.append({name: configs})
        return ret

class HostGroup(object):
    def __init__(self, name, components, cardinality=None, configuration=None):
        self.name = name
        self.components = components
        self.cardinality = cardinality
        self.configuration = configuration

    @classmethod
    def parse(cls, raw):
        fields = {
            'name': raw['name'],
            'components': [obj['name'] for obj in raw['components']],
        }

        if 'cardinality' in raw:
            fields['cardinality'] = int(raw['cardinality'])

        if 'configurations' in raw:
            fields['configuration'] = Configuration.parse(raw['configurations'])

        return cls(**fields)

    def serialize(self):
        components = [{'name': c} for c in self.components]
        ret = {"name": self.name, "components": components}

        if self.configuration is not None:
            ret['configurations'] = self.configuration.serialize()

        if self.cardinality is not None:
            ret['cardinality'] = self.cardinality

        return ret

class Security(object):
    def __init__(self, security_type, kerberos_descriptor=None, kerberos_descriptor_reference=None):
        self.type = security_type
        self.kerberos_descriptor = kerberos_descriptor
        self.kerberos_descriptor_reference = kerberos_descriptor_reference

    @classmethod
    def parse(cls, raw):
        fields = {
            'security_type': raw['type'],
            'kerberos_descriptor': raw.get('kerberos_descriptor'),
            'kerberos_descriptor_reference': raw.get('kerberos_descriptor_reference'),
        }

        return cls(**fields)

    def serialize(self):
        ret = {"type": self.type}

        if self.kerberos_descriptor is not None:
            ret['kerberos_descriptor'] = self.kerberos_descriptor

        if self.kerberos_descriptor_reference is not None:
            ret['kerberos_descriptor_reference'] = self.kerberos_descriptor_reference

        return ret

class Blueprint(object):
    def __init__(self,
                 stack_name,
                 stack_version,
                 host_groups,
                 blueprint_name=None,
                 security=None,
                 configuration=None):
        # pylint: disable=too-many-arguments

        self.stack_name = stack_name
        self.stack_version = stack_version
        self.host_groups = host_groups
        self.blueprint_name = blueprint_name
        self.security = security
        self.configuration = configuration

    @classmethod
    def parse(cls, raw):
        fields = {
            'stack_name': raw['Blueprints']['stack_name'],
            'stack_version': raw['Blueprints']['stack_version'],
            'host_groups': [HostGroup.parse(group) for group in raw['host_groups']],
            'blueprint_name': raw['Blueprints'].get('blueprint_name'),
        }

        if 'security' in raw['Blueprints']:
            fields['security'] = Security.parse(raw['Blueprints']['security'])

        if 'configurations' in raw:
            fields['configuration'] = Configuration.parse(raw['configurations'])

        return cls(**fields)

    def serialize(self):
        ret = {
            'Blueprints': {
                'stack_name': self.stack_name,
                'stack_version': self.stack_version,
            },
            'host_groups': [hg.serialize() for hg in self.host_groups],
        }

        if self.blueprint_name is not None:
            ret['Blueprints']['blueprint_name'] = self.blueprint_name

        if self.security is not None:
            ret['Blueprints']['security'] = self.security.serialize()

        if self.configuration is not None:
            ret['configurations'] = self.configuration.serialize()

        return ret

