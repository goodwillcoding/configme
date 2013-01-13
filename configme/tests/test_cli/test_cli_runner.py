# -*- coding: utf-8 -*-

import unittest


# --------------------------------------------------------------------------- #
class DummyLoggerFactory(object):

    name = None
    out = None
    err = None

    # ....................................................................... #
    def __init__(self, name, out, err):
        self.name = name
        self.out = out
        self.err = err

    # ....................................................................... #
    def to_out(self, message):
        self.out.write(message)

    # ....................................................................... #
    def to_err(self, message):
        self.err.write(message)

    # ....................................................................... #
    # setting logging aliases
    debug = info = to_out
    warn = warning = error = critical = to_err


# --------------------------------------------------------------------------- #
class DummyConfigurator(object):

    templates_path = None
    settings_path = None
    output_path = None

    # ....................................................................... #
    def __init__(self, templates_path, settings_path, output_path):
        self.templates_path = templates_path
        self.settings_path = settings_path
        self.output_path = output_path


# --------------------------------------------------------------------------- #
class DummyRole(object):

    config = None
    name = None
    suffix = None
    variables = None

    # ....................................................................... #
    def __init__(self, config, name, suffix='', variables=None):

        self.config = config
        self.name = name
        self.suffix = suffix

        # handle mutable defaults
        if variables is None:
            variables = {}

        self.variables = variables

    # ....................................................................... #
    def write_configs(self):
        return ['test_config_generation_output']


# --------------------------------------------------------------------------- #
class Test_cli_arguments_config_factory(unittest.TestCase):

    # ....................................................................... #
    def _callFUT(self, *args, **kwargs):
        from ..cli import cli_arguments_config_factory
        return cli_arguments_config_factory(*args, **kwargs)
