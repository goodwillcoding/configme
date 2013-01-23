# -*- coding: utf-8 -*-

"""
Test CLI initialization and configuration.
"""

from unittest import TestCase

from ..exceptions import ConfigMeException

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
class Test_cli_run(TestCase):

    # ....................................................................... #
    def setUp(self):
        from ..compat import StringIO
        self.logger_out = StringIO()
        self.logger_err = StringIO()
        self.logger_fatal = StringIO()

    # ....................................................................... #
    def tearDown(self):
        self.logger_out.close()
        self.logger_err.close()
        self.logger_fatal.close()

    # ....................................................................... #
    def _callFUT(self, *args, **kwargs):
        from ..cli import cli_run
        return cli_run(*args, **kwargs)

    # ....................................................................... #
    def test_cli(self):

        test_file1 = 'test_file1'
        test_file2 = 'test_path2/test_file2'
        test_output_list = [test_file1, test_file2]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyObject(object):
            def __init__(self, *args, **kwargs):
                pass

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyParsedArgs(object):

            templates_path = None
            settings_path = None
            output_path = None
            role_name = None
            role_suffix = None
            role_variables = None

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyArgumentParser(object):

            def __init__(self, *args, **kwargs):
                pass

            def parse(self, *args, **kwargs):
                return DummyParsedArgs()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyLogger(object):

            logger_err = None

            def __init__(self, out, *args, **kwargs):
                self.logger_out = out

            def info(self, message):
                self.logger_out.write(message)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyRole(object):

            def __init__(self, *args, **kwargs):
                pass

            def write_configs(self, *args, **kwargs):
                return test_output_list

        desired_return_code = 0
        desired_logger_out_output = "%s%s" % (test_file1, test_file2)

        return_code = self._callFUT(
            script_args=(),
            argument_parser=DummyArgumentParser(),
            logger_name='some_logger_name',
            logger_out=self.logger_out,
            logger_err=DummyObject(),
            logger_fatal=DummyObject(),
            _logger_factory=DummyLogger,
            _configurator_factory=DummyObject,
            _role_factory=DummyRole)

        logger_out_output = self.logger_out.getvalue()

        self.assertEqual(return_code, desired_return_code)
        self.assertEqual(logger_out_output, desired_logger_out_output)

    # ....................................................................... #
    def test_cli_run_fatal_exception(self):

        test_error_message = 'test_error_message'

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyObject(object):
            def __init__(self, *args, **kwargs):
                pass

        def dummy_logger_factory(*args, **kwargs):
            raise BaseException(test_error_message)

        desired_return_code = 2
        desired_logger_fatal_output = "" \
            "Fatal Error: could not even setup a basic logger.\n\n\n" \
            "More Info: %s" % test_error_message

        return_code = self._callFUT(
            script_args=(),
            argument_parser=DummyObject(),
            logger_name='some_logger_name',
            logger_out=DummyObject(),
            logger_err=DummyObject(),
            logger_fatal=self.logger_fatal,
            _logger_factory=dummy_logger_factory,
            _configurator_factory=DummyObject,
            _role_factory=DummyObject)

        logger_fatal_output = self.logger_fatal.getvalue()

        self.assertEqual(return_code, desired_return_code)
        self.assertEqual(logger_fatal_output, desired_logger_fatal_output)

    # ....................................................................... #
    def test_cli_run_known_exception(self):

        test_error_message = 'test_error_message'

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyObject(object):
            def __init__(self, *args, **kwargs):
                pass

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyArgumentParser(object):

            def __init__(self, *args, **kwargs):
                pass

            def parse(self, *args, **kwargs):
                raise ConfigMeException(test_error_message)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyLogger(object):

            logger_err = None

            def __init__(self, err, *args, **kwargs):
                self.logger_err = err

            def error(self, message):
                self.logger_err.write(message)

        desired_return_code = 1
        desired_logger_err_output = "Error: %s" % test_error_message

        return_code = self._callFUT(
            script_args=(),
            argument_parser=DummyArgumentParser(),
            logger_name='some_logger_name',
            logger_out=DummyObject(),
            logger_err=self.logger_err,
            logger_fatal=DummyObject(),
            _logger_factory=DummyLogger,
            _configurator_factory=DummyObject,
            _role_factory=DummyObject)

        logger_err_output = self.logger_err.getvalue()

        self.assertEqual(return_code, desired_return_code)
        self.assertEqual(logger_err_output, desired_logger_err_output)

    # ....................................................................... #
    def test_cli_run_unknown_exception(self):

        test_error_message = 'test_error_message'

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyObject(object):
            def __init__(self, *args, **kwargs):
                pass

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyArgumentParser(object):

            def __init__(self, *args, **kwargs):
                pass

            def parse(self, *args, **kwargs):
                raise BaseException(test_error_message)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyLogger(object):

            logger_err = None

            def __init__(self, err, *args, **kwargs):
                self.logger_err = err

            def error(self, message):
                self.logger_err.write(message)

        desired_return_code = 2
        desired_logger_err_output = "Unknown Error: %s" % test_error_message

        return_code = self._callFUT(
            script_args=(),
            argument_parser=DummyArgumentParser(),
            logger_name='some_logger_name',
            logger_out=DummyObject(),
            logger_err=self.logger_err,
            logger_fatal=DummyObject(),
            _logger_factory=DummyLogger,
            _configurator_factory=DummyObject,
            _role_factory=DummyObject)

        logger_err_output = self.logger_err.getvalue()

        self.assertEqual(return_code, desired_return_code)
        self.assertEqual(logger_err_output, desired_logger_err_output)


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
