#!/usr/bin/env python

import distribute_setup
distribute_setup.use_setuptools()

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'opensrscli',
    version = '0.0.1',
    author = 'Shawn Siefkas',
    author_email = 'shawn.siefkas@meredith.com',
    description = 'A CLI for OpenSRS reseller accounts',
    license = 'BSD',
    keywords = 'opensrs',
    url = 'http://pypi.python.org/opensrscli',
    packages=['opensrscli'],
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
    ],
    install_requires = {
        'pyCLI': ["pycli"],
        'PyYAML': ["PyYAML"],
        'OpenSRS': ["OpenSRS"],
    },
    entry_points = {
        'console_scripts': [
            'opensrs-balance = opensrscli:balance.run',
            'opensrs-check-transfer = opensrscli:check_transfer.run',
            'opensrs-transfer = opensrscli:transfer.run',
        ],
    }
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
