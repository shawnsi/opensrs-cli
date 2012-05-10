#!/usr/bin/env python
import cli.log
from opensrs import OpenSRS
import string

class OpenSRSApp(cli.log.LoggingApp):
  
  @property
  def name(self):
    """Hacking the name to match the console scripts"""
    decorated_name = super(OpenSRSApp, self).name
    return 'opensrs-%s' % (string.replace(decorated_name, '_', '-'))

  def pre_run(self):
    """Setup our OpenSRS connection"""
    super(OpenSRSApp, self).pre_run()
    self.auth_dict = {
        'username': self.params.username,
        'private_key': open(self.params.privatekey).read().strip(),
        'test': self.params.test,
    }
    self.opensrs = OpenSRS(**self.auth_dict)

  def setup(self):
    """Add parameters that all OpenSRS cli applications will need"""
    super(OpenSRSApp, self).setup()
    self.add_param('-u', '--username', help='OpenSRS username', default=None, type=str, required=True)
    self.add_param('-p', '--privatekey', help='OpenSRS privatekey file', default=None, type=str, required=True)
    self.add_param('-t', '--test', help='use OpenSRS test environment', default=False, action='store_true')
    self.add_param('domain', nargs='*', help='domains to perform command on')

@OpenSRSApp
def balance(app):
  print 'OpenSRS Balance: %s' % app.opensrs.balance()
  
@OpenSRSApp
def check_transfer(app):
  for domain in app.params.domain:
    print 'Checking %s' % domain
    print app.opensrs.check_transfer(domain)
