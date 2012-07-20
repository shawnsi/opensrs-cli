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
        print

check_transfer.add_argument('domain', nargs='*', help='domains to perform command on')

@CLI
def get_nameservers(cli):
    """
    Returns nameservers for a domain
    """
    for domain in cli.args.domain:
        attrs = {
            'domain': domain,
            'type': 'nameservers',
        }
        response = cli.opensrs.post("get", "domain", attrs)
        try:
            nameservers_dict_list = response['attributes']['nameserver_list']
            nameserver_list = map(
                lambda d: d['name'],
                nameservers_dict_list
            )
            print '%s:\n%s' % (domain, '\n'.join(nameserver_list))
        except KeyError:
            print '%s: %s' % (domain, response)
        print

get_nameservers.add_argument('domain', nargs='*', help='domains to perform command on')

@CLI
def set_nameservers(cli):
    for domain in cli.args.domain:
        attrs = {
            'domain': domain,
            'type': 'nameservers',
        }
        response = cli.opensrs.post("get", "domain", attrs)
        try:
            nameservers_dict_list = response['attributes']['nameserver_list']
            nameserver_list = map(
                lambda d: d['name'],
                nameservers_dict_list
            )
            attrs = {
                'domain': domain,
                'op_type': 'add_remove',
                'remove_ns': nameserver_list,
                'add_ns': [
                    'PDNS1.ULTRADNS.NET',
                    'PDNS2.ULTRADNS.NET',
                    'PDNS3.ULTRADNS.ORG',
                    'PDNS4.ULTRADNS.ORG',
                    'PDNS5.ULTRADNS.INFO',
                    'PDNS6.ULTRADNS.CO.UK',
                ],
            }
            response = cli.opensrs.post('advanced_update_nameservers', 'domain', attrs)
            print '%s: %s' % (domain, response['response_text'])
        except KeyError:
            print '%s: %s' % (domain, response)
        print

set_nameservers.add_argument('domain', nargs='*', help='domains to perform command on')

@CLI
def transfer(cli):
    """
    Transfers domains based on OpenSRS preferences
    """
    for domain in cli.args.domain:
        attrs = cli.prefs.transfer
        attrs['domain'] = domain
        response = cli.opensrs.post("sw_register", "domain", attrs)
        if response['is_success']:
            print '%s: %s' % (domain, 'Transfer initiated')
        else:
            print '%s: %s' % (domain, response)
        print

transfer.add_argument('domain', nargs='*', help='domains to perform command on')

@CLI
def lock(cli):
    """
    Locks a domain
    """
    for domain in cli.args.domain:
        attrs = {
            'affect_domains': 0,
            'domain_name': domain,
            'data': 'status',
            'lock_state': 1,
        }
        response = cli.opensrs.post('modify', 'domain', attrs)
        print '%s: %s' % (domain, response['response_text'])

lock.add_argument('domain', nargs='*', help='domains to perform command on')

@CLI
def unlock(cli):
    """
    Unlocks a domain
    """
    for domain in cli.args.domain:
        attrs = {
            'affect_domains': 0,
            'domain_name': domain,
            'data': 'status',
            'lock_state': 0,
        }
        response = cli.opensrs.post('modify', 'domain', attrs)
        print '%s: %s' % (domain, response['response_text'])

unlock.add_argument('domain', nargs='*', help='domains to perform command on')

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
