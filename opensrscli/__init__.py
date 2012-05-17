#!/usr/bin/env python
from parser import CLI

@CLI
def balance(cli):
    """
    Returns OpenSRS balance
    """
    response = cli.opensrs.balance()
    try:
        print response['attributes']['balance']
    except KeyError:
        print response

@CLI
def check_transfer(cli):
    """
    Returns transfer state of domain
    """
    for domain in cli.args.domain:
        response = cli.opensrs.check_transfer(domain)
        try:
            state = int(response['attributes']['transferrable']) and 'Transferrable' or 'Not Transferrable'
            print '%s: %s' % (domain, state)
        except KeyError:
            print '%s: %s' % (domain, response)

check_transfer.add_argument('domain', nargs='*', help='domains to perform command on')

@CLI
def transfer(cli):
    """
    Transfers domains based on OpenSRS preferences
    """
    for domain in cli.args.domain:
        attrs = cli.prefs.transfer
        attrs['domain'] = domain
        response = app.opensrs.post("sw_register", "domain", attrs)
        if response['is_success']:
            print '%s: %s' % (domain, 'Transfer initiated')
        else:
            print '%s: %s' % (domain, response)

transfer.add_argument('domain', nargs='*', help='domains to perform command on')

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
