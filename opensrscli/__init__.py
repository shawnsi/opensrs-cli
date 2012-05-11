#!/usr/bin/env python
import cli.log
from opensrs import OpenSRS
from prefs import Prefs
import string
import copy
import os

class OpenSRSApp(cli.log.LoggingApp):
  
  @property
  def name(self):
    """Hacking the name to match the console scripts"""
    decorated_name = super(OpenSRSApp, self).name
    return 'opensrs-%s' % (string.replace(decorated_name, '_', '-'))

  def pre_run(self):
    """Setup our OpenSRS connection"""
    super(OpenSRSApp, self).pre_run()
    self.prefs = Prefs(self.params.preferences)
    self.auth_dict = {
        'username': self.prefs.username,
        'private_key': self.prefs.private_key,
        'test': self.params.test,
    }
    self.opensrs = OpenSRS(**self.auth_dict)

  def setup(self):
    """Add parameters that all OpenSRS cli applications will need"""
    super(OpenSRSApp, self).setup()
    self.add_param('-p', '--preferences', help='OpenSRS preferences yaml file', default='%s/.opensrs/prefs' % os.getenv('HOME'), type=str)
    self.add_param('-t', '--test', help='use OpenSRS test environment', default=False, action='store_true')
    self.add_param('domain', nargs='*', help='domains to perform command on')

@OpenSRSApp
def balance(app):
  response = app.opensrs.balance()
  if response['is_success']:
    print 'OpenSRS Balance: %s' % response['attributes']['balance']
  else:
    print response

@OpenSRSApp
def check_transfer(app):
  for domain in app.params.domain:
    response = app.opensrs.check_transfer(domain)
    if response['is_success']:
      print '%s: %s' % (domain, int(response['attributes']['transferrable']) and 'Transferrable' or 'Not Transferrable')

@OpenSRSApp
def transfer(app):
  for domain in app.params.domain:
    attrs = app.prefs.transfer
    attrs['domain'] = domain
    response = app.opensrs.post("sw_register", "domain", attrs)
    if response['is_success']:
      print '%s: %s' % (domain, 'Transfer initiated')
    else:
      print '%s: %s' % (domain, 'Failure')
