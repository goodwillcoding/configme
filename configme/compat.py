# -*- coding: utf-8 -*-

"""
Compatability Module.
"""

import os

# ........................................................................... #
# set the WIN and POSIX flags
POSIX = os.name == 'posix'
WIN = os.name == 'nt'

# ........................................................................... #
# in py2 io.StringIO does not behave like py3 io.StringIO
# but instead matches behaviour of StringIO.StringIO
# as such we import appropriately
try:
    from StringIO import StringIO
except ImportError:  # pragma: no cover
    from io import StringIO  # NOQA
