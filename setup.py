# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2008-2011 Michael R.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
###############################################################################

import os
import sys

from setuptools import setup
from setuptools import find_packages

# name and version
from configme.version import PACKAGE_NAME
from configme.version import PACKAGE_VERSION_FULL
from configme.version import PACKAGE_DESC
from configme.version import PACKAGE_URL
from configme.version import PACKAGE_LICENSE
from configme.version import PACKAGE_AUTHOR

# py version detection
py_version = sys.version_info[:2]
PY3 = py_version[0] == 3

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

# install requires
install_requires = [
    'Jinja2',
    ]

# install requires: argparse is not included untill python 2.7 or 3.2
if py_version < (2, 7) or (PY3 and py_version < (3, 2)):
    install_requires.append('argparse')

# testing requires
tests_require = [
    ]

# testing extras are used in a command
testing_extras = tests_require + [
    'nose',
    'coverage',
    'nosexcover',
    'virtualenv',  # for scaffolding tests
    'flake8',
    'ipython',
    'ipdb'
    ]

# documentation generation requires
docs_extras = [
    'Sphinx',
    ]


def main():

    setup(
        name=PACKAGE_NAME,
        version=PACKAGE_VERSION_FULL,
        description=PACKAGE_DESC,
        long_description=README + '\n\n' + CHANGES,
        classifiers=[
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
            "Environment :: Console",
            "Topic :: System :: Systems Administration",
            "License :: Repoze Public License",
            ],
        keywords='config',
        author=PACKAGE_AUTHOR,
        author_email="me@example.com",
        url=PACKAGE_URL,
        license=PACKAGE_LICENSE,
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=install_requires,
        extras_require={
            'testing': testing_extras,
            'docs': docs_extras,
            },
        tests_require=tests_require,
        test_suite="configme.tests",
        entry_points={'console_scripts': ['configme = configme.cli:main']}
        )

if __name__ == '__main__':
    main()
