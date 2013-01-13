# -*- coding: utf-8 -*-

"""
Test Cli Logger
"""

import unittest


# --------------------------------------------------------------------------- #
class Test_cli_logger_factory(unittest.TestCase):

    # ....................................................................... #
    def setUp(self):
        from ...compat import StringIO
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
        from ...cli.cli_logger import cli_logger_factory
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
class DummyLoggingRecord(object):

    # ....................................................................... #
    def __init__(self, levelno):
        self.levelno = levelno


# --------------------------------------------------------------------------- #
class Test_AllowedLevelsFilter(unittest.TestCase):

    # ....................................................................... #
    def _makeOne(self, *args, **kwargs):
        from ...cli.cli_logger import AllowedLevelsFilter
        return AllowedLevelsFilter(*args, **kwargs)

    # ....................................................................... #
    def test_filter_true(self):
        logging_record = DummyLoggingRecord(10)
        level_filter = self._makeOne([10, 20, 30])

        self.assertTrue(level_filter.filter(logging_record))

    # ....................................................................... #
    def test_filter_false(self):
        logging_record = DummyLoggingRecord(40)
        level_filter = self._makeOne([10, 20, 30])

        self.assertFalse(level_filter.filter(logging_record))
