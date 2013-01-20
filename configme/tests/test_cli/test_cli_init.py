# -*- coding: utf-8 -*-

"""
Test CLI initialization and configuration.
"""

import unittest


# --------------------------------------------------------------------------- #
class DummyCliArgumentParser(object):

    description = ''

    _arguments = []

    # ....................................................................... #
    def __init__(self, description):
        self._arguments = []
        self.description = description

    # ....................................................................... #
    def add_argument(
        self,
        short_opt,
        long_opt,
        help,
        required=False,
        action='store',
        nargs=None,
        default=None,
        type=None
    ):

        argument = {
            'short_opt': short_opt,
            'long_opt': long_opt,
            'help': help,
            'required': required,
            'action': action,
            'nargs': nargs,
            'default': default,
            'type': type
            }

        self._arguments.append(argument)

    # ....................................................................... #
    class ArgListToDictAction(object):
        pass

    # ....................................................................... #
    @staticmethod
    def split_argument(self):  # pragma: no cover
        pass


# --------------------------------------------------------------------------- #
class Test_cli_configured_argument_parser(unittest.TestCase):

    # ....................................................................... #
    def _callFUT(self, *args, **kwargs):
        from ...cli import configured_argument_parser
        return configured_argument_parser(*args, **kwargs)

    # ....................................................................... #
    def test_configuration(self):

        test_configuration = [
            {'short_opt': '-t',
             'long_opt': '--templates-path',
             'required': True,
             'help': 'Path to configuration templates folder.',
             'action': 'store',
             'nargs': None,
             'default': None,
             'type': None,
            },
            {'short_opt': '-s',
             'long_opt': '--settings-path',
             'required': True,
             'help': 'Path to settings folder.',
             'action': 'store',
             'nargs': None,
             'default': None,
             'type': None,
            },
            {'short_opt': '-o',
             'long_opt': '--output-path',
             'required': True,
             'help': 'Path to output folder.',
             'action': 'store',
             'nargs': None,
             'default': None,
             'type': None,
            },
            {'short_opt': '-r',
             'long_opt': '--role-name',
             'required': True,
             'help': 'Role name.',
             'action': 'store',
             'nargs': None,
             'default': None,
             'type': None,
            },
            {'short_opt': '-u',
             'long_opt': '--role-suffix',
             'required': False,
             'help': 'Role suffix.',
             'action': 'store',
             'nargs': None,
             'default': '',
             'type': None,
            },
            {'short_opt': '-b',
             'long_opt': '--role-variables',
             'required': False,
             'help':
                 'Variables that will interpolated into the settings files.',
             'action': DummyCliArgumentParser.ArgListToDictAction,
             'nargs': '+',
             'default': {},
             'type': DummyCliArgumentParser.split_argument,
            },
        ]

        parser = self._callFUT(_argument_parser_factory=DummyCliArgumentParser)

        self.assertListEqual(test_configuration, parser._arguments)


# --------------------------------------------------------------------------- #
def dummy_clu_runner_factory(run_return=None):

    class DummyCliRunner(object):

        __run_return = None

        # ....................................................................#
        def __init__(self, *args, **kwargs):
            self.__run_return = run_return

        # ....................................................................#
        def run(self):
            return self.__run_return

    return DummyCliRunner


# --------------------------------------------------------------------------- #
class Test_main(unittest.TestCase):

    # ....................................................................... #
    def _callFUT(self, *args, **kwargs):
        from ...cli import main
        return main(*args, **kwargs)

    # ....................................................................... #
    def test_main(self):

        test_return = 'test_run_method_return'
        dummy_cli_runner = dummy_clu_runner_factory(test_return)

        self.assertEqual(self._callFUT(dummy_cli_runner), test_return)
