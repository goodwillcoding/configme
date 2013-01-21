# -*- coding: utf-8 -*-

"""
Test CLI initialization and configuration.
"""

from unittest import TestCase


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
class Test_cli_configured_argument_parser(TestCase):

    # ....................................................................... #
    def _callFUT(self, *args, **kwargs):
        from ..cli import configured_argument_parser
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
class Test_cli_logger_factory(TestCase):

    # ....................................................................... #
    def setUp(self):
        from ..compat import StringIO
        self.out = StringIO()
        self.err = StringIO()
        self.name = 'test_logger_name_ultrices'

    # ....................................................................... #
    def tearDown(self):
        self.out.close()
        self.err.close()
        # super bad and ugly hack but we need clean up after the logging
        # module
        # logging module is a singleton and there is no "legal" way to remove
        # a specific the "cached" logger instance.
        # this is the illegal way. but lets just close our eyes
        import logging
        logging.RootLogger.manager.loggerDict.pop(self.name)

    # ....................................................................... #
    def _callFUT(self):
        from ..cli import cli_logger_factory
        return cli_logger_factory(
            name=self.name,
            out=self.out,
            err=self.err)

    # ....................................................................... #
    def test_logging_debug_to_stdout(self):
        test_string = "Vestibulum pharetra tortor ac turpis viverra"
        logger_ = self._callFUT()
        logger_.debug(test_string)
        self.assertTrue(test_string in self.out.getvalue())

    # ....................................................................... #
    def test_logging_info_to_stdout(self):
        test_string = "Aliquam cursus, mauris non ultrices laoreet, augue"
        logger_ = self._callFUT()
        logger_.info(test_string)
        self.assertTrue(test_string in self.out.getvalue())

    # ....................................................................... #
    def test_logging_warn_to_stderr(self):
        test_string = "Vivamus ornare mattis orci, vitae sagittis mi"
        logger_ = self._callFUT()
        logger_.warn(test_string)
        self.assertTrue(test_string in self.err.getvalue())

    # ....................................................................... #
    def test_logging_error_to_stderr(self):
        test_string = "Aliquam cursus, mauris non ultrices laoreet, augue"
        logger_ = self._callFUT()
        logger_.error(test_string)
        self.assertTrue(test_string in self.err.getvalue())

    # ....................................................................... #
    def test_logging_critical_to_stderr(self):
        test_string = "Duis lacinia, libero vitae sagittis varius"
        logger_ = self._callFUT()
        logger_.critical(test_string)
        self.assertTrue(test_string in self.err.getvalue())


# --------------------------------------------------------------------------- #
class Test_main(TestCase):

    # ....................................................................... #
    def _callFUT(self, *args, **kwargs):
        from ..cli import main
        return main(*args, **kwargs)

    # ....................................................................... #
    def test_main(self):

        test_return = 'test_run_method_return'

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        def dummy_cli_run(*args, **kwargs):
            return test_return

        self.assertEqual(
            self._callFUT(_cli_run=dummy_cli_run),
            test_return)
