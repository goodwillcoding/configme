# -*- coding: utf-8 -*-

"""
Test utilities
"""

from unittest import TestCase


# --------------------------------------------------------------------------- #
class DummyLoggingRecord(object):

    # ....................................................................... #
    def __init__(self, levelno):
        self.levelno = levelno


# --------------------------------------------------------------------------- #
class Test_AllowedLevelsFilter(TestCase):

    # ....................................................................... #
    def _makeOne(self, *args, **kwargs):
        from ...utils import AllowedLevelsFilter
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
