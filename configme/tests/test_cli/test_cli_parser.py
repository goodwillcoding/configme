# -*- coding: utf-8 -*-

"""
Test Argument Parser
"""

import unittest

from ...exceptions import ScriptArgumentError


# --------------------------------------------------------------------------- #
class Test_CliArgumentParser(unittest.TestCase):

    # ....................................................................... #
    def _makeOne(self, *args, **kwargs):
        from ...cli.cli_parser import CliArgumentParser
        return CliArgumentParser(*args, **kwargs)

    # ....................................................................... #
    def test_error(self):

        test_error_message = 'test_error_message'

        parser = self._makeOne()

        # test that error is raised
        self.assertRaises(ScriptArgumentError, parser.error, '')
        # test that correct error message is displayed
        self.assertRaisesRegexp(
            ScriptArgumentError,
            'test_error_message',
            parser.error,
            test_error_message)

    # ....................................................................... #
    def test_parse(self):

        test_return = "test_parse_args_return"

        def dummy_parse_args(*args, **kwargs):
            return test_return

        test_args = ['some_argument']

        parser = self._makeOne()

        self.assertEqual(
            parser.parse(args=test_args, _parse_args_method=dummy_parse_args),
            test_return)

    # ....................................................................... #
    def test_parse_no_args_exception(self):

        test_args = []

        parser = self._makeOne()
        self.assertRaises(ScriptArgumentError, parser.parse, test_args)


# --------------------------------------------------------------------------- #
class DummyNamespace(object):
    pass


# --------------------------------------------------------------------------- #
class Test_CliArgumentParser_ArgListToDictAction(unittest.TestCase):

    # ....................................................................... #
    def _makeOne(self, *args, **kwargs):
        from ...cli.cli_parser import CliArgumentParser
        return CliArgumentParser.ArgListToDictAction(*args, **kwargs)

    # ....................................................................... #
    def test_ArgListToDictAction_callable(self):

        test_namespace = DummyNamespace()
        test_values = (("a", "b"), ("c", "d"))
        test_dest_variable = 'test_dest_variable'

        desired_dest_dict = {"a": "b", "c": "d"}

        action = self._makeOne(option_strings='', dest=test_dest_variable)

        # now call the action
        action(parser=None, namespace=test_namespace, values=test_values)
        self.assertDictEqual(
            getattr(test_namespace, test_dest_variable),
            desired_dest_dict)

    # ....................................................................... #
    def test_ArgListToDictAction_callable_duplicate_keys_overrides(self):

        test_namespace = DummyNamespace()
        test_values = (("a", "b"), ("c", "d"), ("a", "z"))
        test_dest_variable = 'test_dest_variable'

        desired_dest_dict = {"a": "z", "c": "d"}

        action = self._makeOne(option_strings='', dest=test_dest_variable)

        # now call the action
        action(parser=None, namespace=test_namespace, values=test_values)
        self.assertDictEqual(
            getattr(test_namespace, test_dest_variable),
            desired_dest_dict)


# --------------------------------------------------------------------------- #
class Test_SafeArgumentParser_split_argument(unittest.TestCase):

    # ....................................................................... #
    def _callFUT(self, test_list):
        from ...cli.cli_parser import CliArgumentParser
        parser = CliArgumentParser()
        return parser.split_argument(test_list)

    # ....................................................................... #
    def test_colon_separator(self):
        test_string = "a:b"
        desired_return_tuple = ("a", "b")

        self.assertTupleEqual(self._callFUT(test_string), desired_return_tuple)

    # ....................................................................... #
    def test_equal_separator(self):
        test_string = "a=b"
        desired_return_tuple = ("a", "b")

        self.assertTupleEqual(self._callFUT(test_string), desired_return_tuple)

    # ....................................................................... #
    def test_colon_separator_first(self):
        test_string = "a:=b"
        desired_return_tuple = ("a", "=b")

        self.assertTupleEqual(self._callFUT(test_string), desired_return_tuple)

    # ....................................................................... #
    def test_equal_separator_first(self):
        test_string = "a=:b"
        desired_return_tuple = ("a", ":b")

        self.assertTupleEqual(self._callFUT(test_string), desired_return_tuple)

    # ....................................................................... #
    def test_no_separator_exception(self):
        test_string = "ab"
        self.assertRaises(ScriptArgumentError, self._callFUT, test_string)
