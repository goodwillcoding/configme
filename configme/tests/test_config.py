# -*- coding: utf-8 -*-

import unittest


from ..exceptions import LocationNotFound


# --------------------------------------------------------------------------- #
def dummy_asset_manager_maker(bad_path=None):

    # ....................................................................... #
    class DummyAssetManager(object):

        __bad_path = None

        def __init__(self):
            self.__bad_path = bad_path

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        def location(self, location, location_subject):

            if location == self.__bad_path:
                raise LocationNotFound()

            return location

    return DummyAssetManager


# --------------------------------------------------------------------------- #
class Test_Config(unittest.TestCase):

    # ....................................................................... #
    def _makeOne(self, *args, **kwargs):
        from ..config import Configurator
        return Configurator(*args, **kwargs)

    # ....................................................................... #
    def test_init_and_check_required_initted_properties(self):

        test_templates_path = 'templates_path'
        test_settings_path = 'settings_path'
        test_output_path = 'output_path'

        dummy_asset_manager_factory = dummy_asset_manager_maker()

        config = self._makeOne(
            templates_path=test_templates_path,
            settings_path=test_settings_path,
            output_path=test_output_path,
            _asset_manager_factory=dummy_asset_manager_factory)

        self.assertEqual(config.templates_path, test_templates_path)
        self.assertEqual(config.settings_path, test_settings_path)
        self.assertEqual(config.output_path, test_output_path)

    # ....................................................................... #
    def test_init_and_check_optional_initted_properties(self):

        test_extention = 'test_settings_file_extesion'

        dummy_asset_manager_factory = dummy_asset_manager_maker()

        config = self._makeOne(
            templates_path='some_templates_path',
            settings_path='some_settings_path',
            output_path='some_output_path',
            settings_file_extension=test_extention,
            _asset_manager_factory=dummy_asset_manager_factory)

        self.assertEqual(config.settings_file_extension, test_extention)

    # ....................................................................... #
    def test_init_and_check_optional_initted_properties_defaults(self):

        desired_extention = 'settings'

        dummy_asset_manager_factory = dummy_asset_manager_maker()

        config = self._makeOne(
            templates_path='some_templates_path',
            settings_path='some_settings_path',
            output_path='some_output_path',
            _asset_manager_factory=dummy_asset_manager_factory)

        self.assertEqual(config.settings_file_extension, desired_extention)

    # ....................................................................... #
    def test_templates_path_value_assignment(self):

        good_path = 'test_templates_path'

        dummy_asset_manager_factory = dummy_asset_manager_maker()

        config = self._makeOne(
            templates_path='some_templates_path',
            settings_path='some_settings_path',
            output_path='some_output_path',
            _asset_manager_factory=dummy_asset_manager_factory)

        config.templates_path = good_path
        self.assertEqual(config.templates_path, good_path)

    # ....................................................................... #
    def test_settings_path_value_assignment(self):

        good_path = 'test_settings_path'

        dummy_asset_manager_factory = dummy_asset_manager_maker()

        config = self._makeOne(
            templates_path='some_templates_path',
            settings_path='some_settings_path',
            output_path='some_output_path',
            _asset_manager_factory=dummy_asset_manager_factory)

        config.settings_path = good_path
        self.assertEqual(config.settings_path, good_path)

    # ....................................................................... #
    def test_output_path_value_assignment(self):

        good_path = 'test_output_path'

        dummy_asset_manager_factory = dummy_asset_manager_maker()

        config = self._makeOne(
            templates_path='some_templates_path',
            settings_path='some_settings_path',
            output_path='some_output_path',
            _asset_manager_factory=dummy_asset_manager_factory)

        config.output_path = good_path
        self.assertEqual(config.output_path, good_path)

    # ....................................................................... #
    def test_init_with_bad_templates_path_for_exceptions(self):

        bad_path = 'bad_template_path'

        dummy_asset_manager_factory = dummy_asset_manager_maker(bad_path)

        config_args = dict(
            templates_path=bad_path,
            settings_path='some_settings_path',
            output_path='some_output_path',
            _asset_manager_factory=dummy_asset_manager_factory)

        self.assertRaises(LocationNotFound, self._makeOne, **config_args)

    # ....................................................................... #
    def test_init_with_bad_settings_path_for_exceptions(self):

        bad_path = 'bad_settings_path'

        dummy_asset_manager_factory = dummy_asset_manager_maker(bad_path)

        config_args = dict(
            templates_path='some_templates_path',
            settings_path=bad_path,
            output_path='some_output_path',
            _asset_manager_factory=dummy_asset_manager_factory)

        self.assertRaises(LocationNotFound, self._makeOne, **config_args)

    # ....................................................................... #
    def test_init_with_bad_output_path_for_exceptions(self):

        bad_path = 'bad_output_path'

        dummy_asset_manager_factory = dummy_asset_manager_maker(bad_path)

        config_args = dict(
            templates_path='some_templates_path',
            settings_path='some_settings_path',
            output_path=bad_path,
            _asset_manager_factory=dummy_asset_manager_factory)

        self.assertRaises(LocationNotFound, self._makeOne, **config_args)

    # ....................................................................... #
    def test_templates_path_value_assignment_for_exceptions(self):

        bad_path = 'bad_templates_path'

        dummy_asset_manager_factory = dummy_asset_manager_maker(bad_path)

        config = self._makeOne(
            templates_path='some_templates_path',
            settings_path='some_settings_path',
            output_path='some_output_path',
            _asset_manager_factory=dummy_asset_manager_factory)

        self.assertRaises(LocationNotFound, setattr, config, "templates_path",
                          bad_path)

    # ....................................................................... #
    def test_settings_path_value_assignment_for_exceptions(self):

        bad_path = 'bad_settings_path'

        dummy_asset_manager_factory = dummy_asset_manager_maker(bad_path)

        config = self._makeOne(
            templates_path='some_templates_path',
            settings_path='some_settings_path',
            output_path='some_output_path',
            _asset_manager_factory=dummy_asset_manager_factory)

        self.assertRaises(LocationNotFound, setattr, config, "settings_path",
                          bad_path)

    # ....................................................................... #
    def test_output_path_value_assignment_for_exceptions(self):

        bad_path = 'bad_output_path'

        dummy_asset_manager_factory = dummy_asset_manager_maker(bad_path)

        config = self._makeOne(
            templates_path='some_templates_path',
            settings_path='some_settings_path',
            output_path='some_output_path',
            _asset_manager_factory=dummy_asset_manager_factory)

        self.assertRaises(LocationNotFound, setattr, config, "output_path",
                          bad_path)
