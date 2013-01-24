# -*- coding: utf-8 -*-

"""
Test Template Renderer-
"""

from unittest import TestCase

from ...exceptions import InvalidName


# --------------------------------------------------------------------------- #
class DummyConfig(object):

    _asset_manager = None

    def __init__(self, _asset_manager_factory):
        self._asset_manager = _asset_manager_factory()


# --------------------------------------------------------------------------- #
class Test_BaseTemplateRender(TestCase):

    # ....................................................................... #
    def _makeOne(self, *args, **kwargs):
        from ...rendering import BaseTemplateRenderer

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class TestBaseTemplateRenderer(BaseTemplateRenderer):
            def get_rendered_config(self):
                pass

        return TestBaseTemplateRenderer(*args, **kwargs)

    # ....................................................................... #
    def test_init_and_check_required_initted_properties(self):

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyAssetManager(object):
            pass

        test_config = DummyConfig(_asset_manager_factory=DummyAssetManager)
        test_role_output_folder_path = 'test_role_output_folder_path'
        test_path = 'test_path'
        test_settings = {'test_settings_key': 'test_settings_value'}

        template_renderer = self._makeOne(
            config=test_config,
            role_output_folder_path=test_role_output_folder_path,
            path=test_path,
            settings=test_settings)

        self.assertIs(template_renderer.config, test_config)
        self.assertEqual(template_renderer.role_output_folder_path,
                         test_role_output_folder_path)
        self.assertEqual(template_renderer.path, test_path)
        self.assertDictEqual(template_renderer.settings, test_settings)

    # ....................................................................... #
    def test_output_file_path(self):

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyAssetManager(object):

            def path_join(self, path_parts):
                return '/'.join(path_parts)

        test_config = DummyConfig(_asset_manager_factory=DummyAssetManager)

        test_role_output_folder_path = 'test_role_output_folder_path'
        test_path = 'test_path'

        desired_output_file_path = '%s/%s' \
            % (test_role_output_folder_path, test_path)

        template_renderer = self._makeOne(
            config=test_config,
            role_output_folder_path=test_role_output_folder_path,
            path=test_path,
            settings={})

        self.assertEqual(template_renderer.output_file_path,
            desired_output_file_path)

    # ....................................................................... #
    def test_write(self):

        test_path_folder = 'test_path_folder'

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyAssetManager(object):

            def path_join(self, path_parts):
                return '/'.join(path_parts)

            def path_folder(self, path):
                return test_path_folder

            def asset_or_location_exists(self, path):
                pass

            def create_folder(self, path):
                return path

            def write_to_file(self, path, content):
                return path

        test_config = DummyConfig(_asset_manager_factory=DummyAssetManager)

        test_role_output_folder_path = 'test_role_output_folder_path'
        test_file = 'test_file'
        test_path = '%s/%s' % (test_path_folder, test_file)
        test_settings = {}

        desired_return = '%s/%s/%s' \
            % (test_role_output_folder_path, test_path_folder, test_file)

        template_renderer = self._makeOne(
            config=test_config,
            role_output_folder_path=test_role_output_folder_path,
            path=test_path,
            settings=test_settings)

        self.assertEqual(template_renderer.write(),
            desired_return)


# --------------------------------------------------------------------------- #
class Test_BaseTemplateRender_validate_path(TestCase):

    # ....................................................................... #
    def _callFUT(self, *args, **kwargs):
        from ...rendering import BaseTemplateRenderer
        return BaseTemplateRenderer.validate_path(*args, **kwargs)

    # ....................................................................... #
    def test_validate_path(self):

        test_path = 'test_path'
        self.assertEqual(self._callFUT(test_path), test_path)

    # ....................................................................... #
    def test_validate_path_for_exceptions(self):

        self.assertRaises(InvalidName, self._callFUT, ' bad_path')
        self.assertRaises(InvalidName, self._callFUT, '/bad_path')
        self.assertRaises(InvalidName, self._callFUT, '../bad_path')
        self.assertRaises(InvalidName, self._callFUT, './bad_path')

        self.assertRaises(InvalidName, self._callFUT, 'b/../ad_path')
        self.assertRaises(InvalidName, self._callFUT, 'b/./ad_path')
        self.assertRaises(InvalidName, self._callFUT, 'b<ad_path')
        self.assertRaises(InvalidName, self._callFUT, 'b>ad_path')
        self.assertRaises(InvalidName, self._callFUT, 'b:ad_path')
        self.assertRaises(InvalidName, self._callFUT, "b'ad_path")
        self.assertRaises(InvalidName, self._callFUT, 'b"ad_path')
        self.assertRaises(InvalidName, self._callFUT, 'b|ad_path')
        self.assertRaises(InvalidName, self._callFUT, 'b?ad_path')
        self.assertRaises(InvalidName, self._callFUT, 'b*ad_path')
        self.assertRaises(InvalidName, self._callFUT, 'b`ad_path')

    # ....................................................................... #
    def test_validate_role_name_for_exception_message1(self):

        test_bad_start_char = " "
        test_path = " bad_path"

        desired_error_message = "Path cannot start with '%s': %s" \
                    % (test_bad_start_char, test_path)

        self.assertRaisesRegexp(
            InvalidName,
            desired_error_message,
            self._callFUT,
            test_path)

    # ....................................................................... #
    def test_validate_role_name_for_exception_message2(self):

        test_bad_start_char = "<"
        test_path = "b<ad_path"

        desired_error_message = "Path cannot contain '%s': %s" \
                    % (test_bad_start_char, test_path)

        self.assertRaisesRegexp(
            InvalidName,
            desired_error_message,
            self._callFUT,
            test_path)
