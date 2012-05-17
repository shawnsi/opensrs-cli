#!/usr/bin/env python
from prefs import Prefs
from opensrs import OpenSRS
import argparse
import os

class CLI(object):
    """
    Simple decorator class to create argparse based cli commands.
    """

    entry_points = []

    def __init__(self, func):
        """
        Decorates the supplied function and sets up the argparse parser.

        Keyword arguments:
        func -- the function to be decorated
        """
        self.func = func
        self.prog = 'opensrs-%s' % func.func_name
        self.entry_points.append('%s = opensrscli:%s.run' % (self.prog, func.func_name))
        self.parser = argparse.ArgumentParser(prog=self.prog)
        self.parser.add_argument('-p', '--preferences', help='OpenSRS preferences yaml file',
            default='%s/.opensrs/prefs' % os.getenv('HOME'), type=str)
        self.parser.add_argument('-t', '--test', help='use OpenSRS test environment',
            default=False, action='store_true')
        self.add_argument = self.parser.add_argument

    def run(self):
        """
        Sets up the OpenSRS connection and runs the decorated function.
        """
        self.args = self.parser.parse_args()
        self.prefs = Prefs(self.args.preferences)
        self.auth_dict = {
            'username': self.prefs.username,
            'private_key': self.prefs.private_key,
            'test': self.args.test,
        }
        self.opensrs = OpenSRS(**self.auth_dict)
        self.func(self)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
