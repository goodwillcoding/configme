# -*- coding: utf-8 -*-

"""
Test Settings Parser
"""


from unittest import TestCase

from ..exceptions import SettingsParsingError


# --------------------------------------------------------------------------- #
def dummy_config_parser_maker(content=None,
                              fail_read=False,
                              raise_read_exception_message='',
                              raise_items_exception_message='',
                              make_read_loaded_files_empty=False):

    # ....................................................................... #
    class DummyConfigParser(object):

        __content = []
        __raise_read_exception_message = ''
        __raise_items_exception_message = ''
        __make_read_loaded_files_empty = False
        defaults = {}

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        def __init__(self, defaults=None):

            if defaults is None:  # pragma: no cover
                defaults = {}

            self.__content = content

            self.__raise_read_exception_message = \
                raise_read_exception_message

            self.__raise_items_exception_message = \
                raise_items_exception_message

            self.__make_read_loaded_files_empty = \
                make_read_loaded_files_empty

            self.defaults = defaults

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        def read(self, file_path):

            from ConfigParser import Error as ConfigParserError

            if self.__raise_read_exception_message != '':
                raise ConfigParserError(
                    self.__raise_read_exception_message)

            if self.__make_read_loaded_files_empty:
                return []

            return [file_path, ]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        def sections(self):
            return self.__content.keys()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        def items(self, section_name):

            from ConfigParser import Error as ConfigParserError

            result = []

            try:
                result = [(k, v % self.defaults) for k, v in
                            self.__content[section_name].iteritems()]
            except KeyError:
                # KeyError happens on bad iterpolation
                raise ConfigParserError("%s" %
                    self.__raise_items_exception_message)

            return result

    return DummyConfigParser


# --------------------------------------------------------------------------- #
class Test_settings_parser(TestCase):

    # ....................................................................... #
    def _makeOne(self, *args, **kwargs):
        from ..settings import SettingsParser
        return SettingsParser(*args, **kwargs)

    # ....................................................................... #
    def test_init_and_check_required_initted_properties(self):

        test_file_path = 'test_file_path'
        dummy_config_parser = dummy_config_parser_maker()

        settings_parser = self._makeOne(
            file_path=test_file_path,
            _config_parser_factory=dummy_config_parser)

        self.assertEqual(settings_parser.file_path, test_file_path)
        self.assertIsInstance(settings_parser.parser, dummy_config_parser)

    # ....................................................................... #
    def test_init_and_check_optional_initted_properties_defaults(self):

        test_file_path = 'test_file_path'
        dummy_config_parser = dummy_config_parser_maker()

        settings_parser = self._makeOne(
            file_path=test_file_path,
            _config_parser_factory=dummy_config_parser)

        self.assertEqual(settings_parser.file_path, test_file_path)

    # ....................................................................... #
    def test_read_no_files(self):

        test_settings_content = {}

        desired_result = []

        dummy_config_parser = dummy_config_parser_maker(
            content=test_settings_content)

        settings_parser = self._makeOne(
            file_path='some_file_path',
            _config_parser_factory=dummy_config_parser)

        self.assertListEqual(settings_parser.read(), desired_result)

    # ....................................................................... #
    def test_read_without_variables(self):

        test_settings_content = {
            'test_file': {'test_setting': 'test_setting_value'}
            }

        desired_result = [
            ('test_file', {'test_setting': 'test_setting_value'})
            ]

        dummy_config_parser = dummy_config_parser_maker(
            content=test_settings_content)

        settings_parser = self._makeOne(
            file_path='some_file_path',
            _config_parser_factory=dummy_config_parser)

        self.assertListEqual(settings_parser.read(), desired_result)

    # ....................................................................... #
    def test_read_with_variables(self):

        test_settings_content = {
            'test_file':
            {'test_setting': 'test_setting_value_with_var: %(test_var)s'}
        }

        test_variables = {'test_var': 'test_var_value'}

        desired_result = [
            ('test_file',
             {'test_setting': 'test_setting_value_with_var: test_var_value'})
            ]

        dummy_config_parser = dummy_config_parser_maker(
            content=test_settings_content)

        settings_parser = self._makeOne(
            file_path='some_file_path',
            variables=test_variables,
            _config_parser_factory=dummy_config_parser)

        self.assertListEqual(settings_parser.read(), desired_result)

    # ....................................................................... #
    def test_read_for_bad_variable_interpolation_exception(self):

        test_file_path = 'test_file_path'
        test_builtin_error_text = 'Bad variable interpolation for file:'
        test_error_text = 'test_error_text'

        test_settings_content = {
            'test_file':
            {'test_setting': 'test_setting_value_with_var: %(test_var)s'}
        }

        test_variables = {}

        dummy_config_parser = dummy_config_parser_maker(
            content=test_settings_content,
            raise_items_exception_message=test_error_text)

        settings_parser = self._makeOne(
            file_path=test_file_path,
            variables=test_variables,
            _config_parser_factory=dummy_config_parser)

        settings_parser = self._makeOne(
            file_path=test_file_path,
            _config_parser_factory=dummy_config_parser)

        # test for built in error message
        self.assertRaisesRegexp(
            SettingsParsingError,
            test_builtin_error_text,
            settings_parser.read
            )

        # test for file path in the error message
        self.assertRaisesRegexp(
            SettingsParsingError,
            test_file_path,
            settings_parser.read)

        # test for the bubbled up error in the error message
        self.assertRaisesRegexp(
            SettingsParsingError,
            test_error_text,
            settings_parser.read)

    # ....................................................................... #
    def test_read_for_could_not_parse_file_exception(self):

        test_file_path = 'test_file_path'
        test_builtin_error_text = '^Could not parse file:'
        test_error_text = 'test_error_text'

        dummy_config_parser = dummy_config_parser_maker(
            raise_read_exception_message=test_error_text)

        settings_parser = self._makeOne(
            file_path=test_file_path,
            _config_parser_factory=dummy_config_parser)

        # test for built in error message
        self.assertRaisesRegexp(
            SettingsParsingError,
            test_builtin_error_text,
            settings_parser.read)

        # test for the file path in the error message
        self.assertRaisesRegexp(
            SettingsParsingError,
            test_file_path,
            settings_parser.read)

        # test for the bubbled up error in the error message
        self.assertRaisesRegexp(
            SettingsParsingError,
            test_error_text,
            settings_parser.read)

    # ....................................................................... #
    def test_read_for_could_not_load_file_exception(self):

        test_file_path = 'test_file_path'
        test_builtin_error_text = 'Could not load file:'

        dummy_config_parser = dummy_config_parser_maker(
            make_read_loaded_files_empty=True)

        settings_parser = self._makeOne(
            file_path=test_file_path,
            _config_parser_factory=dummy_config_parser)

        settings_parser = self._makeOne(
            file_path=test_file_path,
            _config_parser_factory=dummy_config_parser)

        # test for built in error message
        self.assertRaisesRegexp(
            SettingsParsingError,
            test_builtin_error_text,
            settings_parser.read
            )

        # test for file path in the error message
        self.assertRaisesRegexp(
            SettingsParsingError,
            test_file_path,
            settings_parser.read)
