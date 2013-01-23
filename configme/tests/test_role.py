# -*- coding: utf-8 -*-

import os

from unittest import TestCase

from ..exceptions import InvalidName


# --------------------------------------------------------------------------- #
class DummyConfig(object):

    templates_path = None
    settings_path = None
    output_path = None
    settings_file_extension = None
    _renderer = None

    # ................................................................... #
    def __init__(self,
                templates_path=None,
                 settings_path=None,
                 output_path=None,
                 settings_file_extension='some_settings_extension',
                 _settings_parser_factory=None,
                 _template_renderer_factory=None,
                 _asset_manager_factory=None):

        self._settings_parser_factory = _settings_parser_factory
        self._template_renderer_factory = _template_renderer_factory
        self._asset_manager_factory = _asset_manager_factory

        if self._asset_manager_factory is not None:
            self._asset_manager = self._asset_manager_factory()

        self.templates_path = templates_path
        self.settings_path = settings_path
        self.output_path = output_path
        self.settings_file_extension = settings_file_extension


# --------------------------------------------------------------------------- #
def dummy_setting_parser_maker(content):
    # use a factory so we can preload any content we want easily
    # and

    # ....................................................................... #
    class DummySettingsParser(object):

        # fake var used to store content the can "read"
        __content = {}

        _file_path = None
        _variables = None

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        def __init__(self, file_path, variables=None):
            self.__content = content

            if variables is None:  # pragma: no cover
                variables = {}

            self._file_path = file_path
            self._variables = variables

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        def read(self):

            result = []

            for section_name in self.__content:
                # interpolate values into section settings
                section_settings = [(k, v % self._variables) for k, v in
                            self.__content[section_name].iteritems()]

                result.append((section_name, section_settings))

            return result

    return DummySettingsParser


# --------------------------------------------------------------------------- #
class DummyTemplateRenderer(object):

    path = None
    role = None
    config = None

    # ....................................................................... #
    def __init__(self, config, role_output_folder_path, path, settings):
        self.role_output_folder_path = role_output_folder_path
        self.path = path

    # ....................................................................... #
    def write(self):
        return os.path.join(self.role_output_folder_path, self.path)


# --------------------------------------------------------------------------- #
def dummy_asset_manager_maker():

    # ....................................................................... #
    class DummyAssetManager(object):

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        def path_join(self, path_parts):
            return '/'.join(path_parts)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        def create_folder(self, folder_path):
            return folder_path

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        def remove_folder(self, folder_path):
            return folder_path

    return DummyAssetManager


# --------------------------------------------------------------------------- #
class Test_Role(TestCase):

    def _makeOne(self, *args, **kwargs):
        from ..role import Role
        return Role(*args, **kwargs)

    # ....................................................................... #
    def test_init_and_check_required_initted_properties(self):

        test_config = DummyConfig()
        test_name = 'test_name'

        role = self._makeOne(test_config, test_name)

        self.assertIs(role.config, test_config)
        self.assertEqual(role.name, test_name)

    # ....................................................................... #
    def test_init_and_check_optional_initted_properties(self):

        config = DummyConfig()
        test_suffix = 'test_suffix'
        test_variables = {'hello': 'world'}

        role = self._makeOne(
            config,
            'some_name',
            suffix=test_suffix,
            variables=test_variables)

        self.assertEqual(role.suffix, test_suffix)
        self.assertDictEqual(role.variables, test_variables)

    # ....................................................................... #
    def test_init_and_check_optional_initted_properties_defaults(self):

        config = DummyConfig()
        desired_default_suffix = ''
        desired_default_variables = {}

        role = self._makeOne(
            config,
            'some_name')

        self.assertEqual(role.suffix, desired_default_suffix)
        self.assertDictEqual(role.variables, desired_default_variables)

    # ....................................................................... #
    def test_name_value_assignment(self):

        config = DummyConfig()
        test_name = 'test_name'

        role = self._makeOne(config, name='some_name')

        role.name = test_name

        self.assertEqual(role.name, test_name)

    # ....................................................................... #
    def test_suffix_value_assignment(self):

        config = DummyConfig()
        test_suffix = 'test_suffix'

        role = self._makeOne(config, name='some_name')

        role.suffix = test_suffix

        self.assertEqual(role.suffix, test_suffix)

    # ....................................................................... #
    def test_suffixed_name_suffix_specified(self):
        # this is a computed property

        config = DummyConfig()
        test_name = 'test_name'
        test_suffix = 'test_suffix'

        desired_suffixed_name = "%s%s" % (test_name, test_suffix)
        role = self._makeOne(config, test_name, test_suffix)

        self.assertEqual(role.suffixed_name, desired_suffixed_name)

    # ....................................................................... #
    def test_suffixed_name_suffix_not_specified(self):
        # this is a computed property

        config = DummyConfig()
        test_name = 'test_name'

        role = self._makeOne(config, test_name)
        self.assertEqual(role.suffixed_name, test_name)

    # ....................................................................... #
    def test_output_folder_path(self):

        _asset_manager_factory = dummy_asset_manager_maker()

        test_output_path = '/test_output_path'
        config = DummyConfig(
            output_path=test_output_path,
            _asset_manager_factory=_asset_manager_factory)

        test_name = 'test_name'
        test_suffix = 'test_suffix'

        role = self._makeOne(config, test_name, test_suffix)
        desired_folder_path = '/'.join([test_output_path, role.suffixed_name])

        self.assertEqual(role.output_folder_path, desired_folder_path)

    # ....................................................................... #
    def test_settings_file_path(self):

        _asset_manager_factory = dummy_asset_manager_maker()

        test_settings_path = '/test_settings_path'
        test_settings_file_extension = 'test_settings_file_extension'
        config = DummyConfig(
            settings_path=test_settings_path,
            settings_file_extension=test_settings_file_extension,
            _asset_manager_factory=_asset_manager_factory)

        test_name = 'test_name'
        role = self._makeOne(config, test_name)

        temp_settings_file_name = "%s.%s" \
            % (test_name, config.settings_file_extension)

        desired_settings_file_path = '/'.join(
            [test_settings_path, temp_settings_file_name])

        self.assertEqual(role.settings_file_path, desired_settings_file_path)

    # ....................................................................... #
    def test_write_configs(self):

        test_output_config_file = 'test/test_config.conf'
        test_name = 'test_role'
        test_output_path = '/test_output_path'

        settings_content = {
            test_output_config_file: {'test_setting': 'test_value'},
            }

        _settings_parser_factory = \
            dummy_setting_parser_maker(content=settings_content)
        _template_renderer_factory = DummyTemplateRenderer
        _asset_manager_factory = dummy_asset_manager_maker()

        desired_output_list = [
            '%s/%s/%s' %
            (test_output_path, test_name, test_output_config_file)]

        config = DummyConfig(
            templates_path='/some_templates_path',
            settings_path='/some_settings_path',
            output_path=test_output_path,
            _settings_parser_factory=_settings_parser_factory,
            _template_renderer_factory=_template_renderer_factory,
            _asset_manager_factory=_asset_manager_factory
            )

        role = self._makeOne(config=config, name=test_name)
        self.assertListEqual(role.write_configs(), desired_output_list)

    # ....................................................................... #
    def test_write_configs_no_files(self):

        test_name = 'test_role'
        test_output_path = '/test_output_path'

        settings_content = {}

        _settings_parser_factory = \
            dummy_setting_parser_maker(content=settings_content)
        _template_renderer_factory = DummyTemplateRenderer
        _asset_manager_factory = dummy_asset_manager_maker()

        desired_output_list = []

        config = DummyConfig(
            templates_path='/some_templates_path',
            settings_path='/some_settings_path',
            output_path=test_output_path,
            _settings_parser_factory=_settings_parser_factory,
            _template_renderer_factory=_template_renderer_factory,
            _asset_manager_factory=_asset_manager_factory
            )

        role = self._makeOne(config=config, name=test_name)
        self.assertListEqual(role.write_configs(), desired_output_list)

    # ....................................................................... #
    def test_write_configs_with_suffix(self):

        test_output_config_file = 'test/test_config.conf'
        test_name = 'test_role'
        test_output_path = '/test_output_path'
        test_suffix = '+test_suffix'

        settings_content = {
            test_output_config_file:
            {'test_setting': 'test_value'},
        }
        _settings_parser_factory = \
            dummy_setting_parser_maker(content=settings_content)
        _template_renderer_factory = DummyTemplateRenderer
        _asset_manager_factory = dummy_asset_manager_maker()

        desired_output_list = [
            '%s/%s%s/%s' %
            (test_output_path,
             test_name,
             test_suffix,
             test_output_config_file)]

        config = DummyConfig(
            templates_path='/some_templates_path',
            settings_path='/some_settings_path',
            output_path=test_output_path,
            _settings_parser_factory=_settings_parser_factory,
            _template_renderer_factory=_template_renderer_factory,
            _asset_manager_factory=_asset_manager_factory
            )

        role = self._makeOne(config=config, name=test_name, suffix=test_suffix)
        self.assertListEqual(role.write_configs(), desired_output_list)

    # ....................................................................... #
    def test_write_configs_with_variables(self):

        test_output_config_file = 'test/test_config.conf'
        test_name = 'test_role'
        test_output_path = '/test_output_path'
        test_variables = {'test_var': 'test_var_value'}

        settings_content = {
            test_output_config_file:
            {'test_setting': 'test_value_with_var: %(test_var)s'},
        }

        _settings_parser_factory = \
            dummy_setting_parser_maker(content=settings_content)
        _template_renderer_factory = DummyTemplateRenderer
        _asset_manager_factory = dummy_asset_manager_maker()

        desired_output_list = [
            '%s/%s/%s' %
            (test_output_path,
             test_name,
             test_output_config_file)]

        config = DummyConfig(
            templates_path='/some_templates_path',
            settings_path='/some_settings_path',
            output_path=test_output_path,
            _settings_parser_factory=_settings_parser_factory,
            _template_renderer_factory=_template_renderer_factory,
            _asset_manager_factory=_asset_manager_factory
            )

        role = self._makeOne(
            config=config,
            name=test_name,
            variables=test_variables)

        self.assertListEqual(role.write_configs(), desired_output_list)


class Test_Role_validate_role_name(TestCase):

    # ....................................................................... #
    def _callFUT(self, *args, **kwargs):
        from ..role import Role
        return Role.validate_role_name(*args, **kwargs)

    # ....................................................................... #
    def test_validate_role_name(self):

        test_role_name = 'test_role_name'
        self.assertEqual(self._callFUT(test_role_name), test_role_name)

    # ....................................................................... #
    def test_validate_role_name_for_exceptions(self):

        self.assertRaises(InvalidName, self._callFUT, ' bad_name')
        self.assertRaises(InvalidName, self._callFUT, 'b<ad_name')
        self.assertRaises(InvalidName, self._callFUT, 'b>ad_name')
        self.assertRaises(InvalidName, self._callFUT, 'b:ad_name')
        self.assertRaises(InvalidName, self._callFUT, "b'ad_name")
        self.assertRaises(InvalidName, self._callFUT, 'b"ad_name')
        self.assertRaises(InvalidName, self._callFUT, 'b/ad_name')
        self.assertRaises(InvalidName, self._callFUT, 'b\\ad_name')
        self.assertRaises(InvalidName, self._callFUT, 'b|ad_name')
        self.assertRaises(InvalidName, self._callFUT, 'b?ad_name')
        self.assertRaises(InvalidName, self._callFUT, 'b*ad_name')
        self.assertRaises(InvalidName, self._callFUT, 'b`ad_name')

    # ....................................................................... #
    def test_validate_role_name_for_exception_message1(self):

        test_bad_start_char = " "
        test_role_name = " bad_role_name"

        desired_error_message = "Role name cannot start with '%s': %s" \
                    % (test_bad_start_char, test_role_name)

        self.assertRaisesRegexp(
            InvalidName,
            desired_error_message,
            self._callFUT,
            test_role_name)

    # ....................................................................... #
    def test_validate_role_name_for_exception_message2(self):

        test_bad_start_char = "<"
        test_role_name = "b<ad_role_name"

        desired_error_message = "Role name cannot contain '%s': %s" \
                    % (test_bad_start_char, test_role_name)

        self.assertRaisesRegexp(
            InvalidName,
            desired_error_message,
            self._callFUT,
            test_role_name)
