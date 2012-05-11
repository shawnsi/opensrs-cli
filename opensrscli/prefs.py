#!/usr/bin/env python
import yaml
import copy

class Prefs(object):
  def __init__(self, yaml_prefs):
    """Read and parse the yaml preferences file provided"""
    self.raw_prefs = yaml.load(open(yaml_prefs, 'r'))

  @property
  def username(self):
    return self.raw_prefs['username']

  @property
  def private_key(self):
    return self.raw_prefs['private_key']

  @property
  def contact_set(self):
    """Convert the yaml contact_set into an OpenSRS compatible structure. This
    does a shallow copy of the default contact into each contact type first.  
    Then any contact type specific info overwrites the defaults."""
    contact_set = {}
    for contact in ['admin', 'owner', 'billing', 'tech']:
      contact_set[contact] = copy.copy(self.raw_prefs['contact_set']['default'])
      try:
        for attr, value in self.raw_prefs['contact_set'][contact].items():
          contact_set[contact][attr] = value
      except KeyError:
        continue
    return contact_set

  @property
  def register(self):
    register = self.raw_prefs['register']
    register['contact_set'] = self.contact_set
    return register

  @property
  def transfer(self):
    transfer = self.register
    transfer['reg_type'] = 'transfer'
    return transfer
